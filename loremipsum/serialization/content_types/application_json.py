"""Handle JSON formatting/parsing of a frozen sample."""

import json


def parse(binary):
    """Turns a JSON structure into a frozen sample."""
    return dict(frozen=json.loads(binary.decode('UTF-8')))


def format(frozen):
    """Truns a frozen sample into a JSON structure."""
    return json.dumps(frozen).encode('UTF-8')
