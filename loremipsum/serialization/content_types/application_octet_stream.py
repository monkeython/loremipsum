"""Handle PICKLE formatting/parsing of a frozen sample."""

import mimetypes
import pickle

mimetypes.add_type('application/octet-stream', '.pickle')


def parse(binary):
    """Turns a PICKLE structure into a frozen sample."""
    return dict(frozen=pickle.loads(binary))


def format(frozen):
    """Truns a frozen sample into a PICKLE structure."""
    return pickle.dumps(frozen)
