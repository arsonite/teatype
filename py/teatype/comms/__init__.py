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

# The HTTP helpers below transitively import heavy web frameworks (fastapi, django,
# rest_framework). Importing them eagerly here made every `teatype.comms.*` submodule
# import (e.g. teatype.comms.ipc.redis) pull in that stack, which dominated CLI startup.
# They are exposed lazily via PEP 562 so the cost is only paid on first actual use.
__all__ = [
    'trequest',
    'get', 'post', 'put', 'patch', 'delete',
    'encode_url', 'decode_url', 'join_uris', 'url',
    'Websocket', 'WEBSOCKET_SUPPORT',
]

_LAZY_ATTRS = {
    'get': ('.http.trequest', 'get'),
    'post': ('.http.trequest', 'post'),
    'put': ('.http.trequest', 'put'),
    'patch': ('.http.trequest', 'patch'),
    'delete': ('.http.trequest', 'delete'),
    'encode_url': ('.http.hyperlink', 'encode'),
    'decode_url': ('.http.hyperlink', 'decode'),
    'join_uris': ('.http.hyperlink', 'join'),
    'url': ('.http.hyperlink', 'url'),
}

def __getattr__(name):
    if name == 'trequest':
        from .http import trequest
        return trequest
    if name in _LAZY_ATTRS:
        module_name, attr = _LAZY_ATTRS[name]
        module = importlib.import_module(module_name, __name__)
        return getattr(module, attr)
    if name == 'Websocket':
        try:
            from .ws.Websocket import Websocket
            return Websocket
        except ImportError:
            return None
    if name == 'WEBSOCKET_SUPPORT':
        try:
            from .ws.Websocket import Websocket  # noqa: F401
            return True
        except ImportError:
            return False
    raise AttributeError(f'module {__name__!r} has no attribute {name!r}')