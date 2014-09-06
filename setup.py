import sys
from setuptools import setup
import os

wd = os.path.dirname(os.path.abspath(__file__))
os.chdir(wd)
sys.path.insert(1, wd)

name = 'loremipsum'
package = __import__(name)
author, email = package.__author__.rsplit(' ', 1)

with open('README.rst', 'r') as readme:
    description = readme.readline().strip()
    long_description = ''.join((description, readme.read()))

url = 'http://projects.monkeython.com/%s' % name

egg = {
    'name': name,
    'version': package.__version__,
    'author': author,
    'author_email': email.strip('<>'),
    'url': url,
    'description': description,
    'long_description': long_description,
    'classifiers': package.__classifiers__,
    'keywords': package.__keywords__,
    'setup_requires': ['distribute'],
    'install_requires': ['distribute'],
    'packages': [name],
    'include_package_data': True,
    'test_suite': 'tests.suite'
}

if __name__ == '__main__':
    setup(**egg)
