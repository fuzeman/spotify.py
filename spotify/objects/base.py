from spotify.components.base import Component

from google.protobuf.internal.containers import RepeatedCompositeFieldContainer
import datetime


class PropertyProxy(object):
    def __init__(self, name=None, type_=None, func=None):
        self.name = name
        self.type = type_
        self.func = func

    def get_attribute(self, instance, path):
        if type(path) is str:
            path = path.split('.')

        key = path.pop(0)

        if not hasattr(instance, key):
            return None

        value = getattr(instance, key)

        if not len(path):
            return value

        return self.get_attribute(value, path)

    def get(self, key, obj, type_map):
        if key in obj._cache:
            return obj._cache[key]

        # Pull value from instance or protobuf
        original = (
            self.get_attribute(obj, self.name) or
            self.get_attribute(obj._internal, self.name)
        )

        # Transform attribute values
        value = self.parse(obj, original, type_map)

        # Cache for later use
        obj._cache[key] = value

        return value

    def parse(self, obj, value, type_map):
        # Retrieve 'type' from type_map
        if type(self.type) is str:
            if not type_map:
                return value

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
            return [self.type(obj.sp, x, type_map) for x in value]

        return self.type(obj.sp, value, type_map)

    @staticmethod
    def parse_date(value):
        try:
            return datetime.date(value.year, value.month, value.day)
        except:
            return None


class Descriptor(Component):
    __protobuf__ = None

    def __init__(self, sp, internal=None, type_map=None):
        super(Descriptor, self).__init__(sp)

        self._internal = internal

        self._proxies = self._find_proxies()
        self._type_map = type_map
        self._cache = {}

    def update(self, obj, *args):
        # Clear cache to ensure we don't use previous values
        self._cache = {}

        # Update 'self' with values from 'obj'
        for key in args:
            setattr(self, key, getattr(obj, key))

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
            return super(Descriptor, self).__getattribute__(name)

        if name in self.__dict__:
            return self.__dict__[name]

        # Check for property proxy
        proxies = getattr(self, '_proxies', None)

        if proxies and name in proxies:
            proxy = proxies.get(name)

            if isinstance(proxy, PropertyProxy):
                return proxy.get(name, self, self._type_map)

        return super(Descriptor, self).__getattribute__(name)

    def __str__(self):
        return self.__repr__()

    @classmethod
    def parse(cls, sp, data, type_map):
        internal = cls.__protobuf__()
        internal.ParseFromString(data)

        return cls(sp, internal, type_map)

    @classmethod
    def construct(cls, sp, **kwargs):
        obj = cls(sp)

        for key, value in kwargs.items():
            setattr(obj, key, value)

        return obj
