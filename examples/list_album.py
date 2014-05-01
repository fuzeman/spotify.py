from spotify.client import Spotify
import logging
import os
from spotify.objects import Album


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    sp = Spotify()

    @sp.login(os.environ['USERNAME'], os.environ['PASSWORD'])
    def on_login():
        print 'logged on'

        @sp.metadata('spotify:album:7u6zL7kqpgLPISZYXNTgYk')
        def on_metadata(album):
            print 'album.name', album.name
            print 'album.genres', album.genres

    while True:
        raw_input()
