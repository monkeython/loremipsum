"""
This utility module is used to setup ``loremipsum`` sub-packages/module for
plugins. A plugs ready package has the following attributes/functions available:

.. py:attribute:: package.DEFAULT

   The package default plugin.

.. py:function:: package.get(name, default=None)

   :param str name:    The ``object`` name.
   :param default:     The default value to return if lookup fails.
   :returns:           The plugged in ``object``.

   Returns the desired plugged in ``object``. Names are changed so that ``/``
   and ``-`` characters are converted to ``_``. So, the following example
   should work as expected:

   >>> from loremipsum.serialization import content_types
   >>> content_types.get('application/octet-stream')

.. py:function:: package.set_default(name)

   Set ``package.DEFAULT``. Initial value is :py:obj:`None`.

   :param str name:    The ``object`` name.

.. py:function:: package.registered()

   Returns a ``name: value`` dictionary of the registered ``object``s. ``name``
   is the actual registered name: see :py:func:`package.get` above.

   :returns:           :py:class:`dict`
"""
import collections
import functools
import importlib
import string

import pkg_resources

# Plugin register
_REGISTERED = collections.defaultdict(dict)


def _get(name, default=None, package=None):
    maketrans = getattr(string, 'maketrans', getattr(str, 'maketrans'))
    name = name.translate(maketrans("/-", "__"))
    return _REGISTERED[package.__name__].get(name, default)


def _set_default(name, package=None):
    package.DEFAULT = _get(name, None, package)


def _registered(package=None):
    return _REGISTERED[package.__name__].copy()


def setup(package):
    """Set the package/module up for plugins management.

    :param package:     The package/module object to setup for plugins.

    This function adds all the object listed in the package/module ``__all__``
    variable. ``plugin`` names listed in ``__all__`` are converted removing
    trailinig (right) ``_``. Also, adds all the objects returned by
    :py:func:`pkg_resources.iter_entry_points`: each object must be a callable
    which returns a value that can be used as argument for
    :py:meth:`dict.update`.
    """

    package.DEFAULT = None
    package.get = functools.partial(_get, package=package)
    package.set_default = functools.partial(_set_default, package=package)
    package.registered = functools.partial(_registered, package=package)

    pkg_name = package.__name__
    for module_name in package.__all__:
        try:
            value = importlib.import_module(module_name, pkg_name)
        except ImportError:
            value = getattr(package, module_name)

        name = module_name.rstrip('_')
        _REGISTERED[pkg_name][name] = value

    plugins = pkg_resources.iter_entry_points(package.__name__)
    _REGISTERED[package.__name__].update(plugins)
