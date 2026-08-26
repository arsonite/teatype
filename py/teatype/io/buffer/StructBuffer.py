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

# Third-party imports
from pydantic import BaseModel

# Local imports
from teatype.io.buffer.BaseBuffer import BaseBuffer

class StructBuffer(BaseBuffer):
    """
    Buffer restricted to a single pydantic schema; add() validates/coerces every entry
    against it, for use-cases that need structured (not free-form dict) buffered data.
    """
    schema:type[BaseModel]

    def __init__(self, schema:type[BaseModel], max_size:int=1000):
        super().__init__(max_size=max_size)
        self.schema = schema

    def add(self, value:any, key:any=None) -> any:
        if not isinstance(value, self.schema):
            value = self.schema.model_validate(value)
        return super().add(value, key=key)
