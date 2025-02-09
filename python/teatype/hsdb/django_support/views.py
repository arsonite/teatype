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
import re
import traceback

# From system imports
from abc import ABCMeta
from typing import List, Type

# From package imports
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.views import APIView
from teatype.hsdb import HybridStorage
from teatype.hsdb.django_support.responses import NotAllowed, ServerError, Success

class HSDBDjangoView(APIView):
    __metaclass__:ABCMeta=ABCMeta
    __COLLECTION_METHODS=['GET', 'POST']
    __DATA_REQUIRED_METHODS=['POST', 'PUT', 'PATCH']
    api_parents:List[str]=[]
    auto_view=True
    data_key:str=None # TODO: Automate data key as well and allow overwriting
    is_collection:bool
    hsdb_model:Type=None
    hsdb_hybrid_storage:HybridStorage
    overwrite_api_name:str=None
    overwrite_api_plural_name:str=None
    overwrite_api_path:str=None
    
    @property
    def allowed_methods(self) -> List[str]:
        if self.is_collection:
            return [method.lower() for method in dir(self) if method in ['get', 'post']]
        return [method.lower() for method in dir(self) if method in ['get', 'put', 'delete', 'patch']]

    def _auto_method(self, request, kwargs):
        try:
            if not self.auto_view:
                raise NotImplementedError(f'Auto mode is off, you need to implement the {request.method} method yourself.')

            if self.hsdb_model is None:
                raise ValueError('Can\' use auto mode without specifying a hsdb_model in view')
            
            if request.method in self.__DATA_REQUIRED_METHODS:
                if not request.data:
                    return NotAllowed(f'Data is required for {request.method} requests')
                
                if self.data_key not in request.data:
                    return NotAllowed(f'Data key {self.data_key} is required for {request.method} requests')
                
                data = request.data[self.data_key]
            
            match request.method:
                case 'GET':
                    if self.is_collection:
                        response = self.hsdb_hybrid_storage.get_entries(self.hsdb_model)
                    else:
                        # id = kwargs.get(id)
                        response = self.hsdb_hybrid_storage.get_entry()
                case 'POST':
                    response = self.hsdb_hybrid_storage.create_entry(self.hsdb_model, data)
                case 'PUT':
                    response = self.hsdb_hybrid_storage.create_entry()
                case 'PATCH':
                    response = self.hsdb_hybrid_storage.modify_entry()
                case 'DELETE':
                    response = self.hsdb_hybrid_storage.delete_entry()
                    
            # TODO: Implement proper response handling
            if response:
                if type(response) == list:
                    response = [entry.as_dict() for entry in response]
                return Success(response)
            else:
                return ServerError({'message': 'Response was "None"'})
        except Exception as exc:
            traceback.print_exc()
            return ServerError(exc)
    
    # TODO: Turn into util function
    def _parse_name(self, seperator:str='-'):
        raw_name = type(self).__name__
        return re.sub(r'(?<!^)(?=[A-Z])', seperator, raw_name).lower()

    # TODO: Figure out how to make these work as properties
    def api_id(self) -> str:
        parsed_name = self._parse_name()
        return f'{parsed_name}_id'
    
    def api_name(self) -> str:
        if self.overwrite_api_name:
            return self.overwrite_api_name
        return self._parse_name()
    
    def api_plural_name(self) -> str:
        return self.api_name() + 's' if not self.api_name().endswith('s') else self.api_name() + 'es'
    
    # TODO: consider api parents
    def api_path(self) -> str:
        if self.overwrite_api_path:
            return self.overwrite_api_path
        
        parsed_name = self._parse_name()
        if self.is_collection:
            return f'/{parsed_name}'
        return f'/{parsed_name}s/<str:{self.api_id()}>'

    def initial(self, request, *args, **kwargs) -> None:
        """
        Dispatch function that triggers before delegating requests to
        the CRUD methods (GET, PUT, PATCH, DELETE).
        """
        request_method = request.method
        if self.is_collection and request_method not in self.__COLLECTION_METHODS:
            return NotAllowed(f'You can\'t use {request_method} requests on collections.')

        if request_method not in self.allowed_methods:
            return NotAllowed(f'Method not allowed. Allowed methods: {self.allowed_methods}')
        
        self.hsdb_hybrid_storage = HybridStorage()
        
    def handle_exception(self, exc):
        if isinstance(exc, MethodNotAllowed):
            return NotAllowed(f'Method not allowed. Allowed methods: {self.allowed_methods}')

    def get(self, request, *args, **kwargs):
        return self._auto_method(request, kwargs)
    
    def post(self, request, *args, **kwargs):
        return self._auto_method(request, kwargs)

    def post(self, request, *args, **kwargs):
        return self._auto_method(request, kwargs)

    def put(self, request, *args, **kwargs):
        return self._auto_method(request, kwargs)

    def patch(self, request, *args, **kwargs):
        return self._auto_method(request, kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self._auto_method(request, kwargs)
    
class HSDBDjangoResource(HSDBDjangoView):
    is_collection:bool=False
    
class HSDBDjangoCollection(HSDBDjangoView):
    is_collection:bool=True