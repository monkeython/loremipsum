"""Handle file URL"""

import mimetypes
import os

from loremipsum.serialization import content_encodings
from loremipsum.serialization import content_types


def load(class_, url, **args):
    """Loads the sample from a file URL."""
    if url.netloc and url.netloc != 'localhost':
        raise NotImplementedError('Cannot load from a location other than'
                                  ' localhot: {}'.format(url.netloc))
    if os.path.isdir(url.path):
        args = {
            'sample': None,
            'lexicon': None,
            'word_delimiters': None,
            'sentence_delimiters': None}
        for arg_name in args:
            with open(os.path.join(url.path, arg_name + '.txt'), 'rb') as arg:
                args[arg_name] = arg.read().decode('utf-8')
        return class_(**args)
    else:
        with open(url.path, 'rb') as file_:
            content = file_.read()
        mimetype, enconding = mimetypes.guess_type(url.path)
        if enconding:
            content = content_encodings.get(enconding).decode(content)
        return class_(**content_types.get(mimetype).parse(content))


def dump(sample, url, **args):
    """Dunps the sample into a file URL."""
    if url.netloc and url.netloc != 'localhost':
        raise NotImplementedError('Cannot dump to a location other than'
                                  ' localhot: {}'.format(url.netloc))
    prefix, extension = os.path.splitext(url.path)
    if not extension:
        files = {
            'sample': sample['text'],
            'lexicon': sample['lexicon'],
            'word_delimiters': sample['word_delimiters'],
            'sentence_delimiters': sample['sentence_delimiters']}
        for filename in files:
            with open(os.path.join(prefix, filename + '.txt'), 'wb') as file_:
                file_.write(files.get(filename))
    else:
        mimetype, enconding = mimetypes.guess_type(url.path)
        content = content_types.get(mimetype).format(sample.frozen())
        if enconding:
            content = content_encodings.get(enconding).encode(content)
        with open(url.path, 'wb') as file_:
            file_.write(content)
