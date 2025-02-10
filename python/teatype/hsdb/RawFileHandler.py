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

# From package imports
from teatype.io import env, file, path

class RawFileHandler:
    _root_data_path:str
    
    def __init__(self, root_data_path):
        if root_data_path:
            self._root_data_path = root_data_path
        else:
            # _root_data_path = env.get('CIRLOG_DATA_PATH')
            _root_data_path = '/var/lib/cirlog'
            self._root_data_path = f'{_root_data_path}/raw'
        
        path.create(self._root_data_path)
        
    def create_entry(self, model:object, data:dict, overwrite_path:str) -> str:
        try:
            if path.exists(model.file_path):
                raise Exception(f'File {model.file_path} already exists')

            # TODO: Create variable in path.create for exists ok
            absolute_file_path = path.join(self._root_data_path, model.file_path)
            file.write(absolute_file_path, data, force_format='json', prettify=True, create_parents=True)
            return absolute_file_path
        except Exception as exc:
            raise Exception(f'Could not create raw file entry: {exc}')