from spotify.client import Spotify
from spotify.objects import Album
from spotify.objects.parser import MAP

import base64
import logging
import os


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    sp = Spotify()

    data = u'ChD18+MRNdVKhbbyhWHCVYRUEgpBbGl2ZSAyMDA3Gh0KEJNSYW4bakpfvodkoWSLUawSCURhZnQgUHVuayABKhFQYXJsb3Bob25lIEZyYW5jZTIHCK4fEBYYIDiSAUIFRGFuY2VCBUhvdXNlSh4KFKholbY8Ky7DfAdD0GX4HxF3JvuYEAAY2AQg2ARKHgoUT3b53a6RU3+jpXEZQfu4yqa8i2YQARiAASCAAUoeChRimPqMEkXFmC4Ly3M/LOoKyP2sSRACGIAKIIAKUhQKA3VwYxINNTA5OTk1MTE2NTg1N1qGAggCGhIKEKwqgGZ/50Y9m1w5uEVMnvUaEgoQmtvf96TxTNiaGopWapLDZhoSChA2IXL0ShFBlI7uqLGMItO2GhIKEG7MBkgELEVXsiSTj/4EOEMaEgoQwLFR1K61Rj+CTfF49y90/xoSChB9RLxtaVlA2pAo3xsTOo9gGhIKEMPbN7mYbkQVtva0OWEKbV8aEgoQN6evqExkTrCt0DNLchrICxoSChAOqrIGgOtJZL3ARAgXs6nNGhIKEHDXg3zgRU+0vWmThkPvgVIaEgoQv0ep8YeNQ6yqPqmTOaX4kxoSChABJMuDV8lGgL7Iyw3t/mGtGhIKELIWJD5IREybjN8tuqMDnjJqbAgBEmgyMDA3IERhZnQgbGlmZSBsaW1pdGVkIHVuZGVyIGV4Y2x1c2l2ZSBsaWNlbnNlIHRvIFBhcmxvcGhvbmUgTXVzaWMgYSBkaXZpc2lvbiBvZiBQYXJsb3Bob25lIE11c2ljIEZyYW5jZWpsCAASaDIwMDcgRGFmdCBsaWZlIGxpbWl0ZWQgdW5kZXIgZXhjbHVzaXZlIGxpY2Vuc2UgdG8gUGFybG9waG9uZSBNdXNpYyBhIGRpdmlzaW9uIG9mIFBhcmxvcGhvbmUgTXVzaWMgRnJhbmNlciQIAAgBCAMaHEFUQlFDSENOQ1VDV0RFR0JJUklUSlBLUFNYU1lyBAgEEgCKAWAKHgoUqGiVtjwrLsN8B0PQZfgfEXcm+5gQABjYBCDYBAoeChRPdvndrpFTf6OlcRlB+7jKpryLZhABGIABIIABCh4KFGKY+owSRcWYLgvLcz8s6grI/axJEAIYgAoggAqSAQpBbGl2ZSAyMDA3'

    al = Album.parse(base64.b64decode(data), MAP)

    print al.name
    print al.artists[0].name

    for track in al.discs[0].tracks:
        print repr(track.gid)

    # @sp.login(os.environ['USERNAME'], os.environ['PASSWORD'])
    # def on_login():
    #     print 'logged on'
    #
    #     @sp.metadata('spotify:album:7u6zL7kqpgLPISZYXNTgYk')
    #     def on_metadata(album):
    #         print 'album.name', album.artist

    while True:
        raw_input()
