from spotify.objects.album import Album
from spotify.objects.album_group import AlbumGroup
from spotify.objects.artist import Artist
from spotify.objects.audio_file import AudioFile
from spotify.objects.copyright import Copyright
from spotify.objects.disc import Disc
from spotify.objects.external_id import ExternalId
from spotify.objects.image import Image
from spotify.objects.image_group import ImageGroup
from spotify.objects.playlist import Playlist, PlaylistItem
from spotify.objects.restriction import Restriction
from spotify.objects.top_tracks import TopTracks
from spotify.objects.track import Track
from spotify.objects.user import User

import logging
import sys

log = logging.getLogger(__name__)


ALL = [
    'Album',
    'AlbumGroup',
    'Artist',
    'AudioFile',
    'Copyright',
    'Disc',
    'ExternalId',
    'Image',
    'ImageGroup',
    'Playlist',
    'PlaylistItem',
    'Restriction',
    'TopTracks',
    'Track',
    'User'
]

NAME_MAP = dict([
    (key, getattr(sys.modules[__name__], key))
    for key in ALL
])


def legacy_map(map, cls):
    tag = getattr(cls, '__node__', None)

    if not tag:
        return

    map[tag] = cls


def discover():
    result = {'XML': {}}

    for cls in NAME_MAP.values():
        class_parsers(cls, result)

    return result


def class_parsers(cls, result=None, flat=False):
    cls_name = cls.__name__

    if result is None:
        result = {'XML': {}}

    if not hasattr(cls, '__parsers__'):
        log.warn('Missing "__parsers__" attribute on %s', cls)

        if flat:
            result['XML'] = cls
        else:
            legacy_map(result['XML'], cls)
    else:
        for parser in cls.__parsers__():
            name = parser.__name__

            if name not in result:
                result[name] = {}

            if flat:
                result[name] = parser
            else:
                tag = getattr(parser, '__tag__', cls_name)
                result[name][tag] = parser

    return result


class Parser(object):
    MercuryJSON = 'MercuryJSON'
    XML = 'XML'
    Tunigo = 'Tunigo'

    NAMES = NAME_MAP
    TYPES = discover()

    @classmethod
    def get(cls, data_type, tag):
        if data_type not in cls.TYPES:
            raise ValueError('Unknown data type "%s"' % data_type)

        types = cls.TYPES

        if tag in cls.NAMES:
            types = class_parsers(cls.NAMES[tag], flat=True)
            return types.get(data_type)

        # Look for tag in type map
        if tag in types[data_type]:
            return types[data_type][tag]

        log.warn('Unknown tag "%s" for data type "%s"', tag, data_type)
        return None

    @classmethod
    def parse(cls, sp, data_type, tag, data):
        #log.debug('parse - data_type: %s, tag: %s, data: %s', repr(data_type), repr(tag), repr(data))
        parser = cls.get(data_type, tag)

        if hasattr(parser, 'parse'):
            return parser.parse(sp, data, cls)

        log.warn('Using an old-style parser %s', parser)

        if data_type == 'XML':
            if type(data) is dict:
                return parser.from_node_dict(sp, data, cls)

            return parser.from_node(sp, data, cls)

        log.warn('Unknown old-style data type')
        return None
