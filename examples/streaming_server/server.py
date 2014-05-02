from dispatcher import Dispatcher
from spotify.client import Spotify
from track_reference import TrackReference

from jinja2 import Environment, FileSystemLoader
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

    def on_login(self):
        log.debug('on_login')

    def start(self):
        # Spotify
        self.sp.login(os.environ['USERNAME'], os.environ['PASSWORD'], self.on_login)

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
        print 'uri', uri

        album = self.sp.metadata(uri).wait()
        print 'album.name: %s' % album.name

        track_uris = [str(tr.uri) for tr in album.discs[0].tracks]

        # TODO multi-get
        tracks = [self.sp.metadata(track_uri).wait() for track_uri in track_uris]

        for x, track in enumerate(tracks):
            print 'discs[0].tracks[%s].name: %s' % (x, track.name)

        # Render template
        return env.get_template('album.html').render(
            tracks=[
                {'name': track.name, 'uri': str(track.uri)}
                for track in tracks
            ]
        )

    def track(self, uri):
        # Create new TrackReference (if one doesn't exist yet)
        if uri not in self.cache:
            log.debug('[%s] Creating new TrackReference' % uri)

            # Create new track reference
            self.cache[uri] = TrackReference(self, uri)

        # Get track reference from cache
        tr = self.cache[uri]

        # Start download
        tr.fetch()

        cherrypy.response.headers['Content-Type'] = tr.info.getheader('Content-Type')
        cherrypy.response.headers['Content-Length'] = tr.info.getheader('Content-Length')

        # Progressively read the stream
        def stream():
            position = 0

            chunk_size_min = 6 * 1024
            chunk_size_max = 10 * 1024

            chunk_scale = 0
            chunk_size = chunk_size_min

            last_progress = None

            while True:
                # Adjust chunk_size
                if chunk_scale < 1:
                    chunk_scale = 2 * (float(position) / tr.length)
                    chunk_size = int(chunk_size_min + (chunk_size_max * chunk_scale))

                    if chunk_scale > 1:
                        chunk_scale = 1

                # Read chunk
                log.debug('{%s] read - position: %s, chunk_size: %s' % (tr.uri, position, chunk_size))
                chunk = tr.read(position, chunk_size)
                log.debug('[%s] finished read')

                if not chunk:
                    log.debug('[%s] Finished at %s bytes (content-length: %s)' % (tr.uri, position, tr.length))
                    break

                position = position + len(chunk)

                # Write chunk
                yield chunk

                last_progress = self.update_progress(tr, position, last_progress)

        return stream()

    track._cp_config = {'response.stream': True}

    @staticmethod
    def update_progress(tr, position, last_progress):
        percent = float(position) / tr.length
        value = int(percent * 20)

        if value == last_progress:
            return value

        log.debug('[%s] Downloading [%s|%s] %03d%%' % (
            tr.uri,
            (' ' * value),
            (' ' * (20 - value)),
            int(percent * 100)
        ))

        return value

    def get_track_url(self, uri):
        return "http://%s:%d/track/%s.mp3" % (
            socket.gethostname(), self.port, uri
        )


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    server = Server()
    server.start()
