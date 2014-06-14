import logging
logging.basicConfig(level=logging.DEBUG)

from spotify.client import Spotify

log = logging.getLogger(__name__)


class App(object):
    def __init__(self):
        self.sp = Spotify()

    def run(self):
        #@self.sp.login(os.environ['USERNAME'], os.environ['PASSWORD'])
        #def on_login():
        self.sp.explore.featured_playlists(callback=self.on_featured_playlists)
        self.sp.explore.top_playlists(callback=self.on_top_playlists)
        self.sp.explore.new_releases(callback=self.on_new_releases)

    def on_featured_playlists(self, result):
        for playlist in result.items:
            print '[%s] "%s" - %s' % (playlist.uri, playlist.name, playlist.image.file_url)

    def on_top_playlists(self, result):
        for playlist in result.items:
            print '[%s] "%s" - %s' % (playlist.uri, playlist.name, playlist.image.file_url)

    def on_new_releases(self, result):
        for album in result.items:
            print '[%s] "%s" - %s' % (album.uri, album.name, ', '.join([ar.name for ar in album.artists]))


if __name__ == '__main__':
    app = App()
    app.run()

    while True:
        raw_input()
