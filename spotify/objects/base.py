from google.protobuf.internal.containers import RepeatedCompositeFieldContainer
import datetime


class PropertyProxy(object):
    def __init__(self, name=None, type_=None, func=None):
        self.name = name
        self.type = type_
        self.func = func

    def get(self, obj, type_map):
        if self.name in obj._cache:
            return obj._cache[self.name]

        value = getattr(obj._internal, self.name, None)
        value = self.parse(value, type_map)

        obj._cache[self.name] = value
        return value

    def parse(self, value, type_map):
        # Retrieve 'type' from type_map
        if type(self.type) is str:
            if self.type not in type_map:
                raise ValueError('Unknown type "%s"' % self.type)

            self.type = type_map[self.type]

        # Use 'func' if specified
        if self.func:
            return self.func(value)

        if not self.type:
            return value

        # Convert to 'type'
        if isinstance(value, (list, RepeatedCompositeFieldContainer)):
            return [self.type(x, type_map) for x in value]

        return self.type(value, type_map)

    @staticmethod
    def parse_date(value):
        try:
            return datetime.date(value.year, value.month, value.day)
        except:
            return None


class Metadata(object):
    __protobuf__ = None

    def __init__(self, internal, type_map):
        self._internal = internal

        self._proxies = self._find_proxies()
        self._type_map = type_map
        self._cache = {}

    def _find_proxies(self):
        proxies = {}

        for key in dir(self):
            if key.startswith('_'):
                continue

            value = getattr(self, key)

            if value is PropertyProxy:
                proxies[key] = PropertyProxy(key)
            elif isinstance(value, PropertyProxy):
                if value.name is None:
                    value.name = key

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
                return proxy.get(self, self._type_map)

        return super(Metadata, self).__getattribute__(name)

    def __repr__(self):
        return '<%s.%s %s>' % (
            self.__class__.__module__,
            self.__class__.__name__,

            ', '.join([
                ('%s: %s' % (k, repr(getattr(self, k))))
                for k in self._proxies
            ])
        )

    def __str__(self):
        return self.__repr__()

    @classmethod
    def parse(cls, data, type_map):
        internal = cls.__protobuf__()
        internal.ParseFromString(data)

        return cls(internal, type_map)
