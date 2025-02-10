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

# From system imports
from abc import ABC, abstractmethod

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
class HSDBModel(ABC):
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
    overwrite_parsed_name:str
    overwrite_parsed_plural_name:str
    
    def __init__(self, id:str=None, name:str=None, overwrite_file_path:str=None):
        # TODO: Turn into util function
        def _parse_name(raw_name:str, seperator:str='-', plural:bool=False):
            return re.sub(r'(?<!^)(?=[A-Z])', seperator, raw_name).lower()
        
        if id is not None:
            self.id = id
        else:
            self.id = generate_id()
            
        if name is not None:
            self.name = name
        
        # TODO: Remove model name for redunancy when using a model index
        self.model_name = type(self).__name__ 
        # TODO: Turn into util function
        self.parsed_name = _parse_name(self.model_name).replace('-model', '')
        self.parsed_plural_name = self.parsed_name + 's' if not self.parsed_name.endswith('s') else self.parsed_name + 'es'
        
        if overwrite_file_path:
            self.file_path = overwrite_file_path
        self.file_path = f'{self.parsed_plural_name}/{self.id}.json'
        
        self.created_at = dt.now()
        self.updated_at = dt.now()
        
    # TODO: Figure out how to do this
    #     self._establishRelations()
    
    # # TODO: Implement
    # def _establishRelations(self):
    #     pass
    
    @abstractmethod
    def serializer(self) -> dict:
        raise NotImplementedError('Model does not have serializer')
    
    def serialize(self, json_dump:bool=False) -> dict|str:
        serialized_data = self.serializer()
        # TODO: Remove model_meta when using a model index and seperate model-meta.json
        full_data = {
            **serialized_data,
            'model_meta': {
                'model_name': self.model_name,
                'parsed_name': self.parsed_name,
                'parsed_plural_name': self.parsed_plural_name
            },
            'id': self.id,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at)
        }
        if hasattr(self, 'name'):
            full_data['name'] = self.name
            
        return full_data if not json_dump else json.dumps(full_data)
    
    def update(self, data:dict):
        for key, value in data.items():
            setattr(self, key, value)
        self.updated_at = dt.now()