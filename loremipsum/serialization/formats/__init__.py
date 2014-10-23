"""
This package collects the protocols plugins for the serialization methods of
:py:class:`Generator`. Protocols plugins are regular python modules which
exposes a load and a dump function.
"""

from loremipsum.serialization.protocols import pickle_

__all__ = ['pickle_']
