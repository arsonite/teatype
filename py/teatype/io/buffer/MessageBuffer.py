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

# Local imports
from teatype.io.buffer.BaseBuffer import BaseBuffer

class MessageBuffer(BaseBuffer):
    """
    Buffer keyed by a message's 'request_id' when present, otherwise by insertion order.
    Iterates over stored messages (not keys), matching websocket message-stream semantics.
    """
    def _make_key(self, value:dict) -> any:
        return value.get('request_id', len(self))

    def __iter__(self):
        return iter(self.values())
