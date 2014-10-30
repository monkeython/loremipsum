"""Handle file URL"""

import mimetypes
import os

from loremipsum.serialization import content_encodings
from loremipsum.serialization import content_types


def load(class_, url, **args):
    """Loads the sample from a file URL."""
    if os.path.isdir(url.path):
        files = {
            'text': None,
            'lexicon': None,
            'word_delimiters': None,
            'sentence_delimiters': None}
        for filename in files:
            with open(os.path.join(url.path, filename + '.txt'), 'rb') as txt:
                files[filename] = txt.read().decode('UTF-8')
        return class_(**files)
    else:
        with open(url.path, 'rb') as file_:
            content = file_.read()
        mimetype, encoding = mimetypes.guess_type(url.path)
        content_encoding = args.get('content_encoding', encoding)
        content_type = args.get('content_type', mimetype)
        if content_encoding:
            content = content_encodings.get(content_encoding).decode(content)
        frozen = content_types.get(content_type).parse(content)
        return class_(**frozen)


def dump(sample, url, **args):
    """Dunps the sample into a file URL."""
    prefix, extension = os.path.splitext(url.path)
    if not extension:
        if not os.path.exists(url.path):
            os.mkdir(url.path)
        files = {
            'text': sample['text'],
            'lexicon': sample['lexicon'],
            'word_delimiters': sample['word_delimiters'],
            'sentence_delimiters': sample['sentence_delimiters']}
        for filename in files:
            with open(os.path.join(prefix, filename + '.txt'), 'wb') as file_:
                file_.write(files.get(filename).encode('UTF-8'))
    else:
        mimetype, encoding = mimetypes.guess_type(url.path)
        content_encoding = args.get('content_encoding', encoding)
        content_type = args.get('content_type', mimetype)
        content = content_types.get(content_type).format(sample.frozen())
        if content_encoding:
            content = content_encodings.get(content_encoding).encode(content)
        with open(url.path, 'wb') as file_:
            file_.write(content)


def remove(url, **args):
    """Remove the sample from a file URL."""
    if os.path.isdir(url.path):
        for filename in os.listdir(url.path):
            os.remove(os.path.join(url.path, filename))
        os.rmdir(url.path)
    else:
        os.remove(url.path)
