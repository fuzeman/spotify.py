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
            self.sp.search('daft punk', count=3, callback=self.on_search)

    def on_search(self, result):
        # Artists
        print 'artists (%s)' % result.artists_total

        for artist in result.artists:
            print '\t[%s] %s' % (artist.uri, artist.name)

        # Albums
        print 'albums (%s)' % result.albums_total

        for album in result.albums:
            print '\t[%s] %s - %s' % (album.uri, album.name, ', '.join([ar.name for ar in album.artists]))

        # Tracks
        print 'tracks (%s)' % result.tracks_total

        for track in result.tracks:
            print '\t[%s] %s' % (track.uri, track.name)

        # Playlists
        print 'playlists (%s)' % result.playlists_total

        for playlist in result.playlists:
            print '\t[%s] %s' % (playlist.uri, playlist.name)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    app = App()
    app.run()

    while True:
        raw_input()
