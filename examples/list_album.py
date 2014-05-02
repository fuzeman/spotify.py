from spotify.client import Spotify

import logging
import os


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    sp = Spotify()

    def play_track(uri):
        @sp.metadata(str(uri))
        def on_metadata(track):
            print '\t', track
            print '\turi:', repr(track.uri)

            def on_track_uri(res):
                print res

            track.track_uri().on('success', on_track_uri)

    @sp.login(os.environ['USERNAME'], os.environ['PASSWORD'])
    def on_login():
        print 'logged on'

        @sp.metadata('spotify:album:7u6zL7kqpgLPISZYXNTgYk')
        def on_metadata(album):
            play_track(album.discs[0].tracks[0].uri)

    while True:
        raw_input()
