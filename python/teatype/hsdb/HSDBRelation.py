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

_AVAILABLE_FIELDS = [
    'primary_keys',
    'primary_model',
    'relation_key',
    'relation_name',
    'relation_type',
    'reverse_lookup',
    'secondary_keys',
    'secondary_model',
    
    # Query params
    'all'
]

# TODO: HSDB type is Relation for metadata access, but value is always the query close
# TODO: Internal callable that returns special query with overwritten foreign model and capped queryset in the init of hsdbmodel
# TODO: Accessing the HSDB Relation value returns the query closure object without execution, a one to one executes the query and returns the object by overriding method
# TODO: Dont use references after all, just ids, otherwise whats the point of the index db
class HSDBRelation(HSDBField):
    # TODO: Extradite instances tracking to index database instead? since its basically indexing?
    _instances:dict['HSDBRelation']=dict() # Class-level dict that tracks existing instances by relation_name
    primary_keys:List[str]
    primary_model:type
    relation_name:type
    relation_type:type
    relation_key:str
    reverse_lookup:str
    secondary_keys:List[str]
    secondary_model:type
    
    def __new__(cls, *args, **kwargs):
        # Kwargs not working for some reason, so using args instead
        # relation_name = cls._stitch_relation_name(kwargs.get('primary_model'), kwargs.get('secondary_model'), kwargs.get('relation_type'))
        relation_name = cls._stitch_relation_name(args[1], args[3], args[4])
        
        if relation_name in cls._instances:
            instance = cls._instances[relation_name]
            for primary_key in args[0]:
                if primary_key not in instance.primary_keys:
                    instance.addPrimaryKey(primary_key)
            for secondary_key in args[2]:
                if secondary_key not in instance.secondary_keys:
                    instance.addSecondaryKey(secondary_key)
            return instance
        
        print('Creating new instance')
        
        instance = super().__new__(cls)
        print(instance)
        cls._instances[relation_name] = instance
        return instance
    
    def __init__(self,
                 primary_keys:List[str],
                 primary_model:type,
                 secondary_keys:List[str],
                 secondary_model:type,
                 relation_type:type,
                 reverse_lookup:str,
                 editable:bool=True,
                 relation_key:str='id',
                 required:bool=False) -> None:
        if hasattr(self, 'initialized'): # Prevent reinitialization on existing instance
            return
        
        super().__init__(editable, True, required)
        
        self.primary_model = primary_model
        self.relation_key = relation_key
        self.reverse_lookup = reverse_lookup
        self.secondary_model = secondary_model
        
        self.setPrimaryKeys(primary_keys)
        self.setSecondaryKeys(secondary_keys)
        
        self.initialized = True  # Flag to prevent reinitialization
        self.relation_name = self._stitch_relation_name(primary_model, secondary_model, relation_type)
        self._value = self._query_closure
    
    @property
    def _query_closure(self):
        query = HSDBQuery(self)
        subset = {key:query._index_db_reference[key] for key in query._index_db_reference if key in self.secondary_keys}
        query._index_db_reference = subset
        query.model = self.secondary_model
        # query._index_db_reference = {{entry.id:entry for entry in self.secondary_model.query.all()}}
        return query

    def __get__(self, instance, owner):
        if self._wrapper is None:
            self._wrapper = self._RelationWrapper(self._value, self)
        return self._wrapper
    
    @staticmethod
    def _stitch_relation_name(primary_model, secondary_model, relation_type):
        return f'{primary_model.__name__}_{relation_type}_{secondary_model.__name__}'
            
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
        def __init__(self, value:any, field:str):
            super().__init__(value, field, _AVAILABLE_FIELDS)
    
    class _RelationFactory(ABC):
        editable:bool
        relation_key:str
        relation_type:str
        required:bool
        reverse_lookup:str
        secondary_model:type
        
        def __init__(self,
                     secondary_model:type,
                     editable:bool=True,
                     relation_key:str='id',
                     required:bool=False,
                     reverse_lookup:str=None) -> None:
            self.editable = editable
            self.relation_key = relation_key
            self.required = required
            self.secondary_model = secondary_model
            
            self.relation_type = kebabify(self.__class__.__name__)
            if reverse_lookup is not None:
                self.reverse_lookup = reverse_lookup
            else:
                self.reverse_lookup = kebabify(secondary_model.__name__, replace=('-model', ''))
            
        def lazy_init(self,
                      primary_keys:List[str],
                      primary_model:type,
                      secondary_keys:List[str]) -> 'HSDBRelation':
            self.apply_ruleset(primary_keys, secondary_keys)
            return HSDBRelation(primary_keys,
                                primary_model,
                                secondary_keys,
                                self.secondary_model,
                                self.relation_type,
                                self.reverse_lookup,
                                self.editable,
                                self.relation_key,
                                self.required)
            
        #########
        # Hooks #
        #########
            
        def apply_ruleset(self, primary_keys:List[str], secondary_keys:List[str]) -> None:
            return
    
    class OneToOne(_RelationFactory):
        def apply_ruleset(self, primary_keys:List[str], secondary_keys:List[str]) -> None:
            if len(primary_keys) > 1 or len(secondary_keys) > 1:
                raise ValueError('One to one relation can only have one entry')

    class OneToMany(_RelationFactory):
        def apply_ruleset(self, primary_keys:List[str], secondary_keys:List[str]) -> None:
            if len(primary_keys) > 1:
                raise ValueError('One to many relation can only have one primary key entry')

    class ManyToMany(_RelationFactory):
        pass