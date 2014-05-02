from spotify.objects.base import Metadata, PropertyProxy
from spotify.proto import metadata_pb2


class Copyright(Metadata):
    __protobuf__ = metadata_pb2.Copyright

    type = PropertyProxy
    text = PropertyProxy
