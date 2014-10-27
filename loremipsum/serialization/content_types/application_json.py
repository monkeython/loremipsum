"""Handle JSON formatting/parsing of a frozen sample."""

import json


def parse(binary):
    """Turns a JSON structure into a frozen sample."""
    frozen = dict(json.loads(binary))
    frozen['chains'] = dict((tuple(k), v) for k, v in frozen['chains'].items())
    for chain, values in frozen['chains'].items():
        frozen['chains'][chain] = [tuple(v) for v in values]
    frozen['starts'] = [tuple(s) for s in frozen['starts']]
    return dict(frozen=tuple(frozen))


def format(frozen):
    """Truns a frozen sample into a JSON structure."""
    return json.dumps(frozen)
