from spotify.objects.base import Metadata, PropertyProxy
from spotify.proto import metadata_pb2


class Disc(Metadata):
    __protobuf__ = metadata_pb2.Disc

    number = PropertyProxy
    name = PropertyProxy
    tracks = PropertyProxy('track', 'Track')
