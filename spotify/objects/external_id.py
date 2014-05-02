from spotify.objects.base import Metadata, PropertyProxy
from spotify.proto import metadata_pb2


class ExternalId(Metadata):
    __protobuf__ = metadata_pb2.ExternalId

    type = PropertyProxy
    id = PropertyProxy
