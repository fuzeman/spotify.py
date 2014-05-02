from spotify.objects.album import Album
from spotify.objects.artist import Artist
from spotify.objects.audio_file import AudioFile
from spotify.objects.copyright import Copyright
from spotify.objects.disc import Disc
from spotify.objects.external_id import ExternalId
from spotify.objects.image import Image
from spotify.objects.image_group import ImageGroup
from spotify.objects.track import Track
from spotify.objects.restriction import Restriction
from spotify.objects.user import User

import sys


ALL = [
    'Album',
    'Artist',
    'AudioFile',
    'Copyright',
    'Disc',
    'ExternalId',
    'Image',
    'ImageGroup',
    'Restriction',
    'Track',
    'User'
]

MAP = dict([(key, getattr(sys.modules[__name__], key)) for key in ALL])
