from spotify.objects.base import Metadata, PropertyProxy
from spotify.proto import metadata_pb2


class Artist(Metadata):
    __protobuf__ = metadata_pb2.Artist

    gid = PropertyProxy
    name = PropertyProxy

    popularity = PropertyProxy
    top_track = PropertyProxy

    album_group = PropertyProxy
    single_group = PropertyProxy
    compilation_group = PropertyProxy
    appears_on_group = PropertyProxy

    genres = PropertyProxy('genre')
    external_ids = PropertyProxy('external_id', 'ExternalId')

    portraits = PropertyProxy('portrait')
    biographies = PropertyProxy('biography')

    activity_periods = PropertyProxy('activity_period')
    restrictions = PropertyProxy('restriction')
    related = PropertyProxy('related')

    is_portrait_album_cover = PropertyProxy('is_portrait_album_cover')
    portrait_group = PropertyProxy('portrait_group')
