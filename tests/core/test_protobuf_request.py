from spotify.core.protobuf_request import ProtobufRequest
from spotify.objects import Album

TEST_REQUEST = ProtobufRequest('sp/hm_b64', [
    {
        'method': 'GET',
        'uri': 'hm://metadata/track/9adbdff7a4f14cd89a1a8a566a92c366'
    }
], {
    'vnd.spotify/metadata-album': Album
}, {
    'method': 'GET',
    'uri': 'hm://metadata/albums'
})


def test_encode():
    encoded = TEST_REQUEST.build(0)
    print 'encoded as: %s' % repr(encoded)

    assert encoded == {
        'name': 'sp/hm_b64',
        'id': '0',
        'args': [0, 'CjRobTovL21ldGFkYXRhL3RyYWNrLzlhZGJkZmY3YTRmMTRjZDg5YTFhOGE1NjZhOTJjMzY2EgAaA0dFVCoA']
    }


def test_decode():
    TEST_REQUEST.process({
        'id': '0',
        'result': [
            u'CjRobTovL21ldGFkYXRhL2FsYnVtL2Y1ZjNlMzExMzVkNTRhODViNmYyODU2MWMyNTU4NDU0Ehp2bmQuc3BvdGlmeS9tZXRhZGF0YS1hbGJ1bSCQAzIYCgpNRC1WZXJzaW9uEgoxMzk4ODY0OTk0Mg8KBk1DLVRUTBIFNjMyMTQyGQoPTUMtQ2FjaGUtUG9saWN5EgZwdWJsaWMyDwoHTUMtRVRhZxIE7P/4Vw==',
            u'ChD18+MRNdVKhbbyhWHCVYRUEgpBbGl2ZSAyMDA3Gh0KEJNSYW4bakpfvodkoWSLUawSCURhZnQgUHVuayABKhFQYXJsb3Bob25lIEZyYW5jZTIHCK4fEBYYIDiSAUIFRGFuY2VCBUhvdXNlSh4KFKholbY8Ky7DfAdD0GX4HxF3JvuYEAAY2AQg2ARKHgoUT3b53a6RU3+jpXEZQfu4yqa8i2YQARiAASCAAUoeChRimPqMEkXFmC4Ly3M/LOoKyP2sSRACGIAKIIAKUhQKA3VwYxINNTA5OTk1MTE2NTg1N1qGAggCGhIKEKwqgGZ/50Y9m1w5uEVMnvUaEgoQmtvf96TxTNiaGopWapLDZhoSChA2IXL0ShFBlI7uqLGMItO2GhIKEG7MBkgELEVXsiSTj/4EOEMaEgoQwLFR1K61Rj+CTfF49y90/xoSChB9RLxtaVlA2pAo3xsTOo9gGhIKEMPbN7mYbkQVtva0OWEKbV8aEgoQN6evqExkTrCt0DNLchrICxoSChAOqrIGgOtJZL3ARAgXs6nNGhIKEHDXg3zgRU+0vWmThkPvgVIaEgoQv0ep8YeNQ6yqPqmTOaX4kxoSChABJMuDV8lGgL7Iyw3t/mGtGhIKELIWJD5IREybjN8tuqMDnjJqbAgBEmgyMDA3IERhZnQgbGlmZSBsaW1pdGVkIHVuZGVyIGV4Y2x1c2l2ZSBsaWNlbnNlIHRvIFBhcmxvcGhvbmUgTXVzaWMgYSBkaXZpc2lvbiBvZiBQYXJsb3Bob25lIE11c2ljIEZyYW5jZWpsCAASaDIwMDcgRGFmdCBsaWZlIGxpbWl0ZWQgdW5kZXIgZXhjbHVzaXZlIGxpY2Vuc2UgdG8gUGFybG9waG9uZSBNdXNpYyBhIGRpdmlzaW9uIG9mIFBhcmxvcGhvbmUgTXVzaWMgRnJhbmNlciQIAAgBCAMaHEFUQlFDSENOQ1VDV0RFR0JJUklUSlBLUFNYU1lyBAgEEgCKAWAKHgoUqGiVtjwrLsN8B0PQZfgfEXcm+5gQABjYBCDYBAoeChRPdvndrpFTf6OlcRlB+7jKpryLZhABGIABIIABCh4KFGKY+owSRcWYLgvLcz8s6grI/axJEAIYgAoggAqSAQpBbGl2ZSAyMDA3'
        ]
    })

    assert False
