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

# TODO: Add validation method inside model
# TODO: Add attribute supports
# TODO: Add language supports
class HSDBModel(ABC):
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
    
    app_name=HSDBAttribute(editable=False, type=str)
    created_at=HSDBAttribute(computed=True, type=dt)
    id=HSDBAttribute(computed=True, unique=True, type=str)
    is_fixture=HSDBAttribute(editable=False, type=bool)
    migration_id=HSDBAttribute(editable=False, type=int)
    synced_at=HSDBAttribute(computed=True, type=dt)
    updated_at=HSDBAttribute(computed=True, type=dt)
    was_synced=HSDBAttribute(editable=False, type=bool)
    app_name:str
    created_at:dt
    id:str
    is_fixture:bool=False
    model_name:str
    synced_at:dt
    updated_at:dt
    was_synced:bool=False
    
    def __init__(self,
                 data:dict,
                 overwrite_path:str=None):
        # For every class variable that is an HSDBAttribute,
        # create an instance copy, assign its key to the variable name,
        # and, if the field is provided in the data dict, set its value.
        # Necessary to avoid sharing the same attribute instance across all instances.
        for attr_name, attr in self.__class__.__dict__.items():
            if isinstance(attr, HSDBAttribute):
                instance_attr = copy.copy(attr)
                instance_attr.key = attr_name
                if attr_name in data:
                    instance_attr.value = data[attr_name]
                setattr(self, attr_name, instance_attr)
                
        return # TODO: Temporary
            
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
        
    @property
    @staticmethod
    def query(self):
        # Always return a new query builder instance when query is accessed.
        return HSDBQuery(self.__class__)

    def serialize(self,
                  fuse_data:bool=False,
                  include_migration:bool=True,
                  include_model:bool=True,
                  json_dump:bool=False,
                  use_data_key:bool=False) -> dict|str:
        serializer = self.serializer()
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
    def loads(self, dict_data:dict):
        pass
    
    #########
    # Hooks #
    #########
    
    def serializer(self) -> dict:
        # If this method is not overridden, collect all HSDBAttribute fields.
        serialized = {}
        for attr_name, attr in self.__dict__.items():
            if isinstance(attr, HSDBAttribute):
                serialized[attr_name] = attr.value
        return serialized

# -------- Sample usage --------
if __name__ == '__main__':

    # Assume these are your models derived from BaseModel.
    class Student(HSDBModel):
        age = HSDBAttribute(type=int)
        height = HSDBAttribute(type=int, description='Height in cm')
        name = HSDBAttribute(type=str)
        # school = HSDBAttribute(type=HSDBRelation)

    # Create model instances
    student_A = Student({'age': 25, 'height': 160, 'name': 'jennifer'})
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
    #         "model_name": "Student"
    #     }
    # }
    print(student_A.serialize(json_dump=True)) 
    
    # Execution delimiter
    import sys
    sys.exit(0)

    # Create a query chain that does not execute immediately.
    query = Student.query.all().sort_by('age').filter_by('name').where('height').greater_than(150)
    # query is now a representation like:
    print(query) # e.g. <HSDBQuery conditions=[('name', '==', ...?), ('height', '>', 150)] sort_by=age>
    
    # Simulate a simple in-memory db:
    db = {
        '1': {'name': 'jennifer', 'age': 25, 'height': 160, 'school': 41},
        '2': {'name': 'alice',    'age': 22, 'height': 155, 'school': 42},
        '3': {'name': 'jennifer', 'age': 19, 'height': 158, 'school': 42},
        
        '41': {'name': 'Central High', 'address': 'Central Street 21'},
        '42': {'name': 'Howard High', 'address': 'Howard Avenue 12'}
    }
    
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