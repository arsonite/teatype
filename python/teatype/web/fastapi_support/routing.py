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
import importlib
import os

try:
    import fastapi
    
    def register_middleware(app, base_path:str, version:int=None) -> None:
        """
        Dynamically imports and registers middleware from all Python modules in the versioned `.middleware` directory.
        """
        if version is None:
            middleware_dir = base_path
        else:
            middleware_dir = f'{base_path}/v{version}'
        middleware_dir += '/middleware'
        
        for file_name in os.listdir(middleware_dir):
            # Skip non-Python files and special files
            if not file_name.endswith('.py') or file_name.startswith('__'):
                continue

            # Construct the module name and file path
            module_name = f'{middleware_dir.replace("/", ".")}.{file_name[:-3]}'
            file_path = os.path.join(middleware_dir, file_name)

            # Dynamically import the module
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Iterate over all attributes to find middleware classes
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                # Check if the attribute is a class and its string name ends with 'Middleware'
                if isinstance(attr, type) and attr.__name__.endswith('Middleware') and attr.__name__ != 'BaseHTTPMiddleware':
                    # Add the middleware to the app (assuming it is compatible)
                    app.add_middleware(attr)
                    print(f'Registered middleware: {attr_name} from {module_name}')

    def register_routes(app, base_path:str, root_prefix:str, version:int=None) -> None:
        """
        Dynamically imports and registers routers from all Python modules in the versioned `.routes` directory.
        """
        if version is None:
            routes_dir = base_path
        else:
            routes_dir = f'{base_path}/v{version}'
        routes_dir += '/routes'
        
        for file_name in os.listdir(routes_dir):
            # Skip non-Python files and special files
            if not file_name.endswith('.py') or file_name.startswith('__'):
                continue

            # Construct the module name and file path
            module_name = f'{routes_dir.replace("/", ".")}.{file_name[:-3]}'
            file_path = os.path.join(routes_dir, file_name)

            # Dynamically import the module
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Check if the module defines a router
            if hasattr(module, 'router'):
                router = getattr(module, 'router')
                # Check if the module contains a 'router' attribute and if it's a valid APIRouter
                # if router and isinstance(router, dict) and "include_router" in router:
                # Register the router with the app
                app.include_router(router, prefix=root_prefix)
                print(f'Registered routes from {module_name}')
except:
    print('fastapi not installed, support for FastAPI dynamic routing unavailable.')