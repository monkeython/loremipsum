import os

import pkg_resources as pkg
from loremipsum import generator

PACKAGE_NAME = __name__


def load(class_, name, **args):
    package_name = args.get('package_name', PACKAGE_NAME)
    args = {
        'sample': None,
        'lexicon': None,
        'word_delimiters': None,
        'sentence_delimiters': None}
    for arg_name in args:
        path = os.path.join('generators', name, arg_name + '.txt')
        args[arg_name] = pkg.resource_string(package_name, path).decode('utf-8')

    return class_(**args)


def dump(*args, **kwargs):
    raise NotImplementedError('Cannot dump generator into package resources.')
