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
from typing import List, Union

# From package imports
from teatype.hsdb import HSDBModel, IndexDatabase

_OPERATOR_VERBS = [('eq', 'equals'),
                   ('ge', 'greater_than_or_equals'),
                   ('le', 'less_than_or_equals'),
                   ('lt', 'less_than'),
                   ('gt', 'greater_than')]

# TODO: Add support for running queries on querysets again after execution to allow reducing even further after initial query
class HSDBQuery:
    _already_executed:bool
    _conditions:List
    _current_attribute:str
    _filter_key:str
    _index_db_reference:IndexDatabase
    _index_id:str
    _model:HSDBModel
    _paginate:Union[int, int]
    _return_ids:bool
    _sort_key:str
    _sort_order:str
    
    def __init__(self, model:HSDBModel):
        # model is used later to help interpret attribute types and relations
        self.model = model
        
        self._aready_executed = False
        self._conditions = [] # list of (attribute_path, operator, value)
        self._current_attribute = None
        self._filter_key = None
        self._index_db_reference = IndexDatabase()
        self._index_id = None
        self._paginate = None
        self._return_ids = False
        self._sort_key = None
        self._sort_order = None

    def __repr__(self):
        return f"<HSDBQuery conditions={self._conditions} filter_key={self._filter_key} sort_by={self._sort_key}>"

    def _add_condition(self, op, value):
        if self._current_attribute is None:
            raise ValueError('No attribute specified. Call where() first.')
        # Each condition is stored with its attribute path, operator, and value.
        self._conditions.append((self._current_attribute, op, value))
        self._current_attribute = None
        
    def _block_executed_query(self, include_pending_condition:bool=False):
        # Including this check to prevent repetition of unnecessary code since all methods need to check for ran query anyways
        if include_pending_condition:
            if self._current_attribute is not None:
                raise ValueError('No value specified for attribute. Call a operator verb first: ' + ', '.join([v for k, v in _OPERATOR_VERBS]))
            
        if self._already_executed:
            raise ValueError('Query already executed. Call a new query property to start a new query.')
    
    def _run_query(self):
        """
        Execute a query representation on an in-memory db.

        Parameters:
        query: HSDBQuery instance with conditions and sort_key.

        Returns:
        List of identifiers that match the query if self._return_ids is True.
        List of data that match the query if self._return_ids is False.
        """
        def get_nested_value(data, attribute_path):
            parts = attribute_path.split('.')
            value = data
            for part in parts:
                if not isinstance(value, dict):
                    # Look up the referenced record in the db using string key.
                    reference = str(value)
                    if reference in self._index_db_reference._db and isinstance(self._index_db_reference._db[reference], dict):
                        value = self._index_db_reference._db[reference]
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
            
        self._block_pending_condition()

        # First filter using conditions.
        results = []
        for identifier, data in self._index_db_reference._db.items():
            if data.get('model_name') != self.model_class:
                continue
            if all(condition_matches(data, condition) for condition in self.conditions):
                if self.return_ids:
                    results.append(identifier)
                else:
                    results.append(data)
        # Sort the results if needed.
        if self.sort_key:
            results.sort(key=lambda item: get_nested_value(item[1], self.sort_key))
        if self.filter_key:
            results = [item for item in results if get_nested_value(item[1], self.filter_key)]
            
        self._already_executed = True
        
        # Return list of identifiers.
        return [item[0] for item in results]
    
    def sort_by(self, attribute_name:str, sort_order:str='asc'):
        self._block_executed_query(include_pending_condition=True)
        self._sort_key = attribute_name
        self._sort_order = sort_order
        return self

    def filter_by(self, attribute_name:str):
        self._block_executed_query()
        # Set the attribute to include in the query results.
        # When the query is executed, only records with this attribute will be returned 
        # as dictionaries containing just that attribute.
        self._filter_key = attribute_name
        return self
    
    def return_ids(self):
        self._block_executed_query()
        self._return_ids = True
        return self
    
    ###################
    # Execution hooks #
    ###################
    
    def __iter__(self):
        """
        Trigger execution when iterating.
        """
        self._block_executed_query()
        return iter(self._execute())

    def __len__(self):
        """
        Trigger execution when len() is called.
        """
        self._block_executed_query()
        return len(self._execute())

    def __getitem__(self, index):
        """
        Trigger execution when accessing an item.
        """
        self._block_executed_query()
        return self._execute()[index]

    def all(self):
        self._block_executed_query()
        # Calling all resets any previous conditions
        self._conditions = []
        return self._execute()
    
    def collect(self):
        """
        Forcing the query to execute and return the results without any special actions.
        """
        self._block_executed_query()
        return self._execute()
    
    def first(self):
        self._block_executed_query()
        self.paginate = (0, 1)
        return self._execute()
        
    def last(self):
        self._block_executed_query()
        self.paginate = (-1, -1)
        return self._execute()
    
    def set(self, patch_data:dict, id:str=None):
        self._block_executed_query()
        # Update a record with the given id.
    
    ##################
    # Operator verbs #
    ##################

    def where(self, attribute_name:str):
        self._block_pending_condition(include_pending_condition=True)
        # Set current attribute that the following operator verb will apply to
        self._current_attribute = attribute_name
        return self
    
    def equals(self, value:any):
        self._block_executed_query()
        self._add_condition('==', value)
        return self
    
    def greater_than_or_equals(self, value:any):
        self._block_executed_query()
        self._add_condition('>=', value)
        return self
    
    def less_than_or_equals(self, value:any):
        self._block_executed_query()
        self._add_condition('<=', value)
        return self

    def less_than(self, value:any):
        self._block_executed_query()
        self._add_condition('<', value)
        return self

    def greater_than(self, value:any):
        self._block_executed_query()
        self._add_condition('>', value)
        return self
    
    ####################
    # Operator aliases #
    ####################

    def w(self, attribute_name:str):
        return self.where(attribute_name)
    
    def eq(self, value:any):
        return self.equals(value)
    
    def ge(self, value:any):
        return self.equals_or_greater_than(value)
    
    def le(self, value:any):
        return self.equal_or_less_than(value)
    
    def lt(self, value:any):
        return self.less_than(value)
    
    def gt(self, value:any):
        return self.greater_than(value)