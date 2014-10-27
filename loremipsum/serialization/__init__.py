"""
This is merely a namespace package for serialization mediums and protocols
plugins used by :py:meth:`Generator.load` and :py:meth`Generator.dump`.
"""

from loremipsum.serialization import content_encodings
from loremipsum.serialization import content_types
from loremipsum.serialization import schemes

__all__ = ['schemes', 'content_types', 'content_encodings']
