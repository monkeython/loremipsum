"""
python setup.py bdist_egg
"""
import sys
from setuptools import setup
import os

WD = os.path.dirname(os.path.abspath(__file__))
os.chdir(WD)
sys.path.insert(1, WD)

NAME = 'loremipsum'
PACKAGE = __import__(NAME)
AUTHOR, EMAIL = PACKAGE.__author__.rsplit(' ', 1)

with open('README.rst', 'r') as README:
    DESCRIPTION = README.readline().strip()
    LONG_DESCRIPTION = ''.join((DESCRIPTION, README.read()))

URL = 'http://projects.monkeython.com/%s' % NAME

EGG = {
    'name': NAME,
    'version': PACKAGE.__version__,
    'author': AUTHOR,
    'author_email': EMAIL.strip('<>'),
    'url': URL,
    'description': DESCRIPTION,
    'long_description': LONG_DESCRIPTION,
    'classifiers': PACKAGE.__classifiers__,
    'keywords': PACKAGE.__keywords__,
    'setup_requires': ['distribute'],
    'install_requires': ['distribute'],
    'packages': [NAME],
    'include_package_data': True,
    'test_suite': 'tests.suite'
}

if __name__ == '__main__':
    setup(**EGG)
