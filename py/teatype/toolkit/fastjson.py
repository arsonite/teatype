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
import json
import math
import os
import pprint
import tempfile
import threading
from typing import Any, Dict, List, Union

# Third-party imports
import orjson
from simdjson import Parser, Object, Array

JSONType = Union[Dict[str, Any], List[Any], str, int, float, bool, None]

# The process umask can only be read by setting it - done once at import time, not per write
_UMASK = os.umask(0)
os.umask(_UMASK)

# A simdjson Parser reuses its internal buffers on every parse(), so it must never be shared
# between threads (e.g. FastAPI routes running through asyncio.to_thread).
_thread_local = threading.local()

def _get_parser() -> Parser:
    parser = getattr(_thread_local, 'parser', None)
    if parser is None:
        parser = _thread_local.parser = Parser()
    return parser

def _sanitize_non_finite(obj:Any) -> JSONType:
    if isinstance(obj, float):
        return obj if math.isfinite(obj) else None
    if isinstance(obj, dict):
        return {key: _sanitize_non_finite(value) for key, value in obj.items()}
    if isinstance(obj, list):
        return [_sanitize_non_finite(value) for value in obj]
    return obj

def compress(data:JSONType,
             compression_map:Dict[str,str],
             delimiter:str=".",
             flatten:bool=False) -> JSONType:
    """
    :param data: JSON data to compress
    :param compression_map: full → short key map
    :param delimiter: used only when flatten=True
    :param flatten: if True, returns a flat dict; else, nested with renamed keys
    """
    if not flatten:
        def _recurse(obj: Any) -> JSONType:
            if isinstance(obj, dict):
                return {
                    compression_map.get(k, k): _recurse(v)
                    for k, v in obj.items()
                }
            if isinstance(obj, list):
                return [_recurse(item) for item in obj]
            return obj
        return _recurse(data)

    # existing flatten algorithm
    flat: Dict[str, Any] = {}
    def _flat(obj: Any, parents: List[str]):
        if isinstance(obj, dict):
            for k, v in obj.items():
                ck = compression_map.get(k, k)
                _flat(v, parents + [ck])
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                _flat(v, parents + [str(i)])
        else:
            flat[delimiter.join(parents)] = obj

    _flat(data, [])
    return flat

def decompress(flat:Union[Dict[str, Any], JSONType],
               compression_map:Dict[str, str],
               delimiter:str=".",
               flatten:bool=False) -> JSONType:
    """
    :param flat: flat dict if flatten=True, else nested with compressed keys
    :param compression_map: full→short key map
    :param delimiter: used only when flatten=True
    :param flatten: should match the flag used in compress_json
    """
    inv_map = {v: k for k, v in compression_map.items()}

    if not flatten:
        def _recurse(obj: Any) -> JSONType:
            if isinstance(obj, dict):
                return {
                    inv_map.get(k, k): _recurse(v)
                    for k, v in obj.items()
                }
            if isinstance(obj, list):
                return [_recurse(item) for item in obj]
            return obj
        return _recurse(flat)  # type: ignore

    # existing un-flatten algorithm
    root: Dict[str, Any] = {}
    for compound_key, value in flat.items():  # type: ignore
        parts = compound_key.split(delimiter)
        cur: Any = root
        for idx, part in enumerate(parts):
            orig = inv_map.get(part, part)
            last = (idx == len(parts) - 1)
            if not last:
                nxt = parts[idx + 1]
                if nxt.isdigit():
                    cur = cur.setdefault(orig, [])
                else:
                    cur = cur.setdefault(orig, {})
            else:
                if part.isdigit() and isinstance(cur, list):
                    i = int(part)
                    while len(cur) <= i:
                        cur.append(None)
                    cur[i] = value
                else:
                    cur[orig] = value
    return root

def dump(data:JSONType, file_path:str, prettify:bool=False, create_parents:bool=True, fsync:bool=False) -> None:
    """
    Dump JSON data to a file atomically: the payload is serialized first and written to a temporary
    file next to the target, which then replaces the target in one step. A failing serialization or
    write never leaves a truncated/partial file behind - the previous content stays intact.
    
    :param data: JSON data to write.
    :param file_path: Path to the output file.
    :param prettify: Indent the output (2 spaces).
    :param create_parents: Create missing parent directories.
    :param fsync: Flush the data to disk before replacing the target (slower, survives power loss).
    """
    option = orjson.OPT_SERIALIZE_NUMPY
    if prettify:
        option |= orjson.OPT_INDENT_2
    payload = orjson.dumps(data, option=option)
    
    directory = os.path.dirname(file_path) or '.'
    if create_parents:
        os.makedirs(directory, exist_ok=True)
    
    # mkstemp creates the file with 0600 - keep the target's permissions (or the umask default)
    mode = os.stat(file_path).st_mode & 0o777 if os.path.isfile(file_path) else 0o666 & ~_UMASK
    file_descriptor, temp_path = tempfile.mkstemp(dir=directory, prefix='.', suffix='.tmp')
    try:
        with os.fdopen(file_descriptor, 'wb') as f:
            f.write(payload)
            if fsync:
                f.flush()
                os.fsync(f.fileno())
        os.chmod(temp_path, mode)
        os.replace(temp_path, file_path)
    except BaseException:
        try:
            os.unlink(temp_path)
        except OSError:
            pass
        raise

def load(file_path:str) -> JSONType:
    """
    Load JSON data from a file.
    
    Files that are not strict JSON because Python's json module wrote them (NaN/Infinity tokens)
    are still read; the non-finite floats become None, like in teatype.io.file.read.
    
    :param file_path: Path to the JSON file.
    :return: Parsed JSON data.
    """
    with open(file_path, 'rb') as f:
        json_bytes = f.read()
        
    try:
        simdjson_object = _get_parser().parse(json_bytes)
    except ValueError:
        data = _sanitize_non_finite(json.loads(json_bytes))
        if not isinstance(data, (dict, list)):
            raise TypeError(f'Unsupported top-level JSON type: {type(data)}')
        return data
    
    if isinstance(simdjson_object, Object):
        return simdjson_object.as_dict()
    elif isinstance(simdjson_object, Array):
        return simdjson_object.as_list()
    else:
        raise TypeError(f'Unsupported top-level JSON type: {type(simdjson_object)}')

def print(data:JSONType) -> str:
    pprint.pprint(data, indent=4, width=80, compact=True)