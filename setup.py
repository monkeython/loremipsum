from setuptools import setup
import sys
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
    'url': '%s/html' % url,
    'description': "A Lorem Ipsum text generator",
    'long_description': long_description,
    'download_url': '%s/eggs/%s-%s-py%s.%s.egg' % \
        ((url, name, module.__version__) + python_version),
    'classifiers': module.__classifiers__,
    'py_modules': [name],
    'requires': ['setuptools'],
    'include_package_data': True,
    'exclude_package_data': {name: ["*.rst", "docs", "tests"]},
    'test_suite': 'tests.suite' }

if __name__ == '__main__':
    setup(**egg)

