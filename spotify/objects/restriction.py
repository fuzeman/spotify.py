from spotify.objects.base import Metadata, PropertyProxy
from spotify.proto import metadata_pb2


class Restriction(Metadata):
    __protobuf__ = metadata_pb2.Restriction

    catalogue = PropertyProxy
    countries_allowed = PropertyProxy
    countries_forbidden = PropertyProxy
    type = PropertyProxy
