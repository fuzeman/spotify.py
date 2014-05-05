from spotify.objects.base import Descriptor, PropertyProxy
from spotify.proto import metadata_pb2


class ExternalId(Descriptor):
    __protobuf__ = metadata_pb2.ExternalId

    type = PropertyProxy
    id = PropertyProxy
