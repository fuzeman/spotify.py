from spotify.core.uri import Uri
from spotify.objects.base import Metadata, PropertyProxy
from spotify.proto import metadata_pb2


class Album(Metadata):
    __protobuf__ = metadata_pb2.Album

    gid = PropertyProxy
    uri = PropertyProxy('gid', func=lambda gid: Uri.from_gid('album', gid))
    name = PropertyProxy

    artists = PropertyProxy('artist', 'Artist')
    type = PropertyProxy

    label = PropertyProxy
    date = PropertyProxy(func=PropertyProxy.parse_date)
    popularity = PropertyProxy

    genres = PropertyProxy('genre')
    covers = PropertyProxy('cover', 'Image')
    external_ids = PropertyProxy('external_id', 'ExternalId')

    discs = PropertyProxy('disc', 'Disc')
    # review - []
    copyrights = PropertyProxy('copyright', 'Copyright')
    restrictions = PropertyProxy('restriction', 'Restriction')
    # related - []
    # sale_period - []
    cover_group = PropertyProxy('cover_group', 'ImageGroup')
