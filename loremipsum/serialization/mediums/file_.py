"""
"""

from loremipsum.serialization import protocols

import os

PREFIX=None

def load(class_, name, **args):
    """
    """

    protocol_name = args.get('serialization_protocol')
    protocol = protocols.get(protocol_name, protocols.DEFAULT)
    prefix = args.get('prefix', PREFIX)
    extension = args.get('extension', protocol.EXTENSION)
    path = os.path.join(prefix, '{}.{}'.format(name, extension))
    with open(path, 'rb') as medium:
        return class_(protocol.load(medium.read()))

def dump(sample, name, **args):
    """
    """

    protocol = args.get('serialization_protocol', protocols.DEFAULT)
    prefix = args.get('prefix', PREFIX)
    extension = args.get('extension', protocol.EXTENSION)
    path = os.path.join(prefix, '{}.{}'.format(name, extension))
    with open(path, 'wb') as medium:
        medium.write(bytes(protocol.dump(sample)))
