"""Handle bz2 encoding/decoding."""

import bz2

LEVEL = 6


def decode(binary):
    """Decode (bunzip2) binary data."""
    return bz2.decompress(binary)


def encode(binary):
    """Encode (bzip2) binary data."""
    return bz2.compress(binary, LEVEL)
