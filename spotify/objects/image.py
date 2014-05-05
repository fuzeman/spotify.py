from spotify.objects.base import Descriptor, PropertyProxy
from spotify.proto import metadata_pb2


class Image(Descriptor):
    __protobuf__ = metadata_pb2.Image

    file_id = PropertyProxy
    size = PropertyProxy

    width = PropertyProxy
    height = PropertyProxy
