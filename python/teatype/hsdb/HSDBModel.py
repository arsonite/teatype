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
from abc import ABC

# From package imports
from teatype.hsdb import HSDBAttribute, HSDBMeta, HSDBQuery
from teatype.hsdb.util import parse_name
from teatype.util import dt, staticproperty

# From-as package imports
from teatype.util import generate_id

# TODO: Try optimizing some questionable parts of the code
# TODO: Implement additional HSDBField as descriptor to allow direct access of attributes without specifying .value
# TODO: Add validation method inside model
# TODO: Add attribute supports
# TODO: Add language supports
class HSDBModel(ABC, metaclass=HSDBMeta):
    # TODO: Implement these as computed properties
    # _app_name:str
    _attribute_cache = {} # Cache to store attributes once for each class
    _overwrite_path:str
    _overwrite_name:str
    _overwrite_plural_name:str
    _path:str
    _name:str
    _plural_name:str
    _relations:dict
    
    # migrated_at:dt
    # migration_app_name:str
    # migration_id:int
    # migration_name:str
    
    cls:type['HSDBModel']
    
    # app_name     = HSDBAttribute(str,  editable=False) # TODO: Maybe make this as a computed python property?
    created_at   = HSDBAttribute(dt,   computed=True)
    id           = HSDBAttribute(str,  computed=True, unique=True)
    # is_fixture   = HSDBAttribute(bool, computed=True) # TODO: Maybe make this as a computed python property?
    # migration_id = HSDBAttribute(int,  computed=True) # TODO: Maybe make this as a computed python property?
    # synced_at    = HSDBAttribute(dt,   computed=True)
    updated_at   = HSDBAttribute(dt,   computed=True)
    # was_synced   = HSDBAttribute(bool, computed=True)
    
    def __init__(self,
                 data:dict,
                 include_base_attributes:bool=True,
                 overwrite_path:str=None):
        # For every class variable that is an HSDBAttribute,
        # create an instance deepcopy, assign its key to the variable name,
        # and, if the field is provided in the data dict, set its value.
        # Necessary to avoid sharing the same attribute instance across all instances.
        # Look up cached attributes for this class
        # Cache the attributes if not already cached
        if self.__class__ not in self._attribute_cache:
            self._cache_attributes()

        # DEPRECATED: Do I even need this anymore?
            # self._fields = {} # Store actual field values
            # for field_name, field in self.__class__.__dict__.items():
            #     if isinstance(field, HSDBAttribute):
            #         if field.required and field_name not in data:
            #             raise ValueError(f"Missing required field: {field_name}")
            #         setattr(self, field_name, data.get(field_name, None))
            
            # Initialize the attributes (lazy loading and caching for values)
            # for attribute_name in self._attribute_cache[self.__class__]:
            #     # Get the attribute from the cache
            #     attribute = self._attribute_cache[self.__class__].get(attribute_name)
            #     # Dynamically create the instance attribute
            #     instance_attribute = HSDBAttribute(
            #         attribute.type, 
            #         **{key: value for key, value in vars(attribute).items() if key not in [
            #             'name', 'type', '_cached_value', '_key', '_value', '_wrapper']} # Exclude these keys
            #     )
            #     instance_attribute.key = attribute_name  # Set the key to the attribute name
                
            #     # Set value if data is provided
            #     if attribute_name in data:
            #         if hasattr(instance_attribute, 'computed') and instance_attribute.computed:
            #             raise ValueError(f'{attribute_name} is computed and cannot be set')
            #         instance_attribute.value = data.get(attribute_name)
                
            #     # Assign to the instance
            #     setattr(self, attribute_name, instance_attribute) # Set the attribute to the instance
        
        # Create a dict to hold instance-specific field values
        self._fields = {}
        for attribute_name, attribute in self._attribute_cache[self.__class__].items():
            # Dynamically create the instance attribute
            instance_attribute = HSDBAttribute(
                attribute.type, 
                **{key: value for key, value in vars(attribute).items() if key not in [
                    'name', 'type', '_cached_value', '_key', '_value', '_wrapper']} # Exclude these keys
            )
            instance_attribute.key = attribute_name
            if attribute_name in data:
                # Validate type before assignment
                if not isinstance(data[attribute_name], attribute.type):
                    raise ValueError(f'Field "{attribute_name}" must be of type {attribute.type.__name__}')
                if attribute.computed:
                    raise ValueError(f'{attribute_name} is computed and cannot be set')
                attribute_value = data.get(attribute_name)
                instance_attribute.value = attribute_value
                
                setattr(self, attribute_name, attribute_value)
                # self._fields[attribute_name] = instance_attribute
            
        # Model name and pluralization
        self._model_name = type(self).__name__ 
        self._name = parse_name(self._model_name, remove='-model', plural=False)
        self._plural_name = parse_name(self._model_name, remove='-model', plural=True)

        # Validation after initialization
        for attribute_name, attr in self.__dict__.items():
            if isinstance(attr, HSDBAttribute):
                if attr.required and not attr.value:
                    raise ValueError(f'Model "{self._model_name}" init error: attribute "{attribute_name}" is required')
        
        # TODO: Find a more elegant solution than this ugly a** hack
        # self.id.instance.__computational_override__(generate_id(truncate=5))
        self.id = generate_id(truncate=64)
        
        current_time = dt.now()
        self.created_at = current_time
        self.updated_at = current_time
            
        if overwrite_path:
            self._path = overwrite_path
        self._path = f'{self._plural_name}/{self.id}.json'
        
        self.cls = self.__class__
        
        # TODO: Make this dynamic
        # self.app_name = 'raw'
        # self.migration_id = 1
    
    # TODO: Get cache working again
    def __getattribute__(self, name):
        # If the field name is in our field cache, return the value from _fields
        _cache = object.__getattribute__(self, '_attribute_cache')
        cls = type(self)
        if cls in _cache and name in _cache[cls]:
            return object.__getattribute__(self, '_fields').get(name).__get__(self, self.__class__)
        return object.__getattribute__(self, name)

    def __setattr__(self, name, value):
        _cache = self.__class__._attribute_cache.get(self.__class__, {})
        if name in _cache:
            attribute = _cache[name]
            # TODO: Fix validation
            # if attribute.computed and self._fields.get(name) is not None:
            #     raise ValueError(f'Attribute "{name}" is computed and cannot be set manually')
            # if not isinstance(value, attribute.type):
            #     raise ValueError(f'Field "{name}" must be of type {attribute.type.__name__}')
            # attribute.__set__(self, value)
            instance_attribute = HSDBAttribute(
                attribute.type, 
                **{key: value for key, value in vars(attribute).items() if key not in [
                    'name', 'type', '_cached_value', '_key', '_value', '_wrapper']} # Exclude these keys
            )
            instance_attribute.key = attribute.name
            instance_attribute.value = value
            self.__dict__.setdefault('_fields', {})[name] = instance_attribute
        else:
            super().__setattr__(name, value)
    
    # TODO: Optimization
    def _cache_attributes(self):
        """
        Cache the attributes for this class (including its ancestors).
        """
        self._attribute_cache[self.__class__] = {}
        seen = set()

        # Traverse through the method resolution order to gather attributes
        for cls in reversed(self.__class__.__mro__):
            for attribute_name, attribute in cls.__dict__.items():
                if attribute_name in seen:
                    continue
                if isinstance(attribute, HSDBAttribute):
                    seen.add(attribute_name)
                    self._attribute_cache[self.__class__][attribute_name] = attribute
                    
    @property
    def serializer(self) -> dict:
        """
        If this method is not overridden, collect all HSDBAttribute fields.
        If this method is overridden, collect all fields that are not computed.
        """
        serialized = dict()
        for attribute_name in self.__dict__['_fields']:
            # Skip non-HSDBAttribute fields
            try:
                if attribute_name in self._fields:
                    serialized[attribute_name] = getattr(self, attribute_name)
            except Exception as exc:
                continue
        return serialized
        
    @staticproperty
    def query(self):
        # Always return a new query builder instance when query is accessed.
        return HSDBQuery(self.__class__)
    
    # TODO: Optimization
    # TODO: Group data with key and base data into index data
    @staticmethod
    def serialize(object:object,
                  fuse_data:bool=False,
                  include_migration:bool=True,
                  include_model:bool=True,
                  json_dump:bool=False,
                  strip_attributes:bool=False,
                  use_data_key:bool=False) -> dict|str:
        serialized_data = object.serializer
        return serialized_data
    
        serialized_data = dict()
            
        if fuse_data:
            return {**base_data, **serializer}
        else:
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
                'model_name': self._model_name,
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
    
    ##################
    # Static methods #
    ##################
    
    @staticmethod
    def load(self, dict_data:dict):
        pass