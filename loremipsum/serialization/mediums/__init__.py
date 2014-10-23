"""
This package collects the medium plugins for the serialization methods of
:py:class:`Generator`. Medium plugins are regular python modules which exposes
a load and a dump function.
"""

from loremipsum.serialization.mediums import directory
from loremipsum.serialization.mediums import file_
from loremipsum.serialization.mediums import pkg_resources_
from loremipsum.serialization.mediums import zipfile_

__all__ = [
    'directory',
    'file_',
    'pkg_resources_',
    'zipfile_']
