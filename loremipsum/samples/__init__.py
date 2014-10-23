"""
"""

from loremipsum import generator
from loremipsum.serialization.mediums import pkg_resources_

loremipsum = generator.Generator(pkg_resources_.load('loremipsum', package_name='loremipsum'))

__all__ = ['loremipsum']
