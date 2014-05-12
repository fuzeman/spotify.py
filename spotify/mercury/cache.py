import logging
import time
from spotify.core.helpers import convert
from spotify.core.uri import Uri

log = logging.getLogger(__name__)


class MercuryCache(object):
    schema_types = {
        'vnd.spotify/metadata-album': 'album',
        'vnd.spotify/metadata-track': 'track'
    }

    content_types = [
        'hm://metadata/album',
        'hm://metadata/track'
    ]

    def __init__(self):
        self._store = {}

    def key_content(self, content_type):
        key = self.schema_types.get(content_type)

        if key is None:
            log.debug('ignoring item with content_type: "%s"', content_type)
            return None

        return key

    def key_hermes(self, content_type, internal):
        content_key = self.key_content(content_type)

        if content_key is None:
            return None, None

        uri = Uri.from_gid(content_key, internal.gid)

        # TODO hermes specific code, look into this again later
        return 'hm://metadata/%s' % uri.type, uri.to_id()

    def key(self, hm):
        x = hm.rindex('/')

        k_content = hm[:x]

        if k_content not in self.content_types:
            return None, None

        k_item = hm[x + 1:]

        return k_content, k_item

    def store(self, header, content_type, internal):
        k_content, k_item = self.key_hermes(content_type, internal)

        if not k_content or not k_item:
            return None

        log.debug('store - k_content: %s, k_item: %s', k_content, k_item)

        if self._store.get(k_content) is None:
            self._store[k_content] = {}

        item = MercuryCacheItem.create(header, content_type, internal)

        self._store[k_content][k_item] = item

        return item

    def get(self, hm):
        k_content, k_item = self.key(hm)

        if not k_content or not k_item:
            return False

        log.debug('get - k_content: %s, k_item: %s', k_content, k_item)

        if self._store.get(k_content) is None:
            return None

        item = self._store[k_content].get(k_item)

        if item is None:
            return None

        if not item.is_valid():
            del self._store[k_content][k_item]
            return None

        return item


class MercuryCacheItem(object):
    def __init__(self, ttl, version, policy, content_type, internal):
        self.ttl = ttl
        self.version = version
        self.policy = policy

        self.content_type = content_type
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
    def create(cls, header, content_type, internal):
        params = dict([(field.name, field.value) for field in header.user_fields])

        return cls(
            convert(params.get('MC-TTL'), int),
            convert(params.get('MD-Version'), int),
            params.get('MC-Cache-Policy'),

            content_type,
            internal
        )
