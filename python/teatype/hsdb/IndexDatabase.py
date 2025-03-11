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
import threading

# From system imports
from typing import List

# From package imports
from pympler import asizeof
from teatype.hsdb import HSDBQuery

class _MemoryFootprint:
    def __init__(self, index_database:object):
        self.size_in_bytes = asizeof.asizeof(self._db)
        self.size_in_kilo_bytes = self.size_in_bytes / 1024
        self.size_in_mega_bytes = self.size_in_kilo_bytes / 1024
        print('index db memory footprint:', round(asizeof.asizeof(self._db / 1024 / 1024), 2), 'MB')
        
    def print(self):
        print('Index db memory footprint:')
        print('     size in bytes:', self.size_in_bytes)
        print('     size in kilo bytes:', self.size_in_kilo_bytes)
        print('     size in mega bytes:', self.size_in_mega_bytes)
        
class IndexDatabase:
    _cache_register:dict # For all cache values
    _cache_register_lock:threading.Lock
    _compute_index:dict # For all compute values for easy modification
    _compute_index_lock:threading.Lock
    _db:dict # For all raw data
    _db_lock:threading.Lock
    _indexed_fields:dict # For all indexed fields for faster query lookups
    _indexed_fields_lock:threading.Lock
    _model_index:dict # For all model references for faster model query lookups
    _model_index_lock:threading.Lock
    _relational_index:dict # For all relations between models parsed dynamically from the model definitions
    _relational_index_lock:threading.Lock
    models:List[type] # For all models
    use_cache:bool # Whether to use cache for faster lookups
    use_compute_index:bool # Whether to use compute index for faster lookups
    use_indexed_fields:bool # Whether to use indexed fields for faster lookups
    use_model_index:bool # Whether to use model index for faster lookups
    use_pointer_reference:bool # Indicates whether to use pointer reference of foreign objects or ids
    use_relational_index:bool # Whether to use relational index for faster lookups
    
    def __init__(self,
                 models:List[type],
                 use_cache:bool=True,
                 use_compute_index:bool=True,
                 use_indexed_fields:bool=True,
                 use_model_index:bool=True,
                 use_pointer_reference:bool=False,
                 use_relational_index:bool=True):
        self.models = models
        self.use_cache = use_cache
        self.use_compute_index = use_compute_index
        self.use_indexed_fields = use_indexed_fields
        self.use_model_index = use_model_index
        self.use_pointer_reference = use_pointer_reference
        self.use_relational_index = use_relational_index
        
        if use_cache:
            self._cache_register = dict()
            self._cache_register_lock = threading.Lock()
        
        if use_compute_index:
            self._compute_index = dict()
            self._compute_index_lock = threading.Lock()
        
        if use_indexed_fields:
            self._indexed_fields = dict()
            self._indexed_fields_lock = threading.Lock()
        
        if use_model_index:
           self._model_index = dict()
           self._model_index_lock = threading.Lock()
        
        if use_relational_index:
            self._relational_index = dict()
            self._relational_index_lock = threading.Lock()
        
        self._db = dict()
        self._db_lock = threading.Lock()
        
    ##############
    # Properties #
    ##############
        
    @property
    def memory_footprint(self) -> _MemoryFootprint:
        return _MemoryFootprint(self)
        
    ##################
    # ORM Operations #
    ##################
                
    def create_entry(self, model:type, data:dict, parse:bool=False) -> object|None:
        try:
            with self._db_lock:
                if parse:
                    data = {
                        **data.get('base_data'),
                        **data.get('data')
                    }
                # TODO: Validation
                model_instance = model(**data)
                model_name = model_instance.model_name
                with self._model_index_lock:
                    if model_name not in self._model_index:
                        self._model_index[model_name] = {}
                
                model_id = model_instance.id
                if model_id in self._db:
                    return None
                
                # Model.create(root_path, model_instance)
                # TODO: Quick and dirty hack, need to refactor this with proper attributes
                # need for algorithm to be implemented with the model callhandlers
                match model_name:
                    # case 'CameraModel':
                    #     pass
                    # case 'ImageModel':
                    #     pass
                    case 'InstrumentModel':
                        existing_match = next(
                            (
                                obj
                                for obj in self._db.values()
                                if getattr(obj, 'model_name', None) == 'InstrumentModel'
                                and getattr(obj, 'article_number', None) == data.get('article_number')
                                and getattr(obj, 'manufacturer', None) == data.get('manufacturer')
                                # and getattr(obj, 'manufacturer_id', None) == data.get('manufacturer_id')
                            ),
                            None,
                        )
                        if existing_match:
                            return None
                    case 'InstrumentTypeModel':
                        existing_match = next(
                            (
                                obj
                                for obj in self._db.values()
                                if getattr(obj, 'model_name', None) == 'InstrumentTypeModel'
                                and getattr(obj, 'name', None) == data.get('name')
                            ),
                            None,
                        )
                        if existing_match:
                            return None
                    # case 'LabelModel':
                    #     pass
                    case 'ManufacturerModel':
                        existing_match = next(
                            (
                                obj
                                for obj in self._db.values()
                                if getattr(obj, 'model_name', None) == 'ManufacturerModel'
                                and getattr(obj, 'name', None) == data.get('name')
                            ),
                            None,
                        )
                        if existing_match:
                            return None
                    case 'SurgeryTypeModel':
                        existing_match = next(
                            (
                                obj
                                for obj in self._db.values()
                                if getattr(obj, 'model_name', None) == 'SurgeryTypeModel'
                                and getattr(obj, 'name', None) == data.get('name')
                            ),
                            None,
                        )
                        if existing_match:
                            return None
                        
                self._db[model_id] = model_instance
                return model_instance
        except:
            import traceback
            traceback.print_exc()
            return None
        
    # TODO: Query optimization with indices
    def get_entries(self, model:type, serialize:bool=False) -> List[object]:
        entries = []
        with self._db_lock:
            for entry_id in self._db:
                entry = self._db[entry_id]
                if entry.model_name == model.__name__:
                    if serialize:
                        entries.append(entry.serialize())
                        continue
                    entries.append(entry)
        return entries
    
    def get_entry(self, model_id:str, serialize:bool=False) -> object|None:
        with self._db_lock:
            entry = self._db.get(model_id)
            if serialize:
                return entry.serialize()
            return entry
    
    def execute_query(self, query:HSDBQuery, return_ids:bool=False):
        """
        Execute a query representation on an in-memory db.

        Parameters:
        query: HSDBQuery instance with conditions and sort_key.
        return_ids: If True, return only the identifiers. If False, return the data.

        Returns:
        List of identifiers that match the query if return_ids is True.
        List of data that match the query if return_ids is False.
        """
        def get_nested_value(data, attribute_path):
            parts = attribute_path.split('.')
            value = data
            for part in parts:
                if not isinstance(value, dict):
                    # Look up the referenced record in the db using string key.
                    reference = str(value)
                    if reference in self._db and isinstance(self._db[reference], dict):
                        value = self._db[reference]
                    else:
                        # If reference not found, return None.
                        return None
                value = value.get(part)
            return value

        def condition_matches(data, condition):
            attribute, operator, expected = condition
            actual_attribute = get_nested_value(data, attribute)
            actual_value = actual_attribute._value
            if operator == '==':
                return actual_value == expected
            elif operator == '<':
                return actual_value is not None and actual_value < expected
            elif operator == '>':
                return actual_value is not None and actual_value > expected
            else:
                raise ValueError(f'Unsupported operator {operator}')

        # First filter using conditions.
        results = []
        for identifier, data in self._db.items():
            print(data)
            if data.get('model_name') != query.model_class:
                continue
            if all(condition_matches(data, condition) for condition in query.conditions):
                if return_ids:
                    results.append(identifier)
                else:
                    results.append(data)
        # Sort the results if needed.
        if query.sort_key:
            results.sort(key=lambda item: get_nested_value(item[1], query.sort_key))
        # Return list of identifiers.
        return [item[0] for item in results]