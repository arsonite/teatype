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
from functools import reduce
from typing import List, Union

# From package imports
from teatype.hsdb import HybridStorage
from teatype.util import stopwatch

_EXECUTION_HOOKS = ['__iter__', '__len__', '__getitem__', 'all', 'collect', 'first', 'last', 'set']
_OPERATOR_VERBS = [('eq', 'equals'),
                   ('ge', 'greater_than_or_equals'),
                   ('le', 'less_than_or_equals'),
                   ('lt', 'less_than'),
                   ('gt', 'greater_than')]

# TODO: Add support for running queries on querysets again after execution to allow reducing even further after initial query
class HSDBQuery:
    _conditions:List
    _current_attribute:str
    _filter_key:str
    _index_db_reference:object # IndexDatabase, avoiding import loop
    _index_id:str
    _measure_time:bool
    _paginate:Union[int, int]
    _return_ids:bool
    _sort_key:str
    _sort_order:str
    already_executed:bool
    model:type # HSDBModel class, avoiding import loop
    
    def __init__(self, model:type):
        # model is used later to help interpret attribute types and relations
        self.model = model
        
        self.already_executed = False
        
        self._conditions = [] # list of (attribute_path, operator, value)
        self._current_attribute = None
        self._filter_key = None
        self._index_db_reference = HybridStorage().index_database._db
        self._index_id = None
        self._measure_time = False
        self._paginate = None
        self._return_ids = False
        self._sort_key = None
        self._sort_order = None

    def __repr__(self):
        return f'<HSDBQuery ' \
               f'conditions={self._conditions} ' \
               f'filter_key={self._filter_key} ' \
               f'sort_by={self._sort_key}({self._sort_order}) ' \
                '/>'
                
    def __str__(self):
        return self.__repr__()

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
            
        if self.already_executed:
            raise ValueError('Query already executed. Call a new query property to start a new query.')
    
    def _run_query(self):
        """
        Execute a query representation on an in-memory db.

        Parameters:
        query: HSDBQuery instance with conditions and sort_key.

        Returns:
        List of identifiers that match the query if self._return_ids is True.
        List of entry that match the query if self._return_ids is False.
        """
        def __get_nested_value(entry, attribute_path):
            """
            Retrieve the value of a nested attribute path in the entry.

            This method now handles nested class attributes and avoids repeated class lookups
            by utilizing the attribute index.
            """
            # parts = attribute_path.split('.')
            # value = entry
            # for part in parts:
            #     # TODO: Implement key lookup through pointer reference.
            #     if not isinstance(value, dict):
            #         # Look up the referenced record in the db using string key.
            #         reference = str(value)
            #         if reference in self._index_db_reference and isinstance(self._index_db_reference[reference], dict):
            #             value = self._index_db_reference[reference]
            #         else:
            #             # If reference not found, return None.
            #             return None
            #     value = getattr(value, part)
            # return value
        
            parts = attribute_path.split('.')
            # Use a reduce to iterate over the attribute parts
            def lookup_value(accumulated_value, part):
                if isinstance(accumulated_value, dict):
                    # If it's a dict, look up the value by key
                    return accumulated_value.get(part, None)
                elif hasattr(accumulated_value, part):
                    # If it's an object, use getattr to get the attribute
                    return getattr(accumulated_value, part, None)
                else:
                    return None

            # Initial value is the entry object itself (which may be a dictionary or class instance)
            return reduce(lookup_value, parts, entry)

        def __condition_matches(entry, condition):
            attribute, operator, expected = condition
            actual_attribute = __get_nested_value(entry, attribute)
            actual_value = actual_attribute._value
            if operator == '==':
                return actual_value == expected
            elif operator == '<':
                return actual_value is not None and actual_value < expected
            elif operator == '>':
                return actual_value is not None and actual_value > expected
            else:
                raise ValueError(f'Unsupported operator {operator}')
            
        self._block_executed_query()
        
        if self._measure_time:
            stopwatch(str(self))

        # First filter using conditions.
        entries = []
        for id, entry in self._index_db_reference.items():
            if entry.cls != self.model:
                continue
            if all(__condition_matches(entry, condition) for condition in self._conditions):
                if self._return_ids:
                    entries.append(id)
                else:
                    entries.append(entry)
                    
        # Sort the entries if needed.
        if self._sort_key:
            entries.sort(key=lambda entry: __get_nested_value(entry[1], self._sort_key))
        if self._filter_key:
            entries = [entry for entry in entries if __get_nested_value(entry[1], self._filter_key)]
            
        if self._measure_time:
            stopwatch()
        
        self.already_executed = True
        
        # Return list of ids.
        return entries
    
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
    
    #####################
    # Runtime modifiers #
    #####################
    
    def measure_time(self):
        self._block_executed_query()
        self._measure_time = True
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
        return iter(self._run_query())

    def __len__(self):
        """
        Trigger execution when len() is called.
        """
        self._block_executed_query()
        return len(self._run_query())

    def __getitem__(self, index):
        """
        Trigger execution when accessing an item.
        """
        self._block_executed_query()
        return self._run_query()[index]

    def all(self):
        self._block_executed_query()
        # Calling all resets any previous conditions
        self._conditions = []
        return self._run_query()
    
    def collect(self):
        """
        Forcing the query to execute and return the results without any special actions.
        """
        self._block_executed_query()
        return self._run_query()
    
    def first(self):
        self._block_executed_query()
        self.paginate = (0, 1)
        return self._run_query()
        
    def last(self):
        self._block_executed_query()
        self.paginate = (-1, -1)
        return self._run_query()
    
    def set(self, patch_data:dict, id:str=None):
        self._block_executed_query()
        # Update a record with the given id.
    
    ##################
    # Operator verbs #
    ##################

    def where(self, attribute_name:str):
        self._block_executed_query(include_pending_condition=True)
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
    
    def w(self, attribute_name: str) -> 'HSDBQuery': return self.where(attribute_name)
    def eq(self, value:any) -> 'HSDBQuery': return self.equals(value)
    def ge(self, value:any) -> 'HSDBQuery': return self.greater_than_or_equals(value)
    def le(self, value:any) -> 'HSDBQuery': return self.less_than_or_equals(value)
    def lt(self, value:any) -> 'HSDBQuery': return self.less_than(value)
    def gt(self, value:any) -> 'HSDBQuery': return self.greater_than(value)