"""Handle gzip encoding/decoding."""

import gzip
import StringIO

LEVEL = 9


def decode(binary):
    """Decode (gunzip) binary data."""
    encoded = StringIO.StringIO(binary)
    with gzip.GzipFile(mode='rb', fileobj=encoded) as compressed:
        decoded = compressed.read()
    return decoded


def encode(binary):
    """Encode (gzip) binary data."""
    encoded = StringIO.StringIO()
    args = dict(mode='wb', fileobj=encoded, compressionelevel=LEVEL)
    with gzip.GzipFile(**args) as compressed:
        compressed.write(binary)
    encoded.seek(0)
    return encoded.read()
