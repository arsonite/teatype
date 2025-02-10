

# Copyright (c) 2024-2025 enamentis GmbH. All rights reserved.
#
# This software module is the proprietary property of enamentis GmbH.
# Unauthorized copying, modification, distribution, or use of this software
# is strictly prohibited unless explicitly authorized in writing.
# 
# THIS SOFTWARE IS PROVIDED "AS IS," WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, OR NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES, OR OTHER LIABILITY ARISING FROM THE USE OF THIS SOFTWARE.
# 
# For more details, check the LICENSE file in the root directory of this repository.

# System imports
import threading

# From system imports
from typing import List

# From package imports
from teatype.hsdb import IndexDatabase, RawFileHandler
from teatype.io import env
from teatype.logging import log
from teatype.util import SingletonMeta

class HybridStorage(threading.Thread, metaclass=SingletonMeta):
    _instance=None
    coroutines:List
    fixtures:dict
    index_database:IndexDatabase
    raw_file_handler:RawFileHandler

    def __init__(self, init:bool=False, models:List[type]=None, overwrite_root_data_path:str=None):
        if not init:
            return
        
        # Only initialize once
        if not getattr(self, '_initialized', False):
            # Prevent re-initialization
            self.coroutines = []
            self.index_database = IndexDatabase(models=models)

            # Set the root data path
            if overwrite_root_data_path:
                root_data_path = overwrite_root_data_path
            else:
                root_data_path = env.get('HSDB_ROOT_PATH')

            self.raw_file_handler = RawFileHandler(root_data_path=root_data_path)

            self._initialized = True # Mark as initialized
            
            log('HybridStorage finished initialization')

    def create_entry(self, model:object, data:dict, overwrite_path:str=None) -> bool:
        try:
            db_entry = self.index_database.create_entry(model, data, overwrite_path)
            self.raw_file_handler.create_entry(model, data, overwrite_path)
            return db_entry.as_dict()
        except Exception as exc:
            import traceback
            traceback.print_exc()
            return None

    def get_entry(self) -> dict:
        pass

    def get_entries(self, model:object) -> List[dict]:
        return self.index_database.get_entries(model)

    def modify_entry(self) -> bool:
        return True

    def delete_entry(self) -> bool:
        return True
