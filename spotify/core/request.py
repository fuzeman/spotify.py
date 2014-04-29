from pyemitter import Emitter
import logging

log = logging.getLogger(__name__)


class Request(Emitter):
    def __init__(self, name, id, args):
        self.name = name
        self.id = id

        self.args = args

    def process(self, data):
        if 'error' in data:
            return self.emit('error', data['error'])
        elif 'id' in data:
            return self.emit('success', data)

        error = 'Unhandled WebSocket message'

        log.error('%s: %s' % (error, data))
        return self.emit('error', error)

    def build(self):
        return {
            'name': self.name,
            'id': str(self.id),
            'args': self.args
        }
