class Metadata(object):
    __protobuf__ = None

    @classmethod
    def parse(cls, data):
        internal = cls.__protobuf__()
        internal.ParseFromString(data)

        return cls(internal)
