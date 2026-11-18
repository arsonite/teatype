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

# System imports
from typing import Optional, Type, Union

class HSDBRawFileType:
    """
    A kind of file a RawFile attribute can hold, used like the Python types of HSDBAttribute: HSDBRawFile(image_png, pdf).
    The class itself is the type, it is never instantiated. It knows its content type, the extension the file is stored
    with and whether some bytes really are such a file.
    """
    mime:str
    extension:str

    @classmethod
    def matches(cls, data:bytes) -> bool:
        return True

class image_jpeg(HSDBRawFileType):
    mime = 'image/jpeg'
    extension = 'jpg'

    @classmethod
    def matches(cls, data:bytes) -> bool:
        return data.startswith(b'\xff\xd8\xff')

class image_png(HSDBRawFileType):
    mime = 'image/png'
    extension = 'png'

    @classmethod
    def matches(cls, data:bytes) -> bool:
        return data.startswith(b'\x89PNG\r\n\x1a\n')

class image_webp(HSDBRawFileType):
    mime = 'image/webp'
    extension = 'webp'

    @classmethod
    def matches(cls, data:bytes) -> bool:
        return data[:4] == b'RIFF' and data[8:12] == b'WEBP'

class image_gif(HSDBRawFileType):
    mime = 'image/gif'
    extension = 'gif'

    @classmethod
    def matches(cls, data:bytes) -> bool:
        return data[:6] in (b'GIF87a', b'GIF89a')

class image_avif(HSDBRawFileType):
    mime = 'image/avif'
    extension = 'avif'

    @classmethod
    def matches(cls, data:bytes) -> bool:
        return data[4:8] == b'ftyp' and data[8:12] in (b'avif', b'avis')

class image_svg(HSDBRawFileType):
    mime = 'image/svg+xml'
    extension = 'svg'

    @classmethod
    def matches(cls, data:bytes) -> bool:
        return b'<svg' in data[:4096]

class pdf(HSDBRawFileType):
    mime = 'application/pdf'
    extension = 'pdf'

    @classmethod
    def matches(cls, data:bytes) -> bool:
        return data.startswith(b'%PDF-')

class octet_stream(HSDBRawFileType):
    """
    Any bytes, written as the Python type `bytes`.
    """
    mime = 'application/octet-stream'
    extension = 'bin'

IMAGES = (image_jpeg, image_png, image_webp, image_gif, image_avif, image_svg)
RAW_FILE_TYPES = (*IMAGES, pdf, octet_stream)

def raw_file_type(item:Union[type, str]) -> Type[HSDBRawFileType]:
    """
    The type of a type (`bytes` is octet_stream) or of a content type, "image/png".
    """
    if item is bytes:
        return octet_stream
    for file_type in RAW_FILE_TYPES:
        if item is file_type or item == file_type.mime:
            return file_type
    raise ValueError(f'Unsupported raw file type: {item}, supported types are: bytes, {", ".join(t.__name__ for t in RAW_FILE_TYPES[:-1])}')

def raw_file_type_of_extension(extension:str) -> Optional[Type[HSDBRawFileType]]:
    return next((file_type for file_type in RAW_FILE_TYPES if file_type.extension == extension), None)
