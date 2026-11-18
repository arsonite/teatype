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
import hashlib
import os
import re

# Third-party imports
from teatype.db.hsdb import RawFileStructure
from teatype.io import file, path
from teatype.logging import *

# <sha256 of the content>.<extension>, which is all a stored file may be called
RAW_FILE_NAME = re.compile(r'[0-9a-f]{64}\.[a-z0-9]{1,8}')

class RawFileHandler:
    _rf_structure:RawFileStructure
    cold_mode:bool
    
    def __init__(self,
                 root_path:str=None,
                 *,
                 cold_mode:bool=False,
                 name:str=None):
        self.cold_mode = cold_mode
        
        self._rf_structure = RawFileStructure(root_path,
                                              cold_mode=cold_mode,
                                              name=name)
        
    ##############
    # Properties #
    ##############
        
    @property
    def fs(self):
        return self._rf_structure.get_fs()
    
    ##############
    # Public API #
    ##############
        
    def write_model(self, model:type) -> str|None:
        """
        Write the schema descriptor models/<ModelName>.json so clients can discover models without the class.
        """
        if self.cold_mode:
            return None
        absolute_path = path.join(self.fs.models.path, f'{model.__name__}.json')
        file.write(absolute_path,
                   model.schema(),
                   force_format='json',
                   prettify=True,
                   create_parents=True)
        return absolute_path
        
    def write_raw_file(self, data:bytes, extension:str='bin') -> str:
        """
        Store binary content (an image, ...) under rawfiles/ and return its name, which is what a model attribute keeps
        to point to it. The name is the hash of the content, so the same content is stored once.
        """
        if self.cold_mode:
            raise RuntimeError('Cold-mode databases have no files')
        extension = re.sub(r'[^a-z0-9]', '', extension.lower())[:8] or 'bin'
        name = f'{hashlib.sha256(data).hexdigest()}.{extension}'
        absolute_path = path.join(self.fs.rawfiles.path, name)
        if not path.exists(absolute_path):
            temporary = f'{absolute_path}.tmp'
            with open(temporary, 'wb') as handle:
                handle.write(data)
            os.replace(temporary, absolute_path) # Never a half written file under its real name
        return name

    def raw_file_path(self, name:str) -> str|None:
        """
        Absolute path of a stored file, None if there is none of that name (also for names that are not made by write_raw_file).
        """
        if self.cold_mode or not RAW_FILE_NAME.fullmatch(name or ''):
            return None
        absolute_path = path.join(self.fs.rawfiles.path, name)
        return absolute_path if path.exists(absolute_path) else None

    def delete_raw_file(self, name:str) -> bool:
        absolute_path = self.raw_file_path(name)
        if not absolute_path:
            return False
        file.delete(absolute_path)
        return True

    # TODO: If new attributes surface (migrations), apply them to old files (backup before)
    def create_entry(self,
                     model_instance:object,
                     compress:bool=False) -> str|None:
        try:
            absolute_path = path.join(self.fs.indexdb.path, model_instance.path)

            if self.cold_mode:
                return absolute_path
            
            if path.exists(absolute_path):
                raise Exception('File already exists')
            
            Model = model_instance.model
            # TODO: If model folder does not exist, create it and put model_meta.json into it
            # TODO: Create variable in path.create for exists ok
            file.write(absolute_path,
                       Model.serialize(model_instance, include_relations=True),
                       force_format='json',
                       prettify=not compress,
                       create_parents=True)
            return absolute_path
        except Exception:
            err('Could not create raw file entry.', traceback=True)
            return None
        
    def delete_entry(self,
                     model_instance:object) -> bool:
        try:
            if self.cold_mode:
                return True
            
            absolute_path = path.join(self.fs.indexdb.path, model_instance.path)
            if not path.exists(absolute_path):
                return False
            
            file.delete(absolute_path)
            return True
        except Exception:
            err('Could not delete raw file entry.', traceback=True)
            return False
        
    def update_entry(self,
                     model_instance:object,
                     compress:bool=False) -> str:
        try:
            absolute_path = path.join(self.fs.indexdb.path, model_instance.path)
            if self.cold_mode:
                return absolute_path
            
            if not file.exists(absolute_path):
                raise Exception('File does not exist')

            Model = model_instance.model
            if not path.exists(absolute_path):
                return 'File does not exist'

            file.write(absolute_path,
                       Model.serialize(model_instance, include_relations=True),
                       force_format='json',
                       prettify=not compress,
                       create_parents=True)
            return absolute_path
        except Exception:
            err('Could not update raw file entry.', traceback=True)
            return None