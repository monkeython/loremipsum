"""Handle serialization of a frozen sample from/to a ZIP file."""

import StringIO
import zipfile


def parse(binary):
    """Turns a ZIP file into a frozen sample."""
    binary = StringIO.StringIO(binary)
    args = {
        'sample': None,
        'lexicon': None,
        'word_delimiters': None,
        'sentence_delimiters': None}
    with zipfile.Zipfile(binary, 'rb') as zip_:
        for arg_name in args:
            args[arg_name] = zip_.read(arg_name + '.txt').decode('utf-8')
    return dict(args=args)


def format(frozen):
    """Truns a frozen sample into a ZIP file."""
    arg_names = ('sample', 'lexicon', 'word_delimiters', 'sentence_delimiters')
    args = dict(frozen)
    binary = StringIO.StringIO()
    with zipfile.Zipfile(binary, 'wb') as zip_:
        for arg_name in arg_names:
            zip_.writestr(arg_name + '.txt', args.get(arg_name))
    binary.seek(0)
    return binary.read()
