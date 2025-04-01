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
from typing import List

# From package imports
from teatype.hsdb.indices import BaseIndex

class RelationalIndex(BaseIndex):
    reverse_index:dict
    
    def __init__(self,
                 cache_entries:bool=False,
                 max_size:int=None) -> None:
        super().__init__(cache_entries, max_size)
        
        self.reverse_index = dict()
        
    def add(self, relation_name:str, target_id:str, secondary_ids:List[str]=[], reverse_lookup:bool=False) -> None:
        """
        Add an entry to the index.
        """
        if reverse_lookup:
            target_index = self.reverse_index[relation_name]
        else:
            target_index = self.primary_index[relation_name]
            
        with self.transaction_lock:
            if relation_name not in target_index:
                target_index[relation_name] = {}
                
            if target_id not in target_index[relation_name]:
                target_index[relation_name][target_id] = secondary_ids
        
    def clear(self, relation_name:str=None, reverse_lookup:bool=False) -> None:
        """
        Clear the entire index.
        """
        if reverse_lookup:
            target_index = self.reverse_index[relation_name]
        else:
            target_index = self.primary_index[relation_name]
        
        with self.transaction_lock:
            if relation_name is None:
                target_index.clear()
            else:
                target_index[relation_name].clear()
        
    def fetch(self, relation_name:str, target_id:str, reverse_lookup:bool=False) -> dict|None:
        """
        Fetch an entry from the index by its ID.
        """
        if reverse_lookup:
            target_index = self.reverse_index[relation_name]
        else:
            target_index = self.primary_index[relation_name]
        
        with self.transaction_lock:
            return target_index.get(target_id)
        
    def fetch_all(self, relation_name:str, reverse_lookup:bool=False) -> dict:
        """
        Get all entries in the index.
        """
        if reverse_lookup:
            target_index = self.reverse_index[relation_name]
        else:
            target_index = self.primary_index[relation_name]
            
        with self.transaction_lock:
            if relation_name is None:
                return target_index
            return target_index[relation_name]
    
    def remove(self, relation_name:str, target_id:str, reverse_lookup:bool=False) -> dict|None:
        """
        Delete an entry from the index by its ID.
        """
        if reverse_lookup:
            target_index = self.reverse_index[relation_name]
        else:
            target_index = self.primary_index[relation_name]
            
        with self.transaction_lock:
            if self.fetch(relation_name, target_id, reverse_lookup) is None:
                raise KeyError(f'Entry with ID {target_id} does not exist in the index.')
            del target_index[relation_name][target_id]