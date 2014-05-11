from spotify.client import Spotify

import logging
import os

log = logging.getLogger(__name__)


class App(object):
    artist_uri = 'spotify:artist:4tZwfgrHOc3mvqYlEYSvVi'  # Daft Punk

    def __init__(self):
        self.sp = Spotify()

        self.tracks = None
        self.album = None

    def run(self):
        @self.sp.login(os.environ['USERNAME'], os.environ['PASSWORD'])
        def on_login():
            # Fetch metadata for album
            self.sp.metadata(self.artist_uri, self.on_artist)

    def on_artist(self, artist):
        self.sp.metadata(artist.albums[0].uri, self.on_album)

    def on_album(self, album):
        print album.name

        self.sp.metadata([tr.uri for tr in album.tracks], self.on_tracks)

    def on_tracks(self, tracks):
        for track in tracks:
            print '\t[%s] - %s' % (track.uri, track.name)



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    app = App()
    app.run()

    while True:
        raw_input()
