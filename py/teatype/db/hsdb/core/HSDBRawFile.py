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
from typing import Type, Union

# Third-party imports
from teatype.db.hsdb.core.HSDBAttribute import HSDBAttribute
from teatype.db.hsdb.core.HSDBRawFileType import IMAGES, HSDBRawFileType, raw_file_type

class HSDBRawFile(HSDBAttribute):
    """
    Attribute that holds a file. Like HSDBAttribute it takes the types it can hold: HSDBRawFile(image_jpeg, image_png),
    HSDBRawFile(pdf), HSDBRawFile(bytes) for anything, HSDBRawFile(*IMAGES) (the default) for all images. The types are in
    HSDBRawFileType.py. The entry keeps only the path, the bytes live in rawfiles/<attribute name>/<sha256>.<extension>,
    so models whose attributes share a name share a folder.

    Write it by sending the bytes and their content type in the attribute, in a POST, a PATCH or a bulk request:
        {"image": {"type": "image/png", "data": "<base64>"}}   or   {"image": "data:image/png;base64,<base64>"}
    The server stores the file and the entry answers with the path ("rawfiles/image/<hash>.png"); sending that path
    again keeps the file, `null` removes it. A file nothing points to anymore is deleted. Read it with GET /hsdb/<path>.
    """
    def __init__(self,
                 *types:Union[Type[HSDBRawFileType], type],
                 description:str=None,
                 max_bytes:int=10 * 1024 * 1024,
                 required:bool=False):
        super().__init__(str, description=description, required=required)
        file_types = [raw_file_type(item) for item in types or IMAGES]
        # Kept in one key, so copies of the attribute can leave it out
        self.raw_file = {'types': [file_type.mime for file_type in file_types], 'max_bytes': max_bytes}

    @staticmethod
    def accepts(spec:dict, content_type:str) -> bool:
        return content_type in spec['types']

    @staticmethod
    def matches(content_type:str, data:bytes) -> bool:
        """
        Whether the bytes are a file of that content type.
        """
        return raw_file_type(content_type).matches(data)

    @staticmethod
    def encode(data:bytes, content_type:str) -> dict:
        """
        The value to send for a file attribute.
        """
        return {'type': content_type, 'data': base64.b64encode(data).decode()}
