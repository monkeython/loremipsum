"""Handle serialization of a frozen sample from/to a ZIP file."""
import io
import zipfile


def parse(binary):
    """Turns a ZIP file into a frozen sample."""
    binary = io.BytesIO(binary)
    args = {
        'text': None,
        'lexicon': None,
        'word_delimiters': None,
        'sentence_delimiters': None}
    with zipfile.ZipFile(binary, 'r') as zip_:
        for arg_name in args:
            args[arg_name] = zip_.read(arg_name + '.txt').decode('UTF-8')
    return args


def format(frozen):
    """Truns a frozen sample into a ZIP file."""
    arg_names = ('text', 'lexicon', 'word_delimiters', 'sentence_delimiters')
    args = dict(frozen)
    binary = io.BytesIO()
    with zipfile.ZipFile(binary, 'w') as zip_:
        for arg_name in arg_names:
            zip_.writestr(arg_name + '.txt', args.get(arg_name).encode('UTF-8'))
    binary.seek(0)
    return binary.read()
