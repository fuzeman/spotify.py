from dispatcher import Dispatcher
from track_reference import TrackReference
from util import log_progress

from jinja2 import Environment, FileSystemLoader
from spotify.client import Spotify
from threading import Event
import cherrypy
import logging
import os
import socket

env = Environment(loader=FileSystemLoader('templates'))
log = logging.getLogger(__name__)


class Server(object):
    def __init__(self, port=12555):
        self.port = port

        self.sp = Spotify()
        self.cache = {}

        self.current = None
        self.on_login = Event()

    def start(self):
        # Spotify
        self.sp.login(os.environ['USERNAME'], os.environ['PASSWORD'], lambda: self.on_login.set())

        # CherryPy
        cherrypy.config.update({
            'server.socket_host': '0.0.0.0',
            'server.socket_port': self.port
        })

        cherrypy.tree.mount(None, config={
            '/': {
                'request.dispatch': Dispatcher(self)
            }
        })

        cherrypy.engine.start()

    def album(self, uri):
        self.on_login.wait()  # Wait for login

        complete = Event()
        album_tracks = []

        # Fetch album metadata
        @self.sp.metadata(uri)
        def on_album(album):

            # Fetch metadata for each track
            @self.sp.metadata([tr.uri for tr in album.discs[0].tracks])
            def on_tracks(tracks):

                # Append onto 'tracks' list
                album_tracks.extend(tracks)

                # Work complete
                complete.set()

        # Wait until tracks are loaded (give up after 5 seconds)
        complete.wait(5)

        # Render template
        return env.get_template('album.html').render(
            tracks=[
                {'name': track.name, 'uri': str(track.uri)}
                for track in album_tracks
            ]
        )

    def track(self, uri):
        self.on_login.wait()  # Wait for login

        # Update current
        if self.current:
            # Track changed, call finish()
            if uri != self.current.uri:
                log.debug('Changing tracks, calling finish() on previous track')
                self.current.finish()

        # Create new TrackReference (if one doesn't exist yet)
        if uri not in self.cache:
            log.debug('[%s] Creating new TrackReference' % uri)

            # Create new track reference
            self.cache[uri] = TrackReference(self, uri)

        # Get track reference from cache
        tr = self.cache[uri]

        # Start download
        tr.fetch()

        # Update current
        self.current = tr

        r_start, r_end = self.handle_range(tr)

        # Update headers
        cherrypy.response.headers['Accept-Ranges'] = 'bytes'
        cherrypy.response.headers['Content-Type'] = tr.response_headers.getheader('Content-Type')
        cherrypy.response.headers['Content-Length'] = r_end - r_start

        # Progressively return track from buffer
        return self.stream(tr, r_start, r_end)

    track._cp_config = {'response.stream': True}

    @staticmethod
    def stream(tr, r_start, r_end):
        position = r_start

        chunk_size_min = 6 * 1024
        chunk_size_max = 10 * 1024

        chunk_scale = 0
        chunk_size = chunk_size_min

        last_progress = None

        while True:
            # Adjust chunk_size
            if chunk_scale < 1:
                chunk_scale = 2 * (float(position) / tr.stream_length)
                chunk_size = int(chunk_size_min + (chunk_size_max * chunk_scale))

                if chunk_scale > 1:
                    chunk_scale = 1

            if position + chunk_size > r_end:
                chunk_size = r_end - position

            # Read chunk
            chunk = tr.read(position, chunk_size)

            if not chunk:
                log.debug('[%s] Finished at %s bytes (content-length: %s)' % (tr.uri, position, tr.stream_length))
                break

            last_progress = log_progress(tr, '  Streaming', position, last_progress)

            position = position + len(chunk)

            # Write chunk
            yield chunk

        log.debug('[%s] Stream Complete', tr.uri)

    def handle_range(self, tr):
        r_start, r_end = self.parse_range(cherrypy.request.headers.get('Range'))

        if not r_start and not r_end:
            return 0, tr.stream_length - 1

        if r_end is None or r_end >= tr.stream_length:
            r_end = tr.stream_length - 1

        log.debug('[%s] Range: %s - %s', tr.uri, r_start, r_end)

        cherrypy.response.headers['Content-Range'] = 'bytes %s-%s/%s' % (r_start, r_end, tr.stream_length)
        cherrypy.response.status = 206

        return r_start, r_end

    @staticmethod
    def parse_range(value):
        value = value.split('=')

        if len(value) != 2:
            return 0, None

        range_type, range = value

        if range_type != 'bytes':
            return 0, None

        range = range.split('-')

        if len(range) != 2:
            return 0, None

        return int(range[0] or 0), int(range[1]) if range[1] else None

    def get_track_url(self, uri):
        return "http://%s:%d/track/%s.mp3" % (
            socket.gethostname(), self.port, uri
        )


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    server = Server()
    server.start()
