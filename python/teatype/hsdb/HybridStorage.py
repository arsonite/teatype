

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
        
    def fill(self):
        pass
            
    def install_fixtures(self, fixtures:List[dict]):
        for fixture in fixtures:
            model_name = fixture.get('model')
            
            matched_model = next((cls for cls in self.index_database.models if cls.__name__ == model_name), None)
            if matched_model is None:
                raise ValueError(f'Model {model_name} not found in models')
            
            for entry in fixture.get('fixtures'):
                id = entry.get('id')
                data = entry.get('data')
                if data.get('de_DE'):
                    name = data['de_DE']['name']
                elif data.get('en_EN'):
                    name = data['en_EN']['name']
                else:
                    name = data.get('name')
                    
                self.create_entry(matched_model, {'id': id, 'name': name})
                
    def install_raw_data(self, parsed_raw_data:List[dict]):
        for raw_data in parsed_raw_data:
            model_name = raw_data.get('model_meta').get('model_name')
            matched_model = next((cls for cls in self.index_database.models if cls.__name__ == model_name), None)
            if matched_model is None:
                raise ValueError(f'Model {model_name} not found in models')
            
            id = raw_data.get('id')
            data = raw_data.get('data')
            self.create_entry(matched_model, {'id': id, **data})

    def create_entry(self, model:object, data:dict, overwrite_path:str=None) -> dict|None:
        try:
            model_instance = self.index_database.create_entry(model, data, overwrite_path)
            if model_instance is None:
                return None
            
            file_path = self.raw_file_handler.create_entry(model_instance, overwrite_path)
            return model_instance.serialize()
        except Exception as exc:
            import traceback
            traceback.print_exc()
            return None

    def get_entry(self, model_id:str) -> dict:
        return self.index_database.get_entry(model_id)

    def get_entries(self, model:object) -> List[dict]:
        return self.index_database.get_entries(model)

    def modify_entry(self) -> bool:
        return True

    def delete_entry(self) -> bool:
        return True
