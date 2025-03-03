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
import json
import re
import threading
import traceback

# From system imports
from multiprocessing import Queue
from typing import List

# From package imports
from teatype.hsdb import IndexDatabase, RawFileHandler
from teatype.hsdb.util import parse_fixtures, parse_index_files
from teatype.io import env, file, path
from teatype.logging import err, hint, log, println, warn
from teatype.util import SingletonMeta

# TODO: Implement Coroutine and Operation (Atomic)
# TODO: Implement threaded Coroutine scheduler
# TODO: Implement threaded Operations controller
class HybridStorage(threading.Thread, metaclass=SingletonMeta):
    coroutines:List
    coroutines_queue:Queue
    fixtures:dict
    index_database:IndexDatabase
    migrations:dict
    operations_queue:Queue
    raw_file_handler:RawFileHandler

    def __init__(self, init:bool=False, models:List[type]=None, root_path:str=None):
        if not init:
            return
        
        # Only initialize once
        if not getattr(self, '_initialized', False):
            # Prevent re-initialization
            
            # Set the root data path
            if root_path is None:
                root_path = env.get('HSDB_ROOT_PATH')
            
            self.coroutines = []
            self.coroutines_queue = Queue()
            self.fixtures = dict
            self.migrations = dict
            self.operations_queue = Queue()
            
            self.index_database = IndexDatabase(models=models)
            self.raw_file_handler = RawFileHandler(root_path=root_path)
            
            self._initialized = True # Mark as initialized
            self.__instance = self # Set the instance
            
            log('HybridStorage finished initialization')
    
    @staticmethod
    def instance():
        if not hasattr(HybridStorage, '__instance'):
            HybridStorage.__instance = HybridStorage(init=True)
        return HybridStorage.__instance
    
    # def fill(self):
    #     pass
    
    # def register_model(self, model:object):
    #     self.index_database.models.append(model)
            
    def install_fixtures(self, fixtures_path:str=None):
        # TODO: Get default path if fixtures_path is None
        fixtures:List[dict] = parse_fixtures(fixtures_path=fixtures_path)
        for fixture in fixtures:
            model_name = fixture.get('model')
            
            matched_model = next((cls for cls in self.index_database.models if cls.__name__ == model_name), None)
            if matched_model is None:
                raise ValueError(f'Model {model_name} not found in models')
            
            for entry in fixture.get('fixtures'):
                data = entry.get('data')
                if 'de_DE' in data.get('name'):
                    name = data['name']['de_DE']
                elif 'en_EN' in data.get('name'):
                    name = data['name']['en_EN']
                else:
                    name = data.get('name')
                data.update({'name': name})
                try:
                    del data['name']['de_DE']
                    del data['name']['en_EN']
                    # del data['model_data']
                except:
                    pass
                    
                self.create_entry(matched_model, entry, parse=True, write=True)
                
    def install_index_files(self):
        parsed_index_files:List[dict] = parse_index_files(hybrid_storage_instance=self)
        for index_key in parsed_index_files:
            model_name = parsed_index_files[index_key][0].get('model_data').get('model_name')
            matched_model = next((cls for cls in self.index_database.models if cls.__name__ == model_name), None)
            if matched_model is None:
                raise ValueError(f'Model {model_name} not found in models')
                
            for index_file in parsed_index_files[index_key]:
                id = index_file.get('base_data').get('id')
                if self.get_entry(id):
                    continue
                
                self.create_entry(matched_model, index_file, parse=True, write=False)

    def create_entry(self,
                     model:object,
                     data:dict,
                     parse:bool=False,
                     write:bool=True,
                     overwrite_path:str=None) -> dict|None:
        try:
            # TODO: Implement implemented trap cleanup handlers in models
            model_instance = self.index_database.create_entry(model, data, parse)
            if model_instance is None:
                return None
            
            if write:            
                try:
                    file_path = self.raw_file_handler.create_entry(model_instance, overwrite_path)
                    # if not file.exists(file_path):
                    #     model_instance.delete()
                except:
                    # model_instance.delete()
                    pass
            return model_instance.serialize()
        except:
            return None

    def get_entry(self, model_id:str, serialize:bool=False) -> dict:
        return self.index_database.get_entry(model_id, serialize)

    def get_entries(self, model:object, serialize:bool=False) -> List[dict]:
        return self.index_database.get_entries(model, serialize)

    def modify_entry(self) -> bool:
        # TODO: Make backup of data before modifications
        #       Delete backup when write was succesful
        return True

    def delete_entry(self) -> bool:
        return True
