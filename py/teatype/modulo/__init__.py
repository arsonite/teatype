# Copyright (C) 2024-2026 Burak Günaydin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# Standard-library imports
import importlib
from importlib.util import find_spec

from .tracer import Tracer

# Probe for the optional dependencies instead of importing the whole package, which
# pulls in fastapi/django/redis and makes every `import teatype.modulo` slow.
_REQUIRED_PACKAGES = ('django', 'fastapi', 'redis', 'rest_framework', 'uvicorn')
_missing_packages = [package for package in _REQUIRED_PACKAGES if find_spec(package) is None]

__MODULO_IMPORT_ERROR__ = ImportError(f'missing packages: {", ".join(_missing_packages)}') if _missing_packages else None
__MODULO_SUPPORT__ = not _missing_packages

_LAZY_ATTRS = {
    'LaunchPad': ('.launchpad', 'LaunchPad'),
    'Operations': ('.operations', 'Operations'),
    'ModuloOperations': ('.operations', 'Operations'),
    'CoreUnit': ('.units.core', 'CoreUnit'),
    'parse_designation': ('.units.core', 'parse_designation'),
    'print_designation': ('.units.core', 'print_designation'),
    'ServiceUnit': ('.units.service', 'ServiceUnit'),
    'WorkhorseUnit': ('.units.workhorse', 'WorkhorseUnit'),
}

def __getattr__(name):
    if name in _LAZY_ATTRS:
        module_name, attribute = _LAZY_ATTRS[name]
        return getattr(importlib.import_module(module_name, __name__), attribute)
    # Lazily import the hsdb registry so fastapi/uvicorn only load when it is used
    if name == 'hsdb':
        global hsdb
        from teatype.modulo.hsdb import hsdb
        return hsdb
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")