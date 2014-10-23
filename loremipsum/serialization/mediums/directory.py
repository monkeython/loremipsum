import os

PREFIX = None


def load(class_, name, **args):
    prefix = args.get('prefix', PREFIX)
    state = {
        'sample': None,
        'lexicon': None,
        'word_delimiters': None,
        'sentence_delimiters': None}
    for arg_name in state:
        path = os.path.join(prefix, name, arg_name + '.txt')
        with open(path, 'rb') as arg:
            state[arg_name] = arg.read().decode('utf-8')

    return class_(**args)


def dump(sample, name, **args):
    prefix = args.get('prefix', PREFIX)
    directory = os.path.join(prefix, name)
    if not os.path.exists(directory):
        os.mkdir(directory, 0755)
    names = ['sample', 'lexicon', 'word_delimiters', 'sentence_delimiters']
    files = dict(zip(names, sample.row()))
    for name in names:
        txt_file = os.path.join(directory, name + '.txt')
        with open(txt_file, 'wb') as medium:
            medium.write(bytes(files.get(name)))
