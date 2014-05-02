from spotify.objects.base import Metadata, PropertyProxy
from spotify.proto import metadata_pb2


class Track(Metadata):
    __protobuf__ = metadata_pb2.Track

    gid = PropertyProxy
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
