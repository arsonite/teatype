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
from teatype.hsdb import IndexDatabase, RawFileHandler
from teatype.io import env
from teatype.logging import log

# A class that represents a Rolodex, from Rolodeck from rotating cards and Index a database index
class HybridStorage(threading.Thread):
    _instance=None
    coroutines:List
    fixtures:dict
    index_database:IndexDatabase
    raw_file_handler:RawFileHandler

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(HybridStorage, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self, overwrite_root_data_path:str=None):
        # Initialize any attributes if needed
        if not hasattr(self, '_initialized'):
            self._initialized = True
            
            # TODO: Add coroutine support
            self.coroutines = []
            
            self.index_database = IndexDatabase()
            
            if overwrite_root_data_path:
                root_data_path = overwrite_root_data_path
            else:
                root_data_path = env.get('HSDB_ROOT_PATH')
            self.raw_file_handler = RawFileHandler(root_data_path=root_data_path)
            
            log('HybridStorage finished initialization')
            