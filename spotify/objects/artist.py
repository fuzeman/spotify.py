from spotify.core.uri import Uri
from spotify.objects.base import Descriptor, PropertyProxy
from spotify.proto import metadata_pb2


class Artist(Descriptor):
    __protobuf__ = metadata_pb2.Artist
    __node__ = 'artist'

    gid = PropertyProxy
    uri = PropertyProxy('gid', func=lambda gid: Uri.from_gid('artist', gid))
    name = PropertyProxy

    popularity = PropertyProxy
    top_track = PropertyProxy

    album_group = PropertyProxy
    single_group = PropertyProxy
    compilation_group = PropertyProxy
    appears_on_group = PropertyProxy

    genres = PropertyProxy('genre')
    external_ids = PropertyProxy('external_id', 'ExternalId')

    portraits = PropertyProxy('portrait')
    biographies = PropertyProxy('biography')

    activity_periods = PropertyProxy('activity_period')
    restrictions = PropertyProxy('restriction')
    related = PropertyProxy('related')

    is_portrait_album_cover = PropertyProxy('is_portrait_album_cover')
    portrait_group = PropertyProxy('portrait_group')

    @classmethod
    def from_dict(cls, sp, data, types):
        uri = Uri.from_id('artist', data.get('id'))

        return Artist(sp).dict_update({
            'gid': uri.to_gid(),
            'uri': uri,
            'name': data.get('name'),
            # TODO portraits
            'popularity': float(data.get('popularity')) if data.get('popularity') else None,
            'restriction': data.get('restrictions')
        })
