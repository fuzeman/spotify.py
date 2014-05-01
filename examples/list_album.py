from spotify.client import Spotify
import logging
import os


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    sp = Spotify()

    @sp.login(os.environ['USERNAME'], os.environ['PASSWORD'])
    def on_login():
        print 'logged on'

        @sp.metadata('spotify:album:7u6zL7kqpgLPISZYXNTgYk')
        def on_metadata(album):
            print 'on_metadata', album

    while True:
        raw_input()
