from spotify.client import Spotify
import logging
import os


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    sp = Spotify()
    sp.login(os.environ['USERNAME'], os.environ['PASSWORD'])

    while True:
        raw_input()
