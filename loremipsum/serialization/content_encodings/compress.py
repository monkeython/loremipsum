"""Handle compress encoding/decoding."""

import zlib

LEVEL = 6


def decode(binary):
    """Decode (uncompress) binary data."""
    return zlib.decompress(binary)


def encode(binary):
    """Encode (compress) binary data."""
    return zlib.compress(binary, LEVEL)
