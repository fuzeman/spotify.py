from spotify.objects.base import Metadata
from spotify.proto import metadata_pb2


class Album(Metadata):
    __protobuf__ = metadata_pb2.Album

    def __init__(self, internal):
        self.internal = internal
