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

# From system imports
from abc import ABC, abstractmethod

# From package imports
from teatype.hsdb import HSDBAttribute
from teatype.hsdb.util import parse_name
from teatype.io import env

# From-as system imports
from datetime import datetime as dt

# From-as package imports
from teatype import id as generate_id

# TODO: Add validation method inside model
# TODO: Add attribute supports
# TODO: Add language supports
class HSDBModel(ABC):
    # app_name=HSDBAttribute('app_name', editable=False, type=str)
    # created_at=HSDBAttribute('created_at', computed=True, type=dt)
    # id=HSDBAttribute('id', computed=True, unique=True, type=str)
    # is_fixture=HSDBAttribute('is_fixture', editable=False, type=bool)
    # migration_id=HSDBAttribute('migration_id', editable=False, type=int)
    # synced_at=HSDBAttribute('synced_at', computed=True, type=dt)
    # updated_at=HSDBAttribute('updated_at', computed=True, type=dt)
    # was_synced=HSDBAttribute('synced', editable=False, type=bool)
    _overwrite_path:str
    _overwrite_name:str
    _overwrite_plural_name:str
    _path:str
    _name:str
    _plural_name:str
    _relations:dict
    
    migrated_at:dt
    migration_app_name:str
    migration_id:int
    migration_name:str
    
    app_name:str
    created_at:dt
    id:str
    is_fixture:bool=False
    model_name:str
    synced_at:dt
    updated_at:dt
    was_synced:bool=False
    
    def __init__(self,
                 id:str=None,
                 created_at:str=None,
                 updated_at:str=None,
                 overwrite_path:str=None):
        # TODO: Turn into util function
        if id is not None:
            self.id = id
        else:
            self.id = generate_id()
            
        # TODO: Remove model name for redunancy when using a model index
        self.model_name = type(self).__name__ 
        self._name = parse_name(self.model_name, remove='-model', plural=False)
        self._plural_name = parse_name(self.model_name, remove='-model', plural=True)
        
        if overwrite_path:
            self.path = overwrite_path
        self.path = f'{self._plural_name}/{self.id}.json'
        
        if created_at:
            self.created_at = dt.fromisoformat(created_at)
        else:
            self.created_at = dt.now()
        if updated_at:
            self.updated_at = dt.fromisoformat(updated_at)
        else:
            self.updated_at = dt.now()
        
        # TODO: Make this dynamic
        self.app_name = 'raw'
        self.migration_id = 1
        
    def loads(self, data:dict):
        pass

    def serialize(self,
                  include_migration:bool=True,
                  include_model:bool=True,
                  json_dump:bool=False,
                  use_data_key:bool=False) -> dict|str:
        serializer = self.serializer()
        serialized_data = dict()
        
        base_data = {
            'created_at': str(self.created_at),
            'id': self.id,
            'updated_at': str(self.updated_at)
        } 
        serialized_data['base_data'] = base_data
        
        data_key = self._name + '_data' if use_data_key else 'data'
        serialized_data[data_key] = serializer
        
        if include_migration:
            migration_data = {
                'app_name': self.app_name,
                'migration_id': self.migration_id,
            }  
            serialized_data['migration_data'] = migration_data
            
        if include_model:
            model_data = {
                'app_name': self.app_name,
                'model_name': self.model_name,
            }
            serialized_data['model_data'] = model_data
        
        return serialized_data if not json_dump else json.dumps(serialized_data, indent=4)
    
    def snapshot(self) -> dict:
        snapshot_dict = {}
        for key, value in self.__dict__.items():
            # TODO: If variable is of type HSDBAttribute
            if isinstance(value, dt):
                snapshot_dict[key] = str(value)
        return snapshot_dict
    
    def update(self, data:dict):
        for key, value in data.items():
            setattr(self, key, value)
        self.updated_at = dt.now()
        
    ####################
    # Abstract methods #
    ####################
    
    @abstractmethod
    def serializer(self) -> dict:
        raise NotImplementedError('Model does not have serializer')