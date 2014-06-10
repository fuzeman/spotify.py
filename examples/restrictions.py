from spotify.client import Spotify

import logging
import os

log = logging.getLogger(__name__)


class App(object):
    uris = [
        'spotify:track:6xYcv63zDYiEaJ1KGgysGN',
        'spotify:track:77w4HJEAGzRwHTapyXjFl1',
        'spotify:track:3sgebd31wwbZY8Uyda3yOC',
        'spotify:track:7q3FEfKhqCF3w6Q8uTfDuH',
        'spotify:track:2n9TFOPyTnN0uYdzscNA4g',
        'spotify:track:08du7WH5gMBaCB9TlIpOiI',
        'spotify:track:2xuw7EWGdn5nYWezDx41xu'
    ]

    def __init__(self):
        self.sp = Spotify()

    def run(self):
        @self.sp.login(os.environ['USERNAME'], os.environ['PASSWORD'])
        def on_login():
            self.sp.user_info['country'] = 'NL'

            self.sp.metadata(self.uris, self.on_tracks)

    def on_tracks(self, tracks):
        results = []

        for track in tracks:
            original_uri = track.uri

            if not track.is_available():
                track.find_alternative()

            results.append((str(original_uri), track))

        for original, track in results:
            print original, str(track.uri)
            print '\tis_available:', track.is_available()

            for restriction in track.restrictions:
                print '\tallowed:', ', '.join(restriction.countries_allowed)
                print '\tforbidden:', ', '.join(restriction.countries_forbidden)

            print


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    app = App()
    app.run()

    while True:
        raw_input()
