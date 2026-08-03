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

# Standard-library imports
from abc import ABC, abstractmethod
from typing import Generic, List, Type, TypeVar

_AVAILABLE_FIELDS = [
    'cls',
    'editable',
    'instance',
    'indexed',
    'key',
    'required',
    'type',
    'value'
]
# Type alias for attribute types
T = TypeVar('T')

# TODO: Try to do automatic type checking and assignment in ValueWrapper as well
# TODO: Implement support for dicts and lists (potentially dangerous though)
class HSDBField(ABC, Generic[T]):
    _cached_value:object        # Cache for the field value
    _key:str                    # internal storage for key
    _value:object               # internal storage for value
    _wrapper:'_ValueWrapper'    # internal storage for value wrapper
    editable:bool               # Whether the attribute can be edited, automatically set to False if computed
    indexed:bool                # Whether the attribute is indexed
    key:str                     # Property for the field key
    name:str                    # The field name, used by HSDBModel to key values in `_fields`
    required:bool               # Whether the attribute is required, automatically set to True if computed
    shortkey:str                # The short key for the attribute, useful for compression
    type:T                      # The type of the attribute
    value:any                   # Property for the field value

    def __init__(self,
                 editable:bool,
                 indexed:bool,
                 required:bool,
                 type:Type,
                 SUPPORTED_TYPES:List[Type]) -> None:
        # Manual type checking to complement static type checking
        if type not in SUPPORTED_TYPES:
            raise ValueError(f'Unsupported type: {type.__name__}, supported types are: {SUPPORTED_TYPES}')
        if not isinstance(editable, bool):
            raise ValueError('editable must be a boolean')
        if not isinstance(indexed, bool):
            raise ValueError('indexed must be a boolean')
        if not isinstance(required, bool):
            raise ValueError('required must be a boolean')
        
        self.editable = editable
        self.indexed = indexed
        self.required = required
        self.type = type
        
        self._cached_value = None
        self._key = None
        self._value = None
        self._wrapper = None
        self.name = None
        
    def __set_name__(self, owner, name):
        """Automatically assigns the field name and default key when the class is created."""
        self.name = name
        self._key = name # Set the key to the field name by default
        
    ##############
    # Properties #
    ##############
    
    @property
    def cls(self):
        return self.__class__
    
    @property
    def instance(self):
        return self

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, new_key:str):
        if not isinstance(new_key, str) or not new_key:
            raise ValueError('key must be a string')
        self._key = new_key

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value:any):
        # Validation is intentionally skipped here: HSDBModel assigns values to
        # computed attributes (e.g. id, created_at) directly, which would otherwise
        # always fail the "computed attributes are read-only" check in _validate_value.
        self._value = new_value
        
    ######################
    # Descriptor Methods #
    ######################
    
    def __set__(self, instance, value):
        # Same validation caveat as the `value` setter above applies here.
        self._value = value
        self._wrapper = None # Invalidate the cached wrapper
        
    #############
    # Internals #
    #############

    class _ValueWrapper(ABC):
        """
        Wrapper that stores both the value and the field pointer reference.
        """
        cache_values:dict # Cache for the field values, populated per-instance in __init__

        def __init__(self, value:any,
                     field:'HSDBField',
                     additional_available_fields:List[str]=[],
                     available_functions:List[str]=[]):
            self._value = value
            self._field = field
            
            self.cache_values = {}
            self._cached_metadata = None
            self._metadata_loaded = False
            
            available_fields = _AVAILABLE_FIELDS + additional_available_fields
            for prop in available_fields:
                self.cache_values[prop] = getattr(self._field, prop)
            
            # The properties/aliases are the same for every instance of a given wrapper
            # subclass, so only build them once instead of redefining them on every access
            if '_properties_built' not in self.__class__.__dict__:
                # Dynamically create properties that fetch from metadata
                for prop in available_fields:
                    setattr(self.__class__, prop, property(lambda self, p=prop: self._load_metadata().get(p)))
                # Dynamically create function aliases
                for func in available_functions:
                    setattr(self.__class__, func, lambda self, f=func: getattr(self._field, f)())
                self.__class__._properties_built = True

        def __repr__(self):
            return repr(self._value)

        def __str__(self):
            return str(self._value)
        
        def _load_metadata(self):
            """
            Load the metadata (lazy loading).
            """
            if not self._metadata_loaded:
                # Cache the metadata to avoid reloading it
                self._cached_metadata = {
                    'cls': self._field.cls,
                    'key': self._field.key
                }
                
                # Add the cached values to the metadata
                for cache_key, cache_value in self.cache_values.items():
                    self._cached_metadata[cache_key] = cache_value
                    
                del self.cache_values
                self._metadata_loaded = True
            return self._cached_metadata