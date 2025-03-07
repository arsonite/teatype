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

# From package imports
from teatype.hsdb import HSDBRelation

# Type alias for attribute types
T = type

class HSDBAttribute:
    computed:bool # Whether the attribute is computed
    description:str # Description of the attribute
    editable:bool # Whether the attribute can be edited
    indexed:bool # Whether the attribute is indexed
    key:str # The attribute key
    max_size:int # Maximum size of the attribute value (only relevant for strings)
    relation:HSDBRelation # Relation object if attribute is a relation
    required:bool # Whether the attribute is required
    searchable:bool # Whether the attribute is searchable
    type:T # holds an actual Python type, e.g. str, int, etc.
    unique:bool # Whether the attribute value must be unique

    def __init__(self,
                 type:T,
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
        self.editable = editable
        self.indexed = indexed
        self.max_size = max_size
        self.relation = relation
        self.required = required
        self.searchable = searchable
        self.type = type
        self.unique = unique
        
        if not isinstance(type, T):
            raise ValueError('type must be a Python type, e.g. str, int, etc.')
        if not isinstance(computed, bool):
            raise ValueError('computed must be a boolean')
        if not isinstance(description, str):
            raise ValueError('description must be a string')
        if not isinstance(editable, bool):
            raise ValueError('editable must be a boolean')
        if not isinstance(indexed, bool):
            raise ValueError('indexed must be a boolean')
        if not isinstance(max_size, int):
            raise ValueError('max_size must be an integer')
        if not isinstance(relation, HSDBRelation):
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
        self._value = new_value