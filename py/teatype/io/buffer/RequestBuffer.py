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
import time

# Local imports
from teatype.logging import warn
from teatype.io.buffer.BaseBuffer import BaseBuffer

class RequestBuffer(BaseBuffer):
    """
    Buffer for request dicts; auto-assigns a 'timestamp' on insert and tracks the time
    deltas (delta_collection) of every entry relative to the latest one.
    """
    delta_collection:list
    latest_timestamp:float

    def __init__(self, max_size:int):
        super().__init__(max_size=max_size)
        self.delta_collection = []
        self.latest_timestamp = None

    def __setitem__(self, key:str, value:dict):
        if not isinstance(value, dict):
            raise TypeError('Value must be provided as a dictionary.')

        try:
            if 'timestamp' not in value:
                value['timestamp'] = time.time_ns() * 1000
            self.latest_timestamp = value['timestamp']
            super().__setitem__(key, value)
            self._refresh_deltas()
        except Exception as exc:
            warn(f'Error inserting item: {exc}')

    def _refresh_deltas(self):
        """
        Recomputes delta_collection from scratch based on current buffer contents.
        """
        try:
            timestamps = [float(entry['timestamp']) for entry in self.values() if entry is not None]
            self.delta_collection = [self.latest_timestamp - timestamp for timestamp in timestamps]
        except Exception as exc:
            warn(f'Error refreshing delta collection: {exc}')
            self.delta_collection = []

    def max_delta(self, unit:str='s') -> float:
        """
        Maximum time difference between the latest entry and all others, in 'ms' or 's'.
        """
        try:
            if unit == 'ms':
                factor = 1.0
            elif unit == 's':
                factor = 1 / 1000
            else:
                raise ValueError(f'Unit "{unit}" is not supported.')
            return round(max(self.delta_collection) * factor, 2) if self.delta_collection else 0.0
        except Exception as exc:
            warn(f'Error computing max delta: {exc}')
            return None

    def clear_buffer(self):
        self.clear()
        self.delta_collection = []
        self.latest_timestamp = None
