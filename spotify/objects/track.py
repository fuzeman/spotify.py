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

    def track_uri(self):
        return self.send('sp/track_uri', 'mp3160', self.uri.to_id())
