from spotify.components.base import Component

import logging

log = logging.getLogger(__name__)


class Metadata(Component):
    def __init__(self, sp):
        super(Metadata, self).__init__(sp)

    def get(self, uris):
        log.debug('metadata(%s)', uris)

        if type(uris) is not list:
            uris = [uris]

        # array of "request" Objects that will be protobuf'd
        requests = []
        h_type = ''

        for uri in uris:
            uri_type = self.uri.type(uri)

            if uri_type == 'local':
                log.debug('ignoring "local" track URI: %s', uri)
                continue

            uri_id = self.uri.id(uri)

            h_type = type

            requests.append({
                'method': 'GET',
                'uri': 'hm://metadata/%s/%s' % (uri_type, uri_id)
            })

        header = {
            'method': 'GET',
            'uri': 'hm://metadata/%ss' % h_type
        }

        multi_get = True

        if len(requests) == 1:
            header = requests[0]
            requests = None
            multi_get = False

        self.send_protobuf({
            'header': header,
            'payload': requests,
            'is_multi_get': multi_get,
            'response_schema': {
                'vnd.spotify/metadata-artist': Artist,
                'vnd.spotify/metadata-album': Album,
                'vnd.spotify/metadata-track': Track
            }
        })

