"""
This is merely a namespace package for serialization mediums and protocols
plugins used by :py:meth:`Generator.load` and :py:meth`Generator.dump`.
"""

from loremipsum.serialization import mediums
from loremipsum.serialization import protocols

__all__ = ['mediums', 'protocols']
