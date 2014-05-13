from spotify.client import Spotify

import logging
import os

log = logging.getLogger(__name__)


class App(object):
    #album_uri = 'spotify:album:7u6zL7kqpgLPISZYXNTgYk'  # Alive 2007
    album_uri = 'spotify:album:1x4SGGPflZamzny9QXRsdi'  # Tourist History

    def __init__(self):
        self.sp = Spotify()

        self.track_uris = None
        self.tracks = None

        self.album = None

        self.request_num = 0

    def run(self):
        @self.sp.login(os.environ['USERNAME'], os.environ['PASSWORD'])
        def on_login():
            # Fetch metadata for album
            self.sp.metadata(self.album_uri, self.on_album)

    def on_album(self, album):
        self.album = album

        # Request track metadata
        self.track_uris = [tr.uri for tr in self.album.tracks]

        self.sp.metadata([
            self.track_uris[0],
            self.track_uris[5],
            self.track_uris[3]
        ], self.on_tracks)

    def on_tracks(self, tracks):
        self.request_num += 1
        self.tracks = tracks

        log.info('%s - %s', self.album.name, ', '.join([artist.name for artist in self.album.artists]))

        for track in self.tracks:
            #if not track.is_available():
            #    track.find_alternative()

            log.info('\t[%02d] (%s) %s', track.number, track.uri, track.name)

        if self.request_num >= 2:
            return

        self.sp.metadata([
            self.track_uris[0],
            self.track_uris[6],
            self.track_uris[3],
            self.track_uris[4],
            self.track_uris[5]
        ], self.on_tracks)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    app = App()
    app.run()

    while True:
        raw_input()
