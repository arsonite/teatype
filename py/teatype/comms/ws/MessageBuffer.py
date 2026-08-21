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

class MessageBuffer:
    """
    Ordered store for websocket messages, keyed by 'request_id' when the message
    carries one, otherwise by insertion order. Oldest entries are evicted once
    max_size is exceeded.
    """
    max_size:int
    messages:dict

    def __init__(self, max_size:int=1000):
        self.max_size = max_size
        self.messages = {}

    def add(self, data:dict):
        key = data.get('request_id', len(self.messages))
        self.messages[key] = data
        if len(self.messages) > self.max_size:
            del self.messages[next(iter(self.messages))]
        return key

    def get(self, key):
        return self.messages.get(key)

    def latest(self):
        return next(reversed(self.messages.values()), None)

    def __len__(self):
        return len(self.messages)

    def __iter__(self):
        return iter(self.messages.values())

    def __getitem__(self, key):
        return self.messages[key]
