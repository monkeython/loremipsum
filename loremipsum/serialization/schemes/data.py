"""Handle the data URI"""

import base64
import re
import urllib

from loremipsum.serialization import content_types


def load(class_, url, **args):
    """Loads the sample from a data URI."""
    info_re = '(?P<mediatype>[^/]+/[^;]+(;[^=]+=[^;]+)*)?(?P<base64>;base64)?'
    info, data = url.path.split(',')
    info = re.match(info_re, info).groupdict()
    mediatype = info['mediatype'].setdefault('text/plain;charset=US-ASCII')
    if ';' in mediatype:
        mimetype, params = mediatype.split(';', 1)
        params = [p.strip().split('=') for p in params.split(';')]
        params = dict((k.strip(), v.strip()) for k, v in params)
    else:
        mimetype, params = mediatype, dict()
    data = base64.b64decode(data) if info['base64'] else urllib.unquote(data)
    return class_(**content_types.get(mimetype).parse(data, **params))


def dump(sample, url, **args):
    """Writes a sample to a data URI."""
    pass
