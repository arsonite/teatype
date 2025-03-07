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
import sys

# From system imports
from typing import Generic, Type, TypeVar

# From package imports
from teatype.hsdb import HSDBRelation
from teatype.util import dt

# Type alias for attribute types
T = TypeVar('T')

# Supported attribute types
_SUPPORTED_TYPES = [bool, dt, float, int, str]

# TODO: Implement support for dicts and lists (potentially dangerous though)
class HSDBAttribute(Generic[T]):
    computed:bool         # Whether the attribute is computed, more of a flavour attribute, laxily enforced
    description:str       # Description of the attribute
    editable:bool         # Whether the attribute can be edited, automatically set to False if computed
    indexed:bool          # Whether the attribute is indexed
    key:str               # The attribute key
    max_size:int          # Maximum size of the attribute value (only relevant for strings)
    relation:HSDBRelation # Relation object if attribute is a relation
    required:bool         # Whether the attribute is required
    searchable:bool       # Whether the attribute is searchable
    type:T                # holds an actual Python type, e.g. str, int, etc.
    unique:bool           # Whether the attribute value must be unique

    def __init__(self,
                 type:Type[T],
                 computed:bool=False,
                 description:str=None,
                 editable:bool=True,
                 indexed:bool=False,
                 max_size:int=sys.maxsize,
                 relation:HSDBRelation=None,
                 required:bool=False,
                 searchable:bool=False,
                 unique:bool=False):
        self.computed = computed
        self.description = description
        self.editable = False if computed else editable
        self.indexed = indexed
        self.max_size = max_size
        self.relation = relation
        self.required = required
        self.searchable = searchable
        self.type = type
        self.unique = unique
        
        if type not in _SUPPORTED_TYPES:
            raise ValueError(f'Unsupported type: {type.__name__}, supported types are: {_SUPPORTED_TYPES}')
        if not isinstance(computed, bool):
            raise ValueError('computed must be a boolean')
        if not isinstance(description, str) and description != None:
            raise ValueError('description must be a string')
        if not isinstance(editable, bool):
            raise ValueError('editable must be a boolean')
        if not isinstance(indexed, bool):
            raise ValueError('indexed must be a boolean')
        if not isinstance(max_size, int):
            raise ValueError('max_size must be an integer')
        if not isinstance(relation, HSDBRelation) and relation != None:
            raise ValueError('relation must be an instance of HSDBRelation')
        if not isinstance(required, bool):
            raise ValueError('required must be a boolean')
        if not isinstance(searchable, bool):
            raise ValueError('searchable must be a boolean')
        if not isinstance(unique, bool):
            raise ValueError('unique must be a boolean')
        if max_size < 0:
            raise ValueError('max_size must be a positive integer')

        self._key = None # internal storage for key
        self._value = None # internal storage for value
        
    def __repr__(self):
        return f'HSDBAttribute(key={self.key}, value={self.value}, type={self.type.__name__})'
    
    def __computational_override__(self, value:any):
        """
        This method is used to override the value of a computed attribute.
        Do not use this method unless you know what you are doing.
        It has not validation checks and assumes that the value is of the correct type and 
        whoever is calling this method knows what they are doing.
        """
        self.value = value

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value

    @key.setter
    def key(self, new_key:str):
        if self._key is not None:
            raise ValueError('key is already set')
        if not isinstance(new_key, str) or not new_key:
            raise ValueError('key must be a non-empty string')
        self._value = new_key

    @value.setter
    def value(self, new_value:any):
        # Check that new_value is of the expected type
        if not isinstance(new_value, self.type):
            raise ValueError(
                f'Value for attribute "{self.key}" must be of type {self.type.__name__}'
            )

        # Additional check: if value is a string, enforce max_size if applicable.
        if self.type is str and len(new_value) > self.max_size:
            raise ValueError(
                f'Value for attribute "{self.key}" exceeds maximum size ({self.max_size})'
            )
            
        if not self.editable and self._value is not None:
            raise ValueError(f'Attribute "{self.key}" is not editable after it has been set once')
        
        if self.computed and self._value is not None:
            raise ValueError(f'Attribute "{self.key}" is computed and cannot be set manually')
        
        self._value = new_value
        
    #################
    # Class methods #
    #################
    
    @classmethod
    def __class_getitem__(cls, item: Type[T]):
        return cls