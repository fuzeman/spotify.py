from spotify.client import Spotify

import logging
import os

log = logging.getLogger(__name__)


class App(object):
    def __init__(self):
        self.sp = Spotify()

    def run(self):
        @self.sp.login(os.environ['USERNAME'], os.environ['PASSWORD'])
        def on_login():
            self.sp.user.collection('albumscoverlist', callback=self.on_album_collection)
            self.sp.user.collection('artistscoverlist', callback=self.on_artist_collection)

    def on_album_collection(self, albums):
        for album in albums:
            print '[%s] "%s" - %s - %s' % (
                album.uri, album.name,
                ', '.join([ar.name for ar in album.artists]),
                [c.file_url for c in album.covers if c]
            )

    def on_artist_collection(self, artists):
        for artist in artists:
            print '[%s] "%s" - %s' % (
                artist.uri, artist.name,
                [p.file_url for p in artist.portraits if p]
            )


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    app = App()
    app.run()

    while True:
        raw_input()
