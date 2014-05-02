from spotify.objects.base import Metadata, PropertyProxy
from spotify.proto import metadata_pb2


class AudioFile(Metadata):
    __protobuf__ = metadata_pb2.AudioFile

    file_id = PropertyProxy
    format = PropertyProxy
