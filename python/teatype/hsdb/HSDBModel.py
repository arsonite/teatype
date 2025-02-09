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

# System imports
import json
import re

# From package imports
from teatype.hsdb import HSDBAttribute
from teatype.io import env

# From-as system imports
from datetime import datetime as dt

# From-as package imports
from teatype import id as generate_id

# TODO: Add validation method inside model
# TODO: Add attribute supports
# TODO: Add language supports
class HSDBModel:
    # created_at=HSDBAttribute('created_at', computed=True)
    # id=HSDBAttribute('id', computed=True, unique=True)
    # file_path=HSDBAttribute('file_path', computed=True)
    # is_fixture=HSDBAttribute('is_fixture', editable=False)
    # name=HSDBAttribute('name', computed=True)
    # plural_name=HSDBAttribute('plural_name', computed=True)
    # root_raw_path=HSDBAttribute('root_raw_path', computed=True)
    # updated_at=HSDBAttribute('updated_at', computed=True)
    id:str
    is_fixture:bool=False
    name:str
    plural_name:str
    overwrite_file_path:str
    
    def __init__(self, id:str=None, name:str=None, overwrite_file_path:str=None):
        # TODO: Turn into util function
        def _parse_name(raw_name:str, seperator:str='-', plural:bool=False):
            return re.sub(r'(?<!^)(?=[A-Z])', seperator, raw_name).lower()
        
        if id is not None:
            self.id = id
        else:
            self.id = generate_id(truncate=16)
            
        if name is not None:
            self.name = name
            
        if overwrite_file_path:
            self.overwrite_file_path = overwrite_file_path
        
        # TODO: Remove model name for redunancy when using a model index
        self.model_name = type(self).__name__ 
        # TODO: Turn into util function
        self.parsed_name = _parse_name(self.model_name).replace('-model', '')
        self.parsed_plural_name = self.name + 's' if not self.name.endswith('s') else self.name + 'es'
        
        self.created_at = dt.now()
        self.updated_at = dt.now()
        
    # TODO: Figure out how to do this
    #     self._establishRelations()
    
    # # TODO: Implement
    # def _establishRelations(self):
    #     pass
    
    @property
    def file_path(self) -> str:
        if self.hasattr('overwrite_file_path'):
            return self.overwrite_file_path
        return f'{self.plural_name}/{self.id}.json'
    
    def as_dict(self) -> dict:
        # TODO: check for hsdbattributes
        return self.__dict__
    
    def serialize(self) -> str:
        return json.dumps(self.as_dict())
    
    def update(self, data:dict):
        for key, value in data.items():
            setattr(self, key, value)
        self.updated_at = dt.now()