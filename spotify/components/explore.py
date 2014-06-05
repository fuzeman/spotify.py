from spotify.components.base import Component
from spotify.core.helpers import set_defaults

import urllib
import time


class Explore(Component):
    base_url = "https://api.tunigo.com/v3/space/%s?%s"
    base_params = {
        'suppress_response_codes': 1,
        'locale':   'en',
        'product':  'premium',
        'version':  '6.31.1',
        'platform': 'web'
    }

    def featured_playlists(self):
        pass

    def top_playlists(self):
        pass

    def new_releases(self, page=0, per_page=100, callback=None):
        self.request("new-releases", {
            'page': page,
            'per_page': per_page
        })

    def request(self, action, params=None):
        query = self.prepare_query(params)

        url = self.base_url % (
            action, query
        )

        print url

        #self.session.get(

        #)

    def prepare_query(self, params):
        params = set_defaults(params, self.base_params)

        params['dt'] = time.strftime("%Y-%m-%dT%H:%M:%S")
        params['region'] = self.sp.country or 'us'

        return urllib.urlencode(params)
