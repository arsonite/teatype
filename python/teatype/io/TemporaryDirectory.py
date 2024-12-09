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
import os
import shutil
import uuid

class TemporaryDirectory:
    """
    A context manager for creating and automatically cleaning up a temporary folder.

    Attributes:
        directory_path (str): The base path where the temporary folder will be created.
        directory_name (str): The name of the temporary folder. If not provided, a unique name will be generated.
        ignore_errors (bool): Whether to ignore errors when deleting the folder.
    """

    def __init__(self, directory_path:str='.', directory_name:str=None, ignore_errors:bool=True, keep_folder:bool=False):
        """
        Initializes the TemporaryDirectory context manager.

        Args:
            directory_path (str): The base path where the temporary folder will be created. Defaults to current directory.
            directory_name (str): The name of the temporary folder. If not provided, a unique name will be generated.
            ignore_errors (bool): Whether to ignore errors when deleting the folder. Defaults to True.
        """
        self.directory_path = directory_path
        # If directory_name is provided, use it; otherwise, generate a unique name
        self.directory_name = directory_name if directory_name else f'~temp-{uuid.uuid4().hex}'
        # Combine base path and folder name to get the full path of the temporary folder
        self.folder_path = os.path.join(self.directory_path, self.directory_name)
        self.ignore_errors = ignore_errors
        self.keep_folder = keep_folder

    def __enter__(self):
        """
        Creates the temporary folder when entering the context.

        Returns:
            str: The path to the temporary folder.
        """
        # Create the directory
        os.makedirs(self.folder_path, exist_ok=True)
        return self.folder_path

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Removes the temporary folder and all its contents when exiting the context.

        Args:
            exc_type (type): The exception type.
            exc_value (Exception): The exception instance.
            traceback (traceback): The traceback object.
        """
        if self.keep_folder:
            return
        # Remove the directory and all its contents
        shutil.rmtree(self.folder_path, self.ignore_errors)