from spotify.core.request import Request
from spotify.mercury.cache import MercuryCache
from spotify.objects import NAME_MAP
from spotify.proto import mercury_pb2

from collections import OrderedDict
import base64
import httplib
import logging

log = logging.getLogger(__name__)
cache = MercuryCache()


class MercuryRequest(Request):
    def __init__(self, sp, name, requests, schema_response, header=None,
                 defaults=None):
        """
        :type sp: spotify.client.Spotify
        :type name: str
        :type requests: list of dict
        :type schema_response: dict or spotify.objects.base.Descriptor

        :type header: dict
        :type defaults: dict
        """
        super(MercuryRequest, self).__init__(sp, name, None)

        self.requests = requests if type(requests) is list else [requests]
        self.schema_response = schema_response
        self.defaults = defaults

        self.request = None
        self.payload = None

        self.response = OrderedDict()

        self.prepare(header, self.requests)

    def prepare(self, header, requests):
        payload = mercury_pb2.MercuryMultiGetRequest()

        for request in requests:
            request = self.prepare_request(request)

            response = cache.get(request.uri)

            if response:
                # Found valid response in cache
                self.response[request.uri] = response
                continue

            payload.request.extend([request])

        if not len(payload.request):
            return

        if len(payload.request) == 1:
            self.request = payload.request[0]
            return

        if header is None:
            raise ValueError('A header is required to send multiple requests')

        header['content_type'] = 'vnd.spotify/mercury-mget-request'

        self.request = self.prepare_request(header)
        self.payload = payload

    def prepare_request(self, request):
        m_request = mercury_pb2.MercuryRequest()

        # Fill MercuryRequest
        m_request.uri = request.get('uri', '')
        m_request.content_type = request.get('content_type', '')
        m_request.method = request.get('method', '')
        m_request.source = request.get('source', '')

        return m_request

    def process(self, data):
        log.debug('process data: %s', repr(data))
        result = data['result']

        header = mercury_pb2.MercuryRequest()
        header.ParseFromString(base64.b64decode(result[0]))

        if 400 <= header.status_code < 600:
            message = httplib.responses[header.status_code] or 'Unknown Error'

            if 400 <= header.status_code < 500:
                self.emit('error', 'Client Error: %s (%s)' % (message, header.status_code))
            elif 500 <= header.status_code < 600:
                self.emit('error', 'Server Error: %s (%s)' % (message, header.status_code))

            return

        if self.payload and header.content_type != 'vnd.spotify/mercury-mget-reply':
            self.emit('error', 'Server Error: Server didn\'t send a multi-GET reply for a multi-GET request!')
            return

        self.process_reply(header, base64.b64decode(result[1]))

    def process_reply(self, header, data):
        if header.content_type == 'vnd.spotify/mercury-mget-reply':
            response = mercury_pb2.MercuryMultiGetReply()
            response.ParseFromString(data)

            items = [
                (item.content_type, self.parse_item(item.body, item.content_type))
                if item.status_code == 200 else None
                for item in response.reply
            ]
        else:
            items = [
                (header.content_type, self.parse_item(data, header.content_type))
            ]

        for content_type, internal in items:
            uri = '/'.join(cache.key_hermes(content_type, internal))

            self.response[uri] = cache.store(header, content_type, internal)

        self.respond()

    def parse_item(self, data, content_type):
        parser_cls = self.get_descriptor(content_type)

        internal = parser_cls.__protobuf__()
        internal.ParseFromString(data)

        return internal

    def respond(self):
        if len(self.response) != len(self.requests):
            return False

        result = []

        for uri, item in self.response.items():
            cls = self.get_descriptor(item.content_type)

            result.append(cls.from_protobuf(self.sp, item.internal, NAME_MAP, self.defaults))

        log.debug('returning result: %s', result)

        if len(self.requests) == 1:
            self.emit('success', result[0] if result else None)
        else:
            self.emit('success', result)

        return True

    def get_descriptor(self, content_type):
        parser_cls = self.schema_response

        if type(parser_cls) is dict:
            parser_cls = parser_cls.get(content_type)

        if parser_cls is None:
            self.emit('error', 'Unrecognized metadata type: "%s"' % content_type)
            return None

        return parser_cls

    def build(self, seq):
        if self.respond() or not self.request:
            return None

        self.args = [
            self.get_number(self.request.method),
            base64.b64encode(self.request.SerializeToString())
        ]

        if self.payload:
            self.args.append(base64.b64encode(self.payload.SerializeToString()))

        return super(MercuryRequest, self).build(seq)

    def get_number(self, method):
        if method == 'SUB':
            return 1

        if method == 'UNSUB':
            return 2

        return 0
