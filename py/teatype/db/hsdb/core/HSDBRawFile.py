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

# System imports
import base64
from typing import List

# Third-party imports
from teatype.db.hsdb.core.HSDBAttribute import HSDBAttribute

# Content types a file attribute can hold, and the extension they are stored with
RAW_FILE_TYPES = {
    'image/jpeg': 'jpg',
    'image/png': 'png',
    'image/webp': 'webp',
    'image/gif': 'gif',
    'image/avif': 'avif',
    'image/svg+xml': 'svg',
    'application/pdf': 'pdf',
    'application/octet-stream': 'bin'
}

class HSDBRawFile(HSDBAttribute):
    """
    Attribute that holds a file (an image, ...). The entry keeps only the path, the bytes live in
    rawfiles/<attribute name>/<sha256>.<extension>, so models whose attributes share a name share a folder.

    Write it by sending the bytes and their content type in the attribute, in a POST, a PATCH or a bulk request:
        {"image": {"type": "image/png", "data": "<base64>"}}   or   {"image": "data:image/png;base64,<base64>"}
    The server stores the file and the entry answers with the path ("rawfiles/image/<hash>.png"); sending that path
    again keeps the file, `null` removes it. A file nothing points to anymore is deleted. Read it with GET /hsdb/<path>.
    """
    def __init__(self,
                 *,
                 description:str=None,
                 max_bytes:int=10 * 1024 * 1024,
                 required:bool=False,
                 types:List[str]=('image/*',)):
        super().__init__(str, description=description, required=required)
        self.raw_file = {'types': list(types), 'max_bytes': max_bytes} # Kept in one key, so copies of the attribute can leave it out

    @staticmethod
    def accepts(spec:dict, content_type:str) -> bool:
        return content_type in RAW_FILE_TYPES and any(
            content_type == allowed or (allowed.endswith('/*') and content_type.startswith(allowed[:-1])) for allowed in spec['types'])

    @staticmethod
    def encode(data:bytes, content_type:str) -> dict:
        """
        The value to send for a file attribute.
        """
        return {'type': content_type, 'data': base64.b64encode(data).decode()}
