"""Handle serialization of a frozen sample from/to a tar file."""

import StringIO
import tarfile


def parse(binary):
    """Turns a TAR file into a frozen sample."""
    binary = StringIO.StringIO(binary)
    args = {
        'sample': None,
        'lexicon': None,
        'word_delimiters': None,
        'sentence_delimiters': None}
    with tarfile.TarFile(fileobj=binary, mode='rb') as tar:
        for arg_name in args:
            member = tar.extractfile(arg_name + '.txt')
            args[arg_name] = member.read().decode('utf-8')
    return dict(args=args)


def format(frozen):
    """Truns a frozen sample into a TAR file."""
    frozen = dict(frozen)
    args = ('sample', 'lexicon', 'word_delimiters', 'sentence_delimiters')
    binary = StringIO.StringIO()
    with tarfile.TarFile(fileobj=binary, mode='wb') as tar:
        for arg_name in args:
            member_info = tarfile.TarInfo(arg_name + '.txt')
            member_content = StringIO.StringIO(frozen.get(arg_name))
            tar.addfile(member_info, member_content)
    binary.seek(0)
    return binary.read()
