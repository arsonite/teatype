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

class HSDBAttribute:
    key:str
    max_size:int
    required:bool
    relation:str
    unique:bool
    value:any
    
    def __init__(self, key:str, editable:bool=True, relation:str=None, required:bool=False, unique:bool=False):
        self.key = key
        self.editable = editable
        self.relation = relation
        self.unique = unique
        self.required = required
        
    def setValue(self, key:str):
        self.key = key

    def setValue(self, value:any):
        self.value = value