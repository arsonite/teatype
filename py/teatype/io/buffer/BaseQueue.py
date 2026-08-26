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
import queue

class BaseQueue:
    """
    Thread-safe queue-backed buffer. Wraps a queue.Queue subclass chosen by discipline
    ('fifo', 'lifo' or 'priority') and proxies unknown attributes to it, so put/get/qsize/
    mutex/etc. keep working, on top of enqueue/dequeue/peek/clear conveniences.
    Base class for queue-shaped buffers (e.g. RequestQueue).
    """
    _DISCIPLINES = {'fifo': queue.Queue, 'lifo': queue.LifoQueue, 'priority': queue.PriorityQueue}

    def __init__(self, discipline:str='fifo', max_size:int=0):
        try:
            queue_class = self._DISCIPLINES[discipline]
        except KeyError:
            raise ValueError(f'Unknown queue discipline "{discipline}"')
        self._queue = queue_class(maxsize=max_size)

    def __getattr__(self, name:str):
        return getattr(self._queue, name)

    def __len__(self) -> int:
        return self._queue.qsize()

    def enqueue(self, item:any, block:bool=True, timeout:float=None):
        self._queue.put(item, block=block, timeout=timeout)

    def dequeue(self, block:bool=True, timeout:float=1.0) -> any:
        try:
            return self._queue.get(block=block, timeout=timeout)
        except queue.Empty:
            return None

    def peek(self) -> any:
        """
        Look at the next item without removing it, or None if the queue is empty.
        """
        try:
            with self._queue.mutex:
                return self._queue.queue[0] if self._queue.queue else None
        except Exception:
            return None

    def clear(self) -> int:
        """
        Clear all items from the queue. Returns the number of items cleared.
        """
        with self._queue.mutex:
            count = len(self._queue.queue)
            self._queue.queue.clear()
        return count

    def pending_count(self) -> int:
        return self._queue.qsize()
