import logging
import time
from spotify.core.helpers import convert

log = logging.getLogger(__name__)


class MercuryCache(object):
    accepted_content = {
        'vnd.spotify/metadata-album': 'album',
        'vnd.spotify/metadata-track': 'track'
    }

    def __init__(self):
        self._store = {}

    def content_key(self, content_type):
        key = self.accepted_content.get(content_type)

        if key is None:
            log.debug('ignoring item with content_type: "%s"', content_type)
            return None

        return key

    def store(self, header, content_type, internal):
        key = self.content_key(content_type)

        if key is None:
            return False

        log.debug('store - key: %s, internal.uri: %s', key, repr(internal.gid))

        if self._store.get(key) is None:
            self._store[key] = {}

        self._store[key][internal.gid] = MercuryCacheItem.create(header, internal)

        return True

    def get(self, content_type, gid):
        key = self.content_key(content_type)

        if key is None:
            return None

        if self._store.get(key) is None:
            return None

        item = self._store[key].get(gid)

        if not item.is_valid():
            del self._store[key][gid]
            return None

        return item.internal




class MercuryCacheItem(object):
    def __init__(self, ttl, version, policy, internal):
        self.ttl = ttl
        self.version = version
        self.policy = policy

        self.internal = internal
        self.gid = internal.gid

        self.timestamp = time.time()

    def is_valid(self):
        elapsed = (time.time() - self.timestamp) * 1000

        return elapsed < self.ttl

    def __repr__(self):
        return '<MercuryCacheItem %s>' % (
            ', '.join([
                ('%s: %s' % (key, repr(getattr(self, key, None))))
                for key in [
                    'ttl', 'version', 'policy',
                    'gid', 'internal'
                ]
            ])
        )

    @classmethod
    def create(cls, header, internal):
        params = dict([(field.name, field.value) for field in header.user_fields])

        return cls(
            convert(params.get('MC-TTL'), int),
            convert(params.get('MD-Version'), int),
            params.get('MC-Cache-Policy'),

            internal
        )
