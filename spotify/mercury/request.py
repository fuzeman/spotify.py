from spotify.core.request import Request
from spotify.core.uri import Uri
from spotify.objects import NAME_MAP
from spotify.proto import mercury_pb2

from collections import OrderedDict
import base64
import httplib
import json
import logging

log = logging.getLogger(__name__)


class MercuryRequest(Request):
    def __init__(self, sp, name, requests, schema, header=None, defaults=None):
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

        self.schema = schema
        self.defaults = defaults

        self.request = None
        self.request_payload = None
        self.multi = None

        self.response = OrderedDict()
        self.response_type = 'Protobuf'

        self.prepared_requests = []
        self.prepare(header)

    def prepare(self, header):
        payload = mercury_pb2.MercuryMultiGetRequest()

        for request in self.requests:
            request = self.parse_request(request)

            if header and self.cached_response(request):
                continue

            # Update payload
            payload.request.extend([request])

            self.prepared_requests.append(request)

        # Ensure we have at least one request
        if not len(payload.request):
            return

        log.debug('prepared %s requests', len(payload.request))

        if len(payload.request) == 1:
            # Single request
            self.request = payload.request[0]
            return

        # Multi request
        if header is None:
            # Header required
            raise ValueError('A header is required to send multiple requests')

        header['content_type'] = 'vnd.spotify/mercury-mget-request'

        # Prepare header
        self.request = self.parse_request(header)
        self.request_payload = payload

    def process(self, data):
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

        if self.request_payload and header.content_type != 'vnd.spotify/mercury-mget-reply':
            self.emit('error', 'Server Error: Server didn\'t send a multi-GET reply for a multi-GET request!')
            return

        self.process_reply(header, base64.b64decode(result[1]))

    def process_reply(self, header, data):
        content_type = header.content_type.split(';')

        if header.content_type == 'vnd.spotify/mercury-mget-reply':
            self.multi = True

            response = mercury_pb2.MercuryMultiGetReply()
            response.ParseFromString(data)

            # Parse items
            items = [
                (item.content_type, self.parse_protobuf(
                    item.body, item.content_type
                ))
                if item.status_code == 200 else None
                for item in response.reply
            ]
        elif content_type and content_type[0].endswith('+json'):
            self.response_type = 'MercuryJSON'
            self.multi = True

            data = json.loads(data)

            # Parse items
            items = [
                (Uri.from_uri(item.get('uri')).type, item)
                for item in data
            ]
        else:
            self.multi = False

            # Parse items
            items = [(header.content_type, self.parse_protobuf(
                data, header.content_type
            ))]

        for x, (content_type, internal) in enumerate(items):
            self.update_response(x, header, content_type, internal)

        self.respond()

    def build(self, seq):
        if self.respond() or not self.request:
            return None

        self.args = [
            self.get_number(self.request.method),
            base64.b64encode(self.request.SerializeToString())
        ]

        if self.request_payload:
            self.args.append(base64.b64encode(self.request_payload.SerializeToString()))

        return super(MercuryRequest, self).build(seq)

    def respond(self):
        # Incorrect response count, not finished yet
        if len(self.response) < len(self.requests):
            return False

        result = []

        # Build objects from protobuf responses
        for uri, item in self.response.items():
            if item is None:
                return False

            content_type, internal = item

            # Get item descriptor
            cls = self.find_descriptor(content_type)

            # Build object from data
            if type(internal) is dict:
                item = cls.from_dict(self.sp, internal, NAME_MAP)
            else:
                item = cls.from_protobuf(self.sp, internal, NAME_MAP, self.defaults)

            result.append(item)

        # Emit success event
        if len(self.requests) == 1 and not self.multi:
            self.emit('success', result[0])
        else:
            self.emit('success', result)

        return True

    @staticmethod
    def get_number(method):
        if method == 'SUB':
            return 1

        if method == 'UNSUB':
            return 2

        return 0

    #
    # Parsing
    #

    def parse_protobuf(self, data, content_type):
        parser_cls = self.find_descriptor(content_type)

        internal = parser_cls.__protobuf__()
        internal.ParseFromString(data)

        return internal

    def find_descriptor(self, content_type):
        cls = self.schema

        # Multi-response schema
        if type(cls) is dict:
            cls = cls.get(content_type)

        # Unable to find descriptor
        if cls is None:
            self.emit('error', 'Unrecognized content_type: "%s"' % content_type)
            return None

        return cls

    @staticmethod
    def parse_request(request):
        m_request = mercury_pb2.MercuryRequest()

        # Fill MercuryRequest
        m_request.uri = request.get('uri', '')
        m_request.content_type = request.get('content_type', '')
        m_request.method = request.get('method', '')
        m_request.source = request.get('source', '')

        return m_request

    #
    # Response caching
    #

    def cached_response(self, request):
        return False

    def update_response(self, index, header, content_type, internal):
        self.response[internal.gid] = (content_type, internal)
