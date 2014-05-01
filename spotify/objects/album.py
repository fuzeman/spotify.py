from spotify.objects.base import Metadata, PropertyProxy
from spotify.proto import metadata_pb2


class Album(Metadata):
    __protobuf__ = metadata_pb2.Album

    name = PropertyProxy

    genres = PropertyProxy('genre')

    def __init__(self, internal):
        super(Album, self).__init__(internal)
