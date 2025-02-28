# Copyright (C) 2024-2025 Burak Günaydin
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

# From package imports
from teatype.io import path

__FS = {
    'hsdb': {
        'backups': {
            'index': {},
            'migration': {},
            'rawfiles': {}
        },
        'dumps': {},
        'exports': {},
        'index': {},
        'logs': {
            'migrations': {}
        },
        'meta': {},
        'models': {
            'adapters': {},
        },
        'rawfiles': {},
        'redundancy': {},
        'rejectpile': {
            'index': {},
            'rawfiles': {}
        }
    }
}

class _FSProxy:
    def __init__(self, data):
        for key, value in data.items():
            if isinstance(value, dict):
                setattr(self, key, _FSProxy(value))
            else:
                setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

class RawFileStructure:
    _fs:_FSProxy
    _root_path:str
    
    def __init__(self, root_path:str, auto_create_folders:bool=True):
        self._root_path = root_path
        
        self._fs = _FSProxy(__FS)
        
        if auto_create_folders:
            import copy
            self.create_fs(root_path, copy.deepcopy(__FS))
        
    def create_fs(self, base_path, structure):
        for key, value in structure.items():
            dir_path = path.join(base_path, key)
            if not path.exists(dir_path):
                path.create(dir_path)
            if isinstance(value, dict):
                self.create_fs(dir_path, value)
        
    def get_fs(self):
        return self._fs