# Copyright (C) 2024-2026 Burak Günaydin
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

# Standard-library imports
import importlib
import pkgutil
from typing import List, Type

# Third-party imports
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

# Local imports
from teatype.db.hsdb.django_support.views import HSDBDjangoCollection, HSDBDjangoResource, HSDBDjangoView
from teatype.toolkit import kebabify

# TODO: Create a seperate base class without django support
def parse_dynamic_routes(app_name:str, search_path:str, verbose:bool=False):
    print(f'Dynamic route registration for app "{app_name}"')
    urlpatterns = []
    for _, module_name, _ in pkgutil.iter_modules([search_path]):
        module = importlib.import_module(f'{app_name}.resources.{module_name}')
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
            api_path = instance.api_path()
            view_type = 'collection' if cls.is_collection else 'resource'
            
            urlpatterns.append(path(api_path, cls.as_view(), name=api_name))
            print(f'    Registered route: "{api_path}" for {view_type} "{api_name}"')
    print()
    return format_suffix_patterns(urlpatterns)

# TODO: Allow restricting/opting out of auto routes via a key on the model definition
#       itself (e.g. `auto_routes = False` or a per-method allow-list), once that's needed.
def create_auto_model_routes(models:List[Type], verbose:bool=False):
    """
    Auto-generate HSDBDjangoCollection/HSDBDjangoResource routes for a list of HSDB
    models, without requiring a hand-written resource module per model. Works the
    same for models with relations (e.g. ManyToOne/ManyToMany), since the auto CRUD
    handling in HSDBDjangoView already resolves relations via the `include_relations`
    and `expand_relations` query params.
    """
    if verbose:
        print('Auto model route registration')
    urlpatterns = []
    for model in models:
        resource_name = kebabify(model.__name__, remove='-model', plural=False)
        resource_name_plural = kebabify(model.__name__, remove='-model', plural=True)
        id_param = f'{resource_name}_id'

        collection_cls = type(f'{model.__name__}AutoCollection', (HSDBDjangoCollection,), {
            'hsdb_model': model,
            'overwrite_api_name': resource_name_plural,
            'overwrite_api_path': resource_name_plural,
        })
        resource_cls = type(f'{model.__name__}AutoResource', (HSDBDjangoResource,), {
            'hsdb_model': model,
            'overwrite_api_name': resource_name,
            'overwrite_api_path': f'{resource_name_plural}/<str:{id_param}>',
            'api_id': lambda self, _id_param=id_param: _id_param,
        })

        for cls in (collection_cls, resource_cls):
            instance = cls()
            api_name = instance.api_name()
            api_path = instance.api_path()
            view_type = 'collection' if cls.is_collection else 'resource'

            urlpatterns.append(path(api_path, cls.as_view(), name=api_name))
            if verbose:
                print(f'    Registered auto route: "{api_path}" for {view_type} "{api_name}"')
    if verbose:
        print()
    return format_suffix_patterns(urlpatterns)