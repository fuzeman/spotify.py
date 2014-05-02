from spotify.components.base import Component
from spotify.core.protobuf_request import ProtobufRequest
from spotify.core.uri import Uri
from spotify.objects import Album, Track, Artist

import logging

log = logging.getLogger(__name__)


class Metadata(Component):
    def __init__(self, sp):
        super(Metadata, self).__init__(sp)

    def get(self, uris, callback=None):
        log.debug('metadata(%s)', uris)

        if type(uris) is not list:
            uris = [uris]

        # array of "request" Objects that will be protobuf'd
        requests = []
        h_type = ''

        for uri in uris:
            uri = Uri.from_uri(uri)

            if uri.type == 'local':
                log.debug('ignoring "local" track URI: %s', uri)
                continue

            h_type = uri.type

            requests.append({
                'method': 'GET',
                'uri': 'hm://metadata/%s/%s' % (uri.type, uri.to_id())
            })

        # Build ProtoRequest
        request = ProtobufRequest(self.sp, 'sp/hm_b64', requests, {
            'vnd.spotify/metadata-artist': Artist,
            'vnd.spotify/metadata-album': Album,
            'vnd.spotify/metadata-track': Track
        }, {
            'method': 'GET',
            'uri': 'hm://metadata/%ss' % h_type
        })

        # Send request
        self.send_request(request)

        # Bind callback (if one exists)
        if callback:
            request.on('success', callback)

        return request
