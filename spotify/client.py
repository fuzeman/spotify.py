from ws4py.client.threadedclient import WebSocketClient
import requests

USER_AGENT = 'Mozilla/5.0 (Chrome/13.37 compatible-ish) spotify.py'


class Spotify(object):
    def __init__(self, user_agent=USER_AGENT):
        self.auth_host = 'play.spotify.com'
        self.auth_path = '/xhr/json/auth.php'
        self.landing_path = '/'

        # Credentials
        self.credentials = {
            'type': 'anonymous'
        }

        # Create HTTP session
        self.session = requests.Session()

        # Update session headers
        self.session.headers.update({
            'User-Agent': user_agent
        })

    def login(self, username=None, password=None):
        if username and password:
            self.credentials = {
                'username': username,
                'password': password,
                'type': 'sp'
            }

        self.connect()

    def login_facebook(self, uid, token):
        self.credentials = {
            'fbuid': uid,
            'token': token,
            'type': 'fb'
        }

        self.connect()

    def connect(self):
        url = 'https://%s%s' % (self.auth_host, self.landing_path)

        r = self.session.get(url)


class SpotifyClient(WebSocketClient):
    def opened(self):
        pass

    def received_message(self, m):
        pass

    def closed(self, code, reason=None):
        pass
