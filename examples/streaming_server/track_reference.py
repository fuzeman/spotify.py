from threading import Lock, Thread
from urllib import urlopen
import logging
import time

log = logging.getLogger(__name__)


class TrackReference(object):
    def __init__(self, server, uri):
        self.server = server
        self.uri = uri

        self.response = None
        self.info = None

        self.length = None

        self.reading = False

        self.buffer = bytearray()
        self.buffer_lock = Lock()

        self.read_lock = Lock()

        self.fetch_lock = Lock()
        self.fetch_thread = None

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

        self.fetch_thread = Thread(target=self.run)
        self.fetch_thread.start()

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

    def run(self):
        chunk_size = 1024
        last_progress = None

        self.reading = True

        while True:
            chunk = self.response.read(chunk_size)
            #log.debug('[%s] Received %s bytes', self.uri, len(chunk))

            with self.buffer_lock:
                self.buffer.extend(chunk)

            if not chunk:
                break

            last_progress = self.update_progress(len(self.buffer), last_progress)

        self.reading = False
        log.debug('[%s] Finished', self.uri)

    def read(self, start, chunk_size=1024):
        while self.reading and len(self.buffer) < start + 1:
            time.sleep(0.5)

        return self.buffer[start:start + chunk_size]

    def update_progress(self, position, last_progress):
        percent = float(position) / self.length
        value = int(percent * 20)

        if value == last_progress:
            return value

        log.debug('[%s] Downloading [%s|%s] %03d%%' % (
            self.uri,
            (' ' * value),
            (' ' * (20 - value)),
            int(percent * 100)
        ))

        return value
