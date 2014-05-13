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
            self.sp.user.playlists(callback=self.on_playlists)
            self.sp.playlist('spotify:user:fuzeman:playlist:4AMR1hLgWrMbZkMneOqUw3', callback=self.on_playlist)

    def on_playlists(self, playlists):
        print "=" * 25

        print 'length:', playlists.length
        print 'position:', playlists.position
        print 'truncated:', playlists.truncated

        print 'items:'

        for item in playlists.fetch():
            print '\t"%s" (%s)' % (item.name, item.uri)

        print "=" * 25

    def on_playlist(self, playlist):
        print playlist.name
        print "-" * 25

        print 'length:', playlist.length
        print 'position:', playlist.position
        print 'truncated:', playlist.truncated

        print 'items:'

        for item in playlist.fetch():
            print '\t"%s" (%s)' % (item.name, item.uri)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    app = App()
    app.run()

    while True:
        raw_input()
