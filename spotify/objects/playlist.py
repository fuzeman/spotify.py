from spotify.objects.base import Descriptor, PropertyProxy
from spotify.proto import playlist4changes_pb2
from spotify.proto import playlist4content_pb2


class PlaylistItem(Descriptor):
    __protobuf__ = playlist4content_pb2.Item

    uri = PropertyProxy

    added_by = PropertyProxy('attributes.added_by')


class Playlist(Descriptor):
    __protobuf__ = playlist4changes_pb2.ListDump

    uri = PropertyProxy
    name = PropertyProxy('attributes.name')

    length = PropertyProxy
    position = PropertyProxy('contents.pos')

    truncated = PropertyProxy('contents.truncated')

    items = PropertyProxy('contents.items', 'PlaylistItem')
