from spotify.core.uri import Uri
from spotify.objects import Artist, Album, Track, Playlist

from lxml import etree
import logging
import traceback

log = logging.getLogger(__name__)


class SearchResponse(object):
    media_types = [
        'artists',
        'albums',
        'tracks',
        'playlists'
    ]

    def __init__(self):
        self.artists = []
        self.artists_total = None

        self.albums = []
        self.albums_total = None

        self.tracks = []
        self.tracks_total = None

        self.playlists = []
        self.playlists_total = None

    @classmethod
    def parse(cls, sp, data):
        xml = etree.fromstring(data['result'].encode('utf-8'))

        obj = cls()

        for m in cls.media_types:
            cls.parse_media(sp, xml, obj, m)

        return obj

    @classmethod
    def parse_media(cls, sp, xml, obj, key):
        # total-<media>
        setattr(obj, '%s_total' % key, xml.find('total-%s' % key).text)

        # <media>
        parse_func = getattr(cls, 'parse_%s' % key.rstrip('s'), None)

        if parse_func is None:
            return

        items = getattr(obj, key)

        for node in xml.find(key):
            try:
                items.append(parse_func(sp, node))
            except Exception, ex:
                log.warn('Unable to parse node %s (%s) - %s', node, ex, traceback.format_exc())

    @classmethod
    def parse_artist(cls, sp, node):
        uri = Uri.from_id('artist', node.find('id').text)

        return Artist(sp).dict_update({
            'gid': uri.to_gid(),
            'uri': uri,
            'name': node.find('name').text,

            'popularity': float(node.find('popularity').text),

            # TODO portraits
            # TODO restrictions
        })

    @classmethod
    def parse_album(cls, sp, node):
        uri = Uri.from_id('album', node.find('id').text)

        return Album(sp).dict_update({
            'gid': uri.to_gid(),
            'uri': uri,
            'name': node.find('name').text,

            # TODO artists

            'popularity': float(node.find('popularity').text),

            # TODO covers
            # TODO restrictions
            # TODO external_ids
        })

    @classmethod
    def parse_track(cls, sp, node):
        uri = Uri.from_id('track', node.find('id').text)

        return Track(sp).dict_update({
            'gid': uri.to_gid(),
            'uri': uri,
            'name': node.find('title').text,

            # TODO albums
            # TODO albums - covers
            # TODO albums - year

            # TODO artists

            'number': int(node.find('track-number').text),
            # TODO disc_number ?
            'duration': int(node.find('length').text),

            'popularity': float(node.find('popularity').text),

            # TODO external_ids
            # TODO restrictions
            # TODO files
        })

    @classmethod
    def parse_playlist(cls, sp, node):
        uri = Uri.from_uri(node.find('uri').text)

        return Playlist(sp).dict_update({
            'uri': uri,
            'name': node.find('name').text,

            # TODO image
        })
