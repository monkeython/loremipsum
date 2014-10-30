"""Handle gzip encoding/decoding."""

import gzip
import io

LEVEL = 9


def decode(binary):
    """Decode (gunzip) binary data."""
    encoded = io.BytesIO(binary)
    with gzip.GzipFile(mode='rb', fileobj=encoded) as file_:
        decoded = file_.read()
    return decoded


def encode(binary):
    """Encode (gzip) binary data."""
    encoded = io.BytesIO()
    gzip_file = dict(mode='wb', fileobj=encoded, compresslevel=LEVEL)
    with gzip.GzipFile(**gzip_file) as file_:
        file_.write(binary)
    encoded.seek(0)
    return encoded.read()
