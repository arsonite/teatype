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

# TODO: HSDB type is Relation for metadata access, but value is always the query close
# TODO: Internal callable that returns special query with overwritten foreign model and capped queryset in the init of hsdbmodel
# TODO: Accessing the HSDB Relation value returns the query closure object without execution, a one to one executes the query and returns the object by overriding method
# TODO: Dont use references after all, just ids, otherwise whats the point of the index db
class HSDBRelation(HSDBField):
    primary_keys:List[str]
    primary_model:type
    relation_type:type
    relational_key:str
    secondary_keys:List[str]
    secondary_model:type
    
    def _query_closure(self):
        query = HSDBQuery(self)
        query._index_db_reference = {{entry.id:entry for entry in self.secondary_model.objects.all()}}
        return query
    
    def __init__(self,
                 primary_keys:List[str],
                 secondary_keys:List[str],
                 relation_type:type,
                 relational_key:str='id') -> None:
        self.relational_key = relational_key
        
        self.setPrimaryKeys(primary_keys)
        self.setSecondaryKeys(secondary_keys)
        
        self.name = f'{self.primary_model.model_name}_{relation_type}_{self.secondary_model.model_name}'
            
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
        self._primary_keys = primary_keys
        self._parse_relation_type()
        
    def setSecondaryKeys(self, secondary_keys:List[str]) -> None:
        self._validate_keys(secondary_keys)
        self._secondary_keys = secondary_keys
        self._parse_relation_type()
        
    ####################
    # Internal Classes #
    ####################

    # class _RelationProxy:
    #     def __init__(self, relation:HSDBRelation) -> None:
    #         self._relation = relation
    
    class _RelationFactory(ABC):
        @classmethod
        def create(cls,
                   relation_type:type,
                   primary_model:type,
                   secondary_model:type,
                   primary_keys:List[str],
                   secondary_keys:List[str],
                   relational_key:str='id'):
            return HSDBRelation(primary_keys, secondary_keys, relation_type, relational_key)

    class _RelationWrapper(HSDBField._ValueWrapper):
        def _load_metadata(self):
            """
            Load the metadata (lazy loading).
            """
            if not self._metadata_loaded:
                self._cached_metadata = {
                    'cls': self._field.cls,
                    'computed': self._field.computed,
                    'description': self._field.description,
                    'editable': self._field.editable,
                    'indexed': self._field.indexed,
                    'instance': self._field,
                    'key': self._field.key,
                    'max_size': self._field.max_size,
                    'required': self._field.required,
                    'searchable': self._field.searchable,
                    'type': self._field.type,
                    'unique': self._field.unique
                }
                self._metadata_loaded = True
            return self._cached_metadata

        @property
        def cls(self):
            metadata = self._load_metadata()
            return metadata['cls']

        @property
        def computed(self):
            metadata = self._load_metadata()
            return metadata['computed']
        
        @property
        def description(self):
            metadata = self._load_metadata()
            return metadata['description']
        
        @property
        def editable(self):
            metadata = self._load_metadata()
            return metadata['editable']
        
        @property
        def indexed(self):
            metadata = self._load_metadata()
            return metadata['indexed']
        
        @property
        def instance(self):
            metadata = self._load_metadata()
            return metadata['instance']
        
        @property
        def key(self):
            metadata = self._load_metadata()
            return metadata['key']
        
        @property
        def max_size(self):
            metadata = self._load_metadata()
            return metadata['max_size']
        
        @property
        def required(self):
            metadata = self._load_metadata()
            return metadata['required']
        
        @property
        def searchable(self):
            metadata = self._load_metadata()
            return metadata['searchable']

        @property
        def type(self):
            metadata = self._load_metadata()
            return metadata['type']
        
        @property
        def unique(self):
            metadata = self._load_metadata()
            return metadata['unique']
    
    class OneToOne(_RelationFactory):
        pass

    class OneToMany(_RelationFactory):
        pass

    class ManyToOne(_RelationFactory):
        pass

    class ManyToMany(_RelationFactory):
        pass