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
        self.sp.explore.new_releases(callback=self.on_new_releases)

    def on_new_releases(self, result):
        print result.items


if __name__ == '__main__':
    app = App()
    app.run()

    while True:
        raw_input()
