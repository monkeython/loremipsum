import sys
from setuptools import setup
import os

wd = os.path.dirname(os.path.abspath(__file__))
os.chdir(wd)
sys.path.insert(1, wd)

name = 'loremipsum'
module = __import__(name)
author, email = module.__author__.rsplit(' ', 1)

with open(os.path.join(wd, 'README.rst'),'r') as readme:
    long_description = readme.read()

python_version = sys.version_info[:2]
url = 'http://projects.monkeython.com/%s' % name

egg = {
    'name': name,
    'version': module.__version__,
    'author': author,
    'author_email': email.strip('<>'),
    'url': url,
    'description': "A Lorem Ipsum text generator",
    'long_description': long_description,
    'classifiers': module.__classifiers__,
    'keywords': ['lorem', 'ipsum', 'text', 'generator'],
    'py_modules': [name],
    'requires': ['setuptools'],
    'include_package_data': True,
    'exclude_package_data': {name:
        ['.gitignore', '*.rst', 'docs', 'tests', 'examples']},
    'test_suite': 'tests.suite' }

if __name__ == '__main__':
    setup(**egg)

