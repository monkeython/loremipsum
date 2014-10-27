"""
This is not a real scheme.
"""
import os

import pkg_resources as pkg


def load(class_, url, **args):
    package, sample = url.netloc, url.path
    args = {
        'sample': None,
        'lexicon': None,
        'word_delimiters': None,
        'sentence_delimiters': None}
    for name in args:
        path = os.path.join('samples', sample, name + '.txt')
        args[name] = pkg.resource_string(package, path).decode('utf-8')

    return class_(**args)


def dump(*args, **kwargs):
    raise NotImplementedError('Cannot dump sample into package resources.')
