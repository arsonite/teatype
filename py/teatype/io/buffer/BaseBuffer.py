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
from collections import OrderedDict

class BaseBuffer(OrderedDict):
    """
    Ordered, dict-like buffer that evicts the oldest entry once max_size is exceeded.
    Base class for the buffer hierarchy (MessageBuffer, RequestBuffer, StructBuffer, ...).
    Subclasses override _make_key() to derive a key from the value passed to add().
    """
    max_size:int

    def __init__(self, max_size:int=1000):
        super().__init__()
        self.max_size = max_size

    def _make_key(self, value:any) -> any:
        """
        Key used by add() when none is given; override for value-derived keys.
        """
        return len(self)

    def __setitem__(self, key:any, value:any):
        super().__setitem__(key, value)
        
        if len(self) > self.max_size:
            # self.keys() always iterates keys, unlike self (subclasses may override __iter__)
            del self[next(iter(self.keys()))]

    def add(self, value:any, key:any=None) -> any:
        """
        Insert value, deriving its key via _make_key() unless one is given. Returns the key used.
        """
        key = self._make_key(value) if key is None else key
        self[key] = value
        return key

    def latest(self) -> any:
        """
        Returns the most recently added value, or None if the buffer is empty.
        """
        return next(reversed(self.values()), None)
