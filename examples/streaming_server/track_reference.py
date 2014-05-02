from threading import Lock
from urllib import urlopen
import logging

log = logging.getLogger(__name__)


class TrackReference(object):
    def __init__(self, server, uri):
        self.server = server
        self.uri = uri

        self.response = None
        self.info = None

        self.length = None

        self.buffer = ''
        self.read_lock = Lock()

        self.fetch_lock = Lock()

    def fetch(self, blocking=True):
        if self.response:
            log.debug('[%s] already fetched track, returning from cache' % self.uri)
            return

        self.fetch_lock.acquire()

        # Request metadata
        self.server.sp.metadata(self.uri)\
                      .on('success', self.on_metadata)

        if blocking:
            # Wait until we are ready
            self.fetch_lock.acquire()

        return self.fetch_lock

    def on_metadata(self, track):
        track.track_uri()\
             .on('success', self.on_track_uri)

    def on_track_uri(self, response):
        result = response.get('result')

        if not result or 'uri' not in result:
            log.warn('Invalid track_uri response')
            self.fetch_lock.release()
            return

        self.response = urlopen(result['uri'])
        self.info = self.response.info()

        self.length = int(self.info.getheader('Content-Length'))

        self.fetch_lock.release()

    def read(self, start, chunk_size=1024):
        # Check if range is in the buffer
        if start < len(self.buffer):
            log.debug('[%s] returning %s bytes from buffer' % (
                self.uri, len(self.buffer) - start
            ))
            return self.buffer[start:]

        with self.read_lock:
            log.debug('trying to read chunk of size %s - %s', chunk_size, self.response.fp.closed)

            # Read chunk from request stream
            chunk = self.response.read(chunk_size)

            # Store in buffer
            self.buffer = self.buffer + chunk

            return chunk
