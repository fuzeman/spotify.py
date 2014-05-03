from pyemitter import Emitter
import logging

log = logging.getLogger(__name__)


class Request(Emitter):
    def __init__(self, sp, name, args):
        """
        :type sp: spotify.client.Spotify
        :type name: str
        :type args: tuple or list or None
        """

        self.sp = sp
        self.name = name
        self.args = args

    def send(self):
        self.sp._connection.send_request(self)
        return self

    def process(self, data):
        if 'error' in data:
            return self.emit('error', data['error'])
        elif 'id' in data:
            return self.emit('success', data)

        error = 'Unhandled WebSocket message'

        log.error('%s: %s' % (error, data))
        return self.emit('error', error)

    def build(self, seq):
        return {
            'name': self.name,
            'id': str(seq),
            'args': list(self.args)
        }
