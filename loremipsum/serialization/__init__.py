"""
This subpackage provides the components needed to serialize a
:py:class:`loremipsum.generator.Sample`.

There are 3 components:

:schemes:
    Handle the sample URL: fetch, store, remove.
:content_types:
    Handle the ``Sample`` serialization formats or protocol.
:content_encodings:
    Handle the serialized ``Sample`` compression/decompression.

All components are pluggable packages: see also :py:mod:`loremipsum.plugs`.
"""

from loremipsum.serialization import content_encodings
from loremipsum.serialization import content_types
from loremipsum.serialization import schemes

__all__ = ['schemes', 'content_types', 'content_encodings']
