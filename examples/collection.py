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
            self.sp.user.collection('albumscoverlist', callback=self.on_collection)

    def on_collection(self, albums):
        for album in albums:
            print album.name
            print album.uri
            print album.artists[0].name
            print album.artists[0].uri
            print album.covers[0].file_url


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    app = App()
    app.run()

    while True:
        raw_input()
