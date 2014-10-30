"""Handle serialization of a frozen sample from/to a tar file."""
import calendar
import datetime
import io
import tarfile


def parse(binary):
    """Turns a TAR file into a frozen sample."""
    binary = io.BytesIO(binary)
    args = {
        'text': None,
        'lexicon': None,
        'word_delimiters': None,
        'sentence_delimiters': None}
    with tarfile.TarFile(fileobj=binary, mode='r') as tar:
        for arg_name in args:
            member = tar.extractfile(arg_name + '.txt')
            args[arg_name] = member.read().decode('utf-8')
    return args


def format(frozen):
    """Truns a frozen sample into a TAR file."""
    frozen = dict(frozen)
    args = ('text', 'lexicon', 'word_delimiters', 'sentence_delimiters')
    binary = io.BytesIO()
    with tarfile.TarFile(fileobj=binary, mode='w') as tar:
        now = calendar.timegm(datetime.datetime.utcnow().timetuple())
        for arg_name in args:
            content = frozen.get(arg_name)
            member_content = io.BytesIO(content.encode('UTF-8'))
            member_info = tarfile.TarInfo(arg_name + '.txt')
            member_info.size = len(content)
            member_info.mode = 0o644
            member_info.mtime = now
            tar.addfile(member_info, member_content)
    binary.seek(0)
    return binary.read()
