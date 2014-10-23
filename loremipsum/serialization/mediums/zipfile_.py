"""
"""

import os
import zipfile

PREFIX=None

def load(name, **args):
    """
    """

    prefix = args.get('prefix', PREFIX)
    state = {
        'sample': None, 
        'lexicon': None, 
        'word_delimiters': None, 
        'sentence_delimiters': None}
    path = os.path.join(prefix, name + '.zip')
    with zipfile.ZipFile(path) as medium:
        for arg_name in state:
            state[arg_name] = medium.read(arg_name + '.txt').decode('utf-8')

    return {'args': state}

def dump(name, frozen, **args):
    """
    """

    prefix = args.get('prefix', PREFIX)
    path = os.path.join(prefix, name + '.zip')
    state = dict(frozen)
    state['text'] = dict(state['text'])
    state['word'] = dict(state['word'])
    state['sentence'] = dict(state['sentence'])
    files = {
        'sample': '\n\n'.join(state['text']['sample']),
        'lexicon': '\n'.join(state['text']['lexicon']),
        'word_delimiters': state['word']['delimiters'],
        'sentence_delimiters': state['sentence']['delimiters']}
    with zipfile.ZipFile(path, 'w') as medium:
        for name, content in files.iteritems():
            medium.writestr(name + '.txt', bytes(content))
