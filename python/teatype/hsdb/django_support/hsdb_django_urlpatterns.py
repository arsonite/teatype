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
import importlib
import pkgutil

# From package imports
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

# From local imports
from teatype.hsdb.django_support import HSDBDjangoCollection, HSDBDjangoResource, HSDBDjangoView

def parse_dynamic_routes(app_name:str, search_path:str, verbose:bool=False):
    print(f'Dynamic route registration for app "{app_name}"')
    urlpatterns = []
    for _, module_name, _ in pkgutil.iter_modules([search_path]):
        module = importlib.import_module(f'.{module_name}', package='restapi.raw.routes')
        if verbose:
            print('Found module:', module_name)
        for _, obj in vars(module).items():
            if isinstance(obj, type) and issubclass(obj, HSDBDjangoView):
                if verbose:
                        print(f'Found class: {obj.__name__}, is subclass of HSDBDjangoView: {issubclass(obj, HSDBDjangoView)}')
                        print(f'Is subclass of HSDBDjangoCollection: {issubclass(obj, HSDBDjangoCollection)}')

        cls = next(
            (
                obj
                for _, obj in vars(module).items()
                if isinstance(obj, type) and issubclass(obj, HSDBDjangoView) and (obj is not HSDBDjangoCollection and obj is not HSDBDjangoResource)
            ),
            None
        )
        if cls:
            if verbose:
                print(f'Selected class: {cls.__name__}')
        else:
            raise Exception('No valid class selected!')

        if issubclass(cls, HSDBDjangoView):
            instance = cls()
            api_name = instance.api_name()
            api_plural_name = instance.api_plural_name()
            api_path = instance.api_path()
            view_type = 'collection' if cls.is_collection else 'resource'
            
            urlpatterns.append(path(api_path, cls.as_view(), name=api_plural_name))
            print(f'    Registered route: "{api_path}" for {view_type} "{api_name}"')
    print()
    return format_suffix_patterns(urlpatterns)