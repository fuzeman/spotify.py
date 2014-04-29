from spotify.client import Spotify
import logging
import os

uri = 'spotify:album:7u6zL7kqpgLPISZYXNTgYk'

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    sp = Spotify()
    sp.login(os.environ['USERNAME'], os.environ['PASSWORD'])

    @sp.on('login')
    def on_login():
        print 'on_login'

        def on_get(album):
            print 'on_get', album

        sp.get(uri)\
          .on('success', on_get)

    while True:
        raw_input()
