from spotify.core.uri import Uri
from spotify.objects import Track
from util import log_progress

from threading import Lock, Thread
from urllib import urlopen
import logging
import time

log = logging.getLogger(__name__)


class TrackReference(object):
    buffer_wait_ms = 100
    buffer_wait = buffer_wait_ms / 1000.0

    def __init__(self, server, uri):
        self.server = server
        self.uri = uri

        self.response = None
        self.response_headers = None

        self.stream_length = None
        self.stream_info = None

        self.reading = False
        self.playing = False
        self.finished = False

        self.start_time = None

        self.buffer = bytearray()

        self.track = None
        self.fetch_lock = Lock()
        self.fetch_thread = None

    def fetch(self, blocking=True):
        if self.response:
            log.debug('[%s] already fetched track, returning from cache' % self.uri)
            return

        self.fetch_lock.acquire()

        # Create a "shell" track (to access uri functions)
        self.track = Track.construct(self.server.sp, uri=Uri.from_uri(self.uri))

        # Request the track_uri
        self.track.track_uri(self.on_track_uri)

        if blocking:
            # Wait until we are ready
            self.fetch_lock.acquire()

        return self.fetch_lock

    def on_track_uri(self, response):
        self.stream_info = response.get('result')

        if not self.stream_info or 'uri' not in self.stream_info:
            log.warn('Invalid track_uri response')
            self.fetch_lock.release()
            return

        self.response = urlopen(self.stream_info['uri'])
        self.response_headers = self.response.info()

        log.info('Opened "%s"', self.stream_info['uri'])
        log.info('Info: %s', self.response_headers)

        self.stream_length = int(self.response_headers.getheader('Content-Length'))
        log.info('Length: %s', self.stream_length)

        if self.response_headers.getheader('Content-Type') == 'text/xml':
            # Error, log response
            log.debug(self.response.read())
        else:
            # Download track for streaming
            self.fetch_thread = Thread(target=self.run)
            self.fetch_thread.start()

        self.fetch_lock.release()

        # Request full metadata for future use
        @self.server.sp.metadata(self.uri)
        def on_metadata(track):
            log.debug('received full track metadata')
            self.track = track

    def run(self):
        chunk_size = 1024
        last_progress = None

        self.reading = True

        while True:
            chunk = self.response.read(chunk_size)
            #log.debug('[%s] Received %s bytes', self.uri, len(chunk))

            self.buffer.extend(chunk)

            if not chunk:
                break

            last_progress = log_progress(self, 'Downloading', len(self.buffer), last_progress)

        self.reading = False
        log.debug('[%s] Download Complete', self.uri)

    def read(self, start, chunk_size=1024):
        if not self.playing:
            self.track.track_event(self.stream_info['lid'], 3, 0)
            self.start_time = time.time()
            self.playing = True

        while self.reading and len(self.buffer) < start + 1:
            time.sleep(self.buffer_wait)

        return self.buffer[start:start + chunk_size]

    def finish(self):
        if self.finished:
            return

        self.finished = True

        position_ms = int((time.time() - self.start_time) * 1000)

        if position_ms > self.track.duration:
            position_ms = self.track.duration

        log.debug('position_ms: %s, duration: %s', position_ms, self.track.duration)

        self.track.track_end(self.stream_info['lid'], position_ms)
