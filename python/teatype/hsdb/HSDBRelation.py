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

# From system imports
from abc import ABC
from typing import List

# From package imports
from teatype.hsdb import HSDBField, HSDBQuery
from teatype.util import kebabify

# TODO: HSDB type is Relation for metadata access, but value is always the query close
# TODO: Internal callable that returns special query with overwritten foreign model and capped queryset in the init of hsdbmodel
# TODO: Accessing the HSDB Relation value returns the query closure object without execution, a one to one executes the query and returns the object by overriding method
# TODO: Dont use references after all, just ids, otherwise whats the point of the index db
class HSDBRelation(HSDBField):
    primary_keys:List[str]
    primary_model:type
    relational_name:type
    relational_type:type
    relational_key:str
    reverse_lookup:str
    secondary_keys:List[str]
    secondary_model:type
    
    @property
    def _query_closure(self):
        query = HSDBQuery(self)
        subset = {key:query._index_db_reference[key] for key in query._index_db_reference if key in self.secondary_keys}
        query._index_db_reference = subset
        # query._index_db_reference = {{entry.id:entry for entry in self.secondary_model.query.all()}}
        return query
    
    def __init__(self,
                 primary_keys:List[str],
                 primary_model:type,
                 secondary_keys:List[str],
                 secondary_model:type,
                 relational_type:type,
                 reverse_lookup:str,
                 editable:bool=True,
                 relational_key:str='id',
                 required:bool=False) -> None:
        super().__init__(editable, True, required)
        
        self.primary_model = primary_model
        self.relational_key = relational_key
        self.reverse_lookup = reverse_lookup
        self.secondary_model = secondary_model
        
        self.setPrimaryKeys(primary_keys)
        self.setSecondaryKeys(secondary_keys)
        
        self.relational_name = f'{self.primary_model.__name__}_{relational_type}_{self.secondary_model.__name__}'
        
        self._value = self._query_closure

    def __get__(self, instance, owner):
        if self._wrapper is None:
            self._wrapper = self._RelationWrapper(self._value, self)
        return self._wrapper
            
    def _validate_key(self, key:str) -> None:
        if not isinstance(key, str) or not key:
            raise ValueError('key must be a non-empty string')
            
    def _validate_keys(self, keys:List[str]) -> None:
        if not isinstance(keys, list) or not keys:
            raise ValueError('keys must be a non-empty list')
        for key in keys:
            self._validate_key(key)
        
    def addPrimaryKey(self, primary_key:str) -> None:
        if primary_key in self.primary_keys:
            raise ValueError(f'Primary key {primary_key} already exists')
        elif primary_key in self.secondary_keys:
            raise ValueError(f'Primary key {primary_key} cannot be a secondary')
        self._validate_key(primary_key)        
        self.primary_keys.append(primary_key)
        
    def addSecondaryKey(self, secondary_key:str) -> None:
        if secondary_key in self.secondary_keys:
            raise ValueError(f'Secondary key {secondary_key} already exists')
        elif secondary_key in self.primary_keys:
            raise ValueError(f'Secondary key {secondary_key} cannot be a primary')
        self._validate_key(secondary_key)        
        self.secondary_keys.append(secondary_key)
        
    def removePrimaryKey(self, primary_key:str) -> None:
        if primary_key not in self.primary_keys:
            raise ValueError(f'Primary key {primary_key} does not exist')
        self.primary_keys.remove(primary_key)
        
    def removeSecondaryKey(self, secondary_key:str) -> None:
        if secondary_key not in self.secondary_keys:
            raise ValueError(f'Secondary key {secondary_key} does not exist')
        self.secondary_keys.remove(secondary_key)
    
    def setPrimaryKeys(self, primary_keys:List[str]) -> None:
        self._validate_keys(primary_keys)
        self.primary_keys = primary_keys
        
    def setSecondaryKeys(self, secondary_keys:List[str]) -> None:
        self._validate_keys(secondary_keys)
        self.secondary_keys = secondary_keys
        
    ####################
    # Internal Classes #
    ####################

    class _RelationWrapper(HSDBField._ValueWrapper):
        def _load_metadata(self):
            """
            Load the metadata (lazy loading).
            """
            if not self._metadata_loaded:
                self._cached_metadata = {
                    'primary_keys': self._field.primary_keys,
                    'primary_model': self._field.primary_model,
                    'relational_key': self._field.relational_key,
                    'relational_name': self._field.relational_name,
                    'relational_type': self._field.relational_type,
                    'reverse_lookup': self._field.reverse_lookup,
                    'secondary_keys': self._field.secondary_keys,
                    'secondary_model': self._field.secondary_model
                }
                self._metadata_loaded = True
            return self._cached_metadata

        @property
        def primary_keys(self):
            metadata = self._load_metadata()
            return metadata['primary_keys']
        
        @property
        def primary_model(self):
            metadata = self._load_metadata()
            return metadata['primary_model']
        
        @property
        def relational_key(self):
            metadata = self._load_metadata()
            return metadata['relational_key']
        
        @property
        def relational_name(self):
            metadata = self._load_metadata()
            return metadata['relational_name']
        
        @property
        def relational_type(self):
            metadata = self._load_metadata()
            return metadata['relational_type']
        
        @property
        def reverse_lookup(self):
            metadata = self._load_metadata()
            return metadata['reverse_lookup']
        
        @property
        def secondary_keys(self):
            metadata = self._load_metadata()
            return metadata['secondary_keys']
        
        @property
        def secondary_model(self):
            metadata = self._load_metadata()
            return metadata['secondary_model']
    
    class _RelationFactory(ABC):
        editable:bool
        relational_key:str
        relation_type:str
        required:bool
        reverse_lookup:str
        secondary_model:type
        
        def __init__(self,
                     secondary_model:type,
                     editable:bool=True,
                     relational_key:str='id',
                     required:bool=False,
                     reverse_lookup:str=None) -> None:
            self.editable = editable
            self.relational_key = relational_key
            self.required = required
            self.secondary_model = secondary_model
            
            self.relation_type = kebabify(self.__class__.__name__)
            if reverse_lookup is not None:
                self.reverse_lookup = reverse_lookup
            else:
                self.reverse_lookup = kebabify(secondary_model.__name__, replace=('-model', ''))
            
        def create(self,
                   primary_keys:List[str],
                   primary_model:type,
                   secondary_keys:List[str]) -> 'HSDBRelation':
            return HSDBRelation(primary_keys,
                                primary_model,
                                secondary_keys,
                                self.secondary_model,
                                self.relation_type,
                                self.reverse_lookup,
                                self.editable,
                                self.relational_key,
                                self.required)
    
    class OneToOne(_RelationFactory):
        pass

    class OneToMany(_RelationFactory):
        pass

    class ManyToOne(_RelationFactory):
        pass

    class ManyToMany(_RelationFactory):
        pass