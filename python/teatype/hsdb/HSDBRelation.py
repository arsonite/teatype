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

class HSDBRelation:
    _name:str
    _primary_keys:List[str]
    _relation_type:str
    _relational_key:str
    _secondary_keys:List[str]
    
    class OneToOne:
        pass
    
    class OneToMany:
        pass
    
    class ManyToMany:
        pass
    
    def __init__(self, name:str, primary_keys:List[str], secondary_keys:List[str], relational_key:str='id') -> None:
        self._name = name
        self._relational_key = relational_key
        
        self.setPrimaryKeys(primary_keys)
        self.setSecondaryKeys(secondary_keys)
    
    def __repr__(self) -> str:
        return (f'HSDBRelation(primary_keys={self._primary_keys},' \
                f'secondary_keys={self._secondary_keys},' \
                f'relation_type={self._relation_type})')
    
    def _parse_relation_type(self) -> None:
        if len(self._primary_keys) == 1 and len(self._secondary_keys) == 1:
            self._relation_type = 'one-to-one'
        elif len(self._primary_keys) == 1 and len(self._secondary_keys) > 1:
            self._relation_type = 'one-to-many'
        elif len(self._primary_keys) > 1 and len(self._secondary_keys) == 1:
            self._relation_type = 'many-to-one'
        else:
            self._relation_type = 'many-to-many'
            
    def _validate_key(self, key:str) -> None:
        if not isinstance(key, str) or not key:
            raise ValueError('key must be a non-empty string')
            
    def _validate_keys(self, keys:List[str]) -> None:
        if not isinstance(keys, list) or not keys:
            raise ValueError('keys must be a non-empty list')
        for key in keys:
            self._validate_key(key)
        
    def addPrimaryKey(self, primary_key:str) -> None:
        if primary_key in self._primary_keys:
            raise ValueError(f'Primary key {primary_key} already exists')
        elif primary_key in self._secondary_keys:
            raise ValueError(f'Primary key {primary_key} cannot be a secondary')
        self._validate_key(primary_key)        
        self._primary_keys.append(primary_key)
        self._parse_relation_type()
        
    def addSecondaryKey(self, secondary_key:str) -> None:
        if secondary_key in self._secondary_keys:
            raise ValueError(f'Secondary key {secondary_key} already exists')
        elif secondary_key in self._primary_keys:
            raise ValueError(f'Secondary key {secondary_key} cannot be a primary')
        self._validate_key(secondary_key)        
        self._secondary_keys.append(secondary_key)
        self._parse_relation_type()
        
    def removePrimaryKey(self, primary_key:str) -> None:
        if primary_key not in self._primary_keys:
            raise ValueError(f'Primary key {primary_key} does not exist')
        self._primary_keys.remove(primary_key)
        self._parse_relation_type()
        
    def removeSecondaryKey(self, secondary_key:str) -> None:
        if secondary_key not in self._secondary_keys:
            raise ValueError(f'Secondary key {secondary_key} does not exist')
        self._secondary_keys.remove(secondary_key)
        self._parse_relation_type()
        
    ###########
    # Getters #
    ###########
    
    def getName(self) -> str:
        return self._name
    
    def getPrimaryKeys(self) -> List[str]:
        return self._primary_keys
    
    def getSecondaryKeys(self) -> List[str]:
        return self._secondary_keys
    
    def getRelationType(self) -> str:
        return self._relation_type
    
    ###########
    # Setters #
    ###########
    
    def setPrimaryKeys(self, primary_keys:List[str]) -> None:
        self._validate_keys(primary_keys)
        self._primary_keys = primary_keys
        self._parse_relation_type()
        
    def setSecondaryKeys(self, secondary_keys:List[str]) -> None:
        self._validate_keys(secondary_keys)
        self._secondary_keys = secondary_keys
        self._parse_relation_type()