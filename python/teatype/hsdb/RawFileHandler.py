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
from teatype.io import env, file, path
from teatype.hsdb import RawFileStructure

_DEFAULT_ROOT_PATH = '/var/lib/hsdb'

class RawFileHandler:
    _raw_file_structure:RawFileStructure
    _root_path:str
    
    def __init__(self, root_path:str=None):
        if root_path is None:
            root_path = _DEFAULT_ROOT_PATH
        self._root_path = root_path
            
        self._raw_file_structure = RawFileStructure(root_path)
        
    @property
    def fs(self):
        return self._raw_file_structure.get_fs()
        
    # TODO: If new attributes surface (migrations), apply them to old files (backup before)
    def create_entry(self, model_instance:object, overwrite_path:str, compress:bool=False) -> str:
        try:
            absolute_file_path = path.join(self._root_path, model_instance.file_path)
            if path.exists(absolute_file_path):
                return 'File already exists'
        
            # TODO: If model folder does not exist, create it and put model_meta.json into it
            # TODO: Create variable in path.create for exists ok
            file.write(absolute_file_path,
                       model_instance.serialize(),
                       force_format='json',
                       prettify=not compress,
                       create_parents=True)
            return absolute_file_path
        except Exception as exc:
            raise Exception(f'Could not create raw file entry: {exc}')