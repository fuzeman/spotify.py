import binascii

base62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


class Uri(object):
    def __init__(self, type, code):
        self.type = type
        self.code = code

    def to_id(self):
        v = 0

        for c in self.code:
            v = v * 62 + base62.index(c)

        return hex(v)[2:-1].rjust(32, "0")

    def to_gid(self):
        pass

    def __str__(self):
        return 'spotify:%s:%s' % (self.type, self.code)

    def __repr__(self):
        return '<Uri %s>' % (self.__str__())

    @classmethod
    def from_id(cls, type, id):
        if not id:
            return None

        res = []
        v = int(id, 16)

        while v > 0:
            res = [v % 62] + res
            v /= 62

        code = ''.join([base62[i] for i in res])

        return cls(type, code.rjust(22, '0'))

    @classmethod
    def from_gid(cls, type, gid):
        id = binascii.hexlify(gid).rjust(32, '0')

        return cls.from_id(type, id)

    @classmethod
    def from_uri(cls, uri):
        parts = uri.split(':')

        if len(parts) == 3:
            parts = parts[1:]
        elif len(parts) < 2 or len(parts) > 3:
            raise ValueError('Unknown URI provided')

        return cls(parts[0], parts[1])
