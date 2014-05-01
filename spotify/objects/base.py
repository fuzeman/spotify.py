class PropertyProxy(object):
    def __init__(self, name):
        self.name = name


class Metadata(object):
    __protobuf__ = None

    def __init__(self, internal):
        self._internal = internal

        self._proxies = self._find_proxies()

    def _find_proxies(self):
        proxies = {}

        for key in dir(self):
            if key.startswith('_'):
                continue

            value = getattr(self, key)

            if value is PropertyProxy:
                proxies[key] = PropertyProxy(key)
            elif isinstance(value, PropertyProxy):
                proxies[key] = value

        return proxies

    def __getattribute__(self, name):
        if name.startswith('_'):
            return super(Metadata, self).__getattribute__(name)

        # Check for property proxy
        proxies = getattr(self, '_proxies', None)

        if proxies and name in proxies:
            proxy = proxies.get(name)

            if isinstance(proxy, PropertyProxy):
                return getattr(self._internal, proxy.name, None)

        return super(Metadata, self).__getattribute__(name)

    @classmethod
    def parse(cls, data):
        internal = cls.__protobuf__()
        internal.ParseFromString(data)

        return cls(internal)
