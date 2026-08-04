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
from typing import Optional

# Third-party imports
from pydantic import BaseModel, ConfigDict

class WebsocketMessage(BaseModel):
    """
    Minimal contract every websocket payload must satisfy: a 'key' used to route
    callback handlers, and an optional 'request_id' used to correlate buffered
    input/output. Any other fields are passed through untouched.
    """
    model_config=ConfigDict(extra='allow')

    key:str
    request_id:Optional[str]=None
