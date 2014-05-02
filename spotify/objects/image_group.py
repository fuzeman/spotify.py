from spotify.objects.base import Metadata, PropertyProxy
from spotify.proto import metadata_pb2


class ImageGroup(Metadata):
    __protobuf__ = metadata_pb2.ImageGroup

    images = PropertyProxy('image', 'Image')
