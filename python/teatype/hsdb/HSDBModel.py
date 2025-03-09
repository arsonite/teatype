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
import copy
import json

# From system imports
from abc import ABC, abstractmethod

# From package imports
from teatype.hsdb import HSDBAttribute, HSDBQuery, HSDBRelation
from teatype.hsdb.util import parse_name
from teatype.io import env
from teatype.util import dt

# From-as package imports
from teatype.util import id as generate_id

# TODO: Implement additional HSDBField as descriptor to allow direct access of attributes without specifying .value
# TODO: Add validation method inside model
# TODO: Add attribute supports
# TODO: Add language supports
class HSDBModel(ABC):
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
    
    app_name     = HSDBAttribute(str,  editable=False) # TODO: Maybe make this as a computed python property?
    created_at   = HSDBAttribute(dt,   computed=True)
    id           = HSDBAttribute(str,  computed=True, unique=True)
    is_fixture   = HSDBAttribute(bool, computed=True) # TODO: Maybe make this as a computed python property?
    migration_id = HSDBAttribute(int,  computed=True) # TODO: Maybe make this as a computed python property?
    synced_at    = HSDBAttribute(dt,   computed=True)
    updated_at   = HSDBAttribute(dt,   computed=True)
    was_synced   = HSDBAttribute(bool, computed=True)
    
    def __init__(self,
                 data:dict,
                 overwrite_path:str=None):
        # For every class variable that is an HSDBAttribute,
        # create an instance deepcopy, assign its key to the variable name,
        # and, if the field is provided in the data dict, set its value.
        # Necessary to avoid sharing the same attribute instance across all instances.
        # Look up cached attributes for this class
        if self.__class__ not in self._attribute_cache:
            self._cache_attributes()

        # Initialize the attributes
        # TODO: Maybe use vars(self) instead of self.__dict__
        for attribute_name in self._attribute_cache[self.__class__]: 
            # Get the attribute from the cache
            attribute = self._attribute_cache[self.__class__][attribute_name]
            # Dynamically create the instance_attribute
            instance_attribute = HSDBAttribute(
                attribute.type, 
                # Exclude type, _key, and _value from the vars (using these for future expandibility)
                **{key: value for key, value in vars(attribute).items() if key not in ['type', '_key', '_value']}  
            )
            instance_attribute.key = attribute_name # Set the key to the attribute name

            # Set value if data is provided
            if attribute_name in data:
                if instance_attribute.computed:
                    raise ValueError(f'{attribute_name} is computed and cannot be set')
                instance_attribute.value = data[attribute_name]

            # Assign to the instance
            setattr(self, attribute_name, instance_attribute) # Set the attribute to the instance
        
        self._model_name = type(self).__name__ 
        # Validation after initialization
        for attribute_name, attr in self.__dict__.items():
            if isinstance(attr, HSDBAttribute):
                if attr.required and not attr.value:
                    raise ValueError(f'Model "{self._model_name}" init error: attribute "{attribute_name}" is required')
            
        self._name = parse_name(self._model_name, remove='-model', plural=False)
        self._plural_name = parse_name(self._model_name, remove='-model', plural=True)
        
        if self.id is None:
            self.id = generate_id(truncate=5)
            
        if overwrite_path:
            self._path = overwrite_path
        self._path = f'{self._plural_name}/{self.id.value}.json'
                
        if self.created_at.value:
            self.created_at = dt.fromist.fromisoformat(self.created_at.value)
        else:
            self.created_at = dt.now()
        if self.updated_at.value:
            self.updated_at = dt.fromisoformat(self.updated_at.value)
        else:
            self.updated_at = dt.now()
        
        # TODO: Make this dynamic
        self.app_name = 'raw'
        self.migration_id = 1
        
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
    @staticmethod
    def query(self):
        # Always return a new query builder instance when query is accessed.
        return HSDBQuery(self.__class__)

    # TODO: Group data with key and base data into index data
    def serialize(self,
                  fuse_data:bool=False,
                  include_migration:bool=True,
                  include_model:bool=True,
                  json_dump:bool=False,
                  use_data_key:bool=False) -> dict|str:
        serializer = self.serializer()
        return serializer
    
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
    
    # TODO: Put this into IndexDatabase instead
    @staticmethod
    def execute_query(query:HSDBQuery, db_entries:dict):
        """
        Execute a query representation on an in-memory db.

        Parameters:
        query: HSDBQuery instance with conditions and sort_key.
        db_entries: dict with {identifier: data} where data is a dict of attributes.
                    Nested attributes (for relations) are obtained via lookup.
                    For example, a student record may store just the school id.

        Returns:
        List of identifiers that match the query.
        """
        def get_nested_value(data, attr_path):
            parts = attr_path.split('.')
            value = data
            for part in parts:
                if not isinstance(value, dict):
                    # Look up the referenced record in the db_entries using string key.
                    ref = str(value)
                    if ref in db_entries and isinstance(db_entries[ref], dict):
                        value = db_entries[ref]
                    else:
                        # If reference not found, return None.
                        return None
                value = value.get(part)
            return value

        def condition_matches(data, condition):
            attr, op, expected = condition
            actual = get_nested_value(data, attr)
            if op == '==':
                return actual == expected
            elif op == '<':
                return actual is not None and actual < expected
            elif op == '>':
                return actual is not None and actual > expected
            else:
                raise ValueError(f"Unsupported operator {op}")

        # First filter using conditions.
        results = []
        for identifier, data in db_entries.items():
            if all(condition_matches(data, cond) for cond in query.conditions):
                results.append((identifier, data))
        # Sort the results if needed.
        if query.sort_key:
            results.sort(key=lambda item: get_nested_value(item[1], query.sort_key))
        # Return list of identifiers.
        return [item[0] for item in results]
    
    @staticmethod
    def load(self, dict_data:dict):
        pass
    
    #########
    # Hooks #
    #########
    
    def serializer(self) -> dict:
        """
        If this method is not overridden, collect all HSDBAttribute fields.
        If this method is overridden, collect all fields that are not computed.
        """
        serialized = {}
        for attribute_name, attr in self.__dict__.items():
            if isinstance(attr, HSDBAttribute):
                serialized[attribute_name] = attr.value
        return serialized

# Sample usage
if __name__ == '__main__':
    import sys
    from pprint import pprint

    # Assume these are your models derived from BaseModel.
    class StudentModel(HSDBModel):
        age    = HSDBAttribute(int, required=True)
        height = HSDBAttribute(int, description='Height in cm', required=True)
        name   = HSDBAttribute(str, required=True)
        # school = HSDBAttribute(type=HSDBRelation)
        
    class SchoolModel(HSDBModel):
        address = HSDBAttribute(str, required=True)
        name    = HSDBAttribute(str, required=True)

    # Create model instances
    student_A = StudentModel({'age': 25, 'height': 160, 'name': 'jennifer jones'})
    # e.g. {
    #     "base_data": {
    #         "created_at": "2025-01-01T00:00:00",
    #         "id": "1",
    #         "updated_at": "2025-01-01T00:00:00"
    #     },
    #     "data": {
    #         "age": null,
    #         "height": null,
    #         "name": null,
    #         "school": null
    #     },
    #     "migration_data": {
    #         "app_name": "raw",
    #         "migration_id": 1
    #     },
    #     "model_data": {
    #         "app_name": "raw",
    #         "_model_name": "Student"
    #     }
    # }
    # student_B = StudentModel({'age': 18, 'height': 185, 'name': 'bob barker'})
    # student_C = StudentModel({'age': 21, 'height': 173, 'name': 'alice anderson'})
    
    # school_A = SchoolModel({'address': 'Central Street 21', 'name': 'Central High'})
    # school_B = SchoolModel({'address': 'Howard Avenue 12', 'name': 'Howard High'})
    
    # Simulate a simple in-memory db:
    db = {
        student_A.id.value: student_A.serialize(),
        # student_B.id.value: student_B.serialize(),
        # student_C.id.value: student_C.serialize(),
        # school_A.id.value: school_A.serialize(),
        # school_B.id.value: school_B.serialize()
    }
    pprint(db)
    
    sys.exit(0) # Execution delimiter

    # Create a query chain that does not execute immediately.
    query = Student.query.all().sort_by('age').filter_by('name').where('height').greater_than(150)
    # query is now a representation like:
    print(query) # e.g. <HSDBQuery conditions=[('name', '==', ...?), ('height', '>', 150)] sort_by=age>
    
    print()
    
    # Create a query with chained where's for bonus usage:
    query_obj = (
        m.query
         .where("name").equals("jennifer")
         .where("age").less_than(20)
         .where("school.name").equals("Howard High")
    )
    
    # Execute
    matching_ids = execute_query(query_obj, db)
    print("Matching ids:", matching_ids)