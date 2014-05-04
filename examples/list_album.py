from spotify.client import Spotify

import logging
import os
import time


class App(object):
    def __init__(self):
        self.sp = Spotify()

        self.tracks = None
        self.album = None

    def run(self):
        @self.sp.login(os.environ['USERNAME'], os.environ['PASSWORD'])
        def on_login():
            # Fetch metadata for album
            self.sp.metadata('spotify:album:7u6zL7kqpgLPISZYXNTgYk', self.on_album)

    def on_album(self, album):
        self.album = album

        # Request track metadata
        self.sp.metadata([tr.uri for tr in self.album.discs[0].tracks], self.on_tracks)

    def on_tracks(self, tracks):
        self.tracks = tracks

        print '%s - %s' % (self.album.name, ', '.join([artist.name for artist in self.album.artists]))

        for track in self.tracks:
            print '\t[%02d] %s' % (track.number, track.name)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    app = App()
    app.run()

    while True:
        raw_input()
