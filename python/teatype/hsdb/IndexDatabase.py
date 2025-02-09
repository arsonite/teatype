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

class IndexDatabase:
    _compute_index:dict # For all compute values for easy modification
    _compute_index_lock:threading.Lock
    _db:dict # For all raw data
    _db_lock:threading.Lock
    _models:List[type] # For all models
    _model_index:dict # For all model references for faster model query lookups
    _model_index_lock:threading.Lock
    _relational_index:dict # For all relations between models parsed dynamically from the model definitions
    _relational_index_lock:threading.Lock
    
    def __init__(self, models:List[type]):
        self._models = models
        
        self._db_lock = threading.Lock()
        self._db = dict()
    
    def fill(self, raw_data:dict):
        for entry in raw_data:
            model_name = entry.get('model_name')
            model_id = entry.get('id')
                
            matched_model = next((cls for cls in self._models if cls.__name__ == model_name), None)
            if matched_model is None:
                raise ValueError(f'Model {model_name} not found in models')
            
            if model_id not in self._db:
                self._db[model_id] = matched_model(**entry)
            
    def create_entry(self, model:object, data:dict, overwrite_path:str) -> object|None:
        try:
            with self._db_lock:
                model_instance = model(**data)
                
                model_name = model_instance.model_name
                with self._model_index_lock:
                    if model not in self._model_index:
                        self._model_index[model] = {}
                model_id = model_instance.id
                if model_id in self._db[model]:
                    raise ValueError(f'Model entry with id {model_id} already exists')
                
                # Model.create(overwrite_path, model_instance)
                # TODO: Quick and dirty hack, need to refactor this with proper attributes
                # need for algorithm to be implemented with the model callhandlers
                match model_name:
                    case 'InstrumentModel':
                        pass
                    case 'ImageModel':
                        pass
                    
                # model_plural_name = model.plural_name
                # if model_plural_name not in self._db:
                #     self._db[model.plural_name] = {}
                
                # self._db[model.plural_name][model_id] = data
                
                self._db[model_id] = data
                
                # TODO: Temporary
                import pprint
                pprint.pprint(self._db)
                
                return model_instance
        except:
            import traceback
            traceback.print_exc()
            return None
        
    def get_entries(self, model:object) -> List[object]:
        with self._db_lock:
            for entry in self._db:
                print(entry)
                
            # for model_name, model_data in self._db.items():
            #     if model_name == model.model_name:
            #         return [data for data in model_data.values()]
        
    def query(self, model:object, query:dict) -> List[object]:
        filters = query.get('where', {})
        order_by = query.get('order_by', None)
        limit = query.get('limit', None)
        results = []

        for record_id, record_data in self._db.items():
            if all(record_data.get(k) == v for k, v in filters.items()):
                instance = model(**record_data)
                results.append(instance)

        if order_by:
            field, _, direction = order_by.partition(" ")
            reverse = direction.lower() == "desc"
            results.sort(key=lambda x: getattr(x, field, None), reverse=reverse)

        if isinstance(limit, int):
            results = results[:limit]

        return results