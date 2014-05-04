from spotify.core.helpers import set_defaults
from spotify.core.uri import Uri
from spotify.objects.base import Metadata, PropertyProxy
from spotify.proto import metadata_pb2


class Track(Metadata):
    __protobuf__ = metadata_pb2.Track

    gid = PropertyProxy
    uri = PropertyProxy('gid', func=lambda gid: Uri.from_gid('track', gid))
    name = PropertyProxy

    albums = PropertyProxy('album', 'Album')
    artists = PropertyProxy('artist', 'Artist')

    number = PropertyProxy
    disc_number = PropertyProxy
    duration = PropertyProxy

    popularity = PropertyProxy
    explicit = PropertyProxy

    external_ids = PropertyProxy('external_id', 'ExternalId')
    restrictions = PropertyProxy('restriction', 'Restriction')
    files = PropertyProxy('file', 'AudioFile')
    alternatives = PropertyProxy('alternative', 'Track')
    # sale_period - []
    preview = PropertyProxy

    def track_uri(self, callback=None, async=True, timeout=None):
        """Requests the track stream URI.

        :param callback: Callback to trigger on a successful response
        :type callback: function

        :return: decorate wrapper if no callback is provided, otherwise
                 returns the `Request` object.
        :rtype: function or `spotify.core.request.Request`
        """
        request = self.build('sp/track_uri', 'mp3160', self.uri.to_id())

        return self.request_wrapper(request, callback)

    def track_event(self, lid, event, time):
        """Send the "sp/track_event" event.

        :param lid: Stream lid (from "sp/track_uri")
        :param event: Event
        :param time: Current track playing position (in milliseconds)
        """
        return self.send(
            'sp/track_event',
            lid,
            event,
            time
        )

    def track_progress(self, lid, position, source='unknown', reason='unknown', latency=150,
                       context='unknown', referrer=None):

        referrer = set_defaults(referrer, {
            'referrer': 'unknown',
            'version': '0.1.0',
            'vendor': 'com.spotify'
        })

        return self.send(
            'sp/track_progress',
            lid,

            # Start
            source,
            reason,

            # Timings
            position,
            latency,

            # Context
            context,
            str(self.uri),

            # Referrer
            referrer['referrer'],
            referrer['version'],
            referrer['vendor'],
        )

    def track_end(self, lid, position, seeks=None, latency=150, context='unknown',
                  source=None, reason=None, referrer=None):

        seeks = set_defaults(seeks, {
            'num_forward': 0,
            'num_backward': 0,
            'ms_forward': 0,
            'ms_backward': 0
        })

        source = set_defaults(source, {
            'start': 'unknown',
            'end': 'unknown'
        })

        reason = set_defaults(reason, {
            'start': 'unknown',
            'end': 'unknown'
        })

        referrer = set_defaults(referrer, {
            'referrer': 'unknown',
            'version': '0.1.0',
            'vendor': 'com.spotify'
        })

        return self.send(
            'sp/track_end',
            lid,

            # Timings
            position,  # ms_played
            position,  # ms_played_union

            # Seek count
            seeks['num_forward'],
            seeks['num_backward'],
            seeks['ms_forward'],
            seeks['ms_backward'],

            latency,

            # Context
            str(self.uri),
            context,

            # Source
            source['start'],
            source['end'],

            # Reason
            reason['start'],
            reason['end'],

            # Referrer
            referrer['referrer'],
            referrer['version'],
            referrer['vendor'],

            position  # max_continuous
        )
