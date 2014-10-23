"""
"""

import sys
import pickle

EXTENSION = 'pickle'
PROTOCOL_VERSION = pickle.HIGHEST_PROTOCOL
FIX_IMPORTS = True
ERRORS = 'strict'

def load(binary, **args):
    """
    """
    if sys.version_info[0] == 2:
        state = pickle.loads(binary)
    else:
        errors = args.get('errors', ERRORS)
        fix_imports = args.get('fix_imports', FIX_IMPORTS)
        protocol = args.get('protocol_version', PROTOCOL_VERSION)
        state = pickle.loads(binary, fix_imports=fix_imports, encoding='utf-8', errors=errors)
    return state


def dump(state, **args):
    """
    """
    protocol = args.get('protocol_version', PROTOCOL_VERSION)
    if sys.version_info[0] == 2:
        serial = pickle.dumps(state, protocol=protocol)
    else:
        fix_imports = args.get('fix_imports', FIX_IMPORTS)
        serial = pickle.dumps(state, fix_imports=fix_imports, protocol=protocol)
    return serial
