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
import uuid
from datetime import datetime
from typing import Optional

# Local imports
from teatype.io.buffer.BaseQueue import BaseQueue

class RequestQueue(BaseQueue):
    """
    FIFO queue for cloud-based upload/download/archive/fetch requests; wraps each request with
    tracking metadata (request_id, queued_at, action) on enqueue.
    """
    allowed_action:str

    def __init__(self, allowed_action:str, max_queue_size:int=0):
        if allowed_action not in ['download', 'upload', 'archive', 'fetch']:
            raise ValueError(f'Invalid action type "{allowed_action}" for RequestQueue.')
        super().__init__(discipline='fifo', max_size=max_queue_size)
        self.allowed_action = allowed_action

    def enqueue(self, request:dict) -> str:
        """
        Add a cloud request to the queue, returning its (possibly generated) request_id.
        """
        request_id = request.get('request_id')
        if request_id is None:
            request_id = f'{self.allowed_action}_{uuid.uuid4().hex[:12]}'
            request['request_id'] = request_id

        request['_queued_at'] = datetime.now().isoformat()
        request['_action'] = self.allowed_action

        super().enqueue(request)
        return request_id

    def dequeue(self, block:bool=False, timeout:float=1.0) -> Optional[dict]:
        return super().dequeue(block=block, timeout=timeout)

    # Legacy methods for backward compatibility
    def push_request(self, url, is_async:bool=False):
        self.enqueue({'request_command': 'legacy-url-request',
                      'request_data': {'url': url, 'async': is_async}})

    def fetch_request(self, block:bool=False, timeout:float=1.0) -> Optional[dict]:
        return self.dequeue(block=block, timeout=timeout)
