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
import configparser
import csv
import json
import os
import shutil

# From system imports
from pathlib import PosixPath
from typing import List

# From own imports
from teatype.logging import err, warn

def append(path:str, data:any, force_format:str=None) -> bool:
    """
    Append data to a file at the specified path.

    Depending on the file extension, the data is appended in the appropriate format:
    - .json: JSON format
    - .ini: INI configuration
    - .csv: CSV format
    - others: plain text

    Parameters:
        path (str): The path to the file.
        data (any): The data to append to the file.

    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    try:
        # Open the file in append mode
        with open(path, 'a') as f:
            if force_format == 'lines':
                # Append multiple lines to the file
                f.writelines(data)
            if path.endswith('.json') or force_format == 'json':
                # Append JSON data to the file
                json.dump(data, f)
            elif path.endswith('.ini') or force_format == 'ini':
                # Initialize ConfigParser and read existing INI configuration
                config = configparser.ConfigParser()
                config.read(path)
                # Update the configuration with new data
                config.update(data)
                # Write the updated configuration back to the file
                config.write(f)
            elif path.endswith('.csv') or force_format == 'csv':
                # Create a CSV writer object
                writer = csv.writer(f)
                # Write a new row to the CSV file
                writer.writerow(data)
            else:
                # Append plain text data to the file
                f.write(data)
        return True
    except Exception as e:
        # Log an error message if an exception occurs
        err(f'Error appending to file {path}: {e}')
        return False
    
def copy(source:str, destination:str, create_parent_directories:bool=True, overwrite:bool=True) -> bool:
    """
    Copy a file from the source path to the destination path.

    Parameters:
        source (str): The path to the source file.
        destination (str): The path to the destination file.

    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    try:
        if not exists(source):
            # Log an error message if the source file does not exist
            err(f'File "{source}" does not exist.')
            return False
        
        if exists(destination):
            if overwrite:
                pass
            else:
                # Log a warning message if the destination file already exists
                err(f'File "{destination}" already exists. Call with "overwrite=True" to replace it.')
                return False
            
        shutil.copy(source, destination)
        return True
    except Exception as exc:
        # Log an error message if an exception occurs
        err(f'Error copying file from {source} to {destination}: {exc}')
        return False

def delete(path:str) -> bool:
    """
    Delete a file (or directory) at the specified path.

    Parameters:
        path (str): The path to the file.

    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    try:
        os.remove(path)
        return True
    except Exception as exc:
        # Log an error message if an exception occurs
        err(f'Error deleting file "{path}": {exc}')
        return False
    
def exists(path:PosixPath|str) -> bool:
    """
    Check if a file exists at the specified path.

    Parameters:
        path (str): The path to the file.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    if isinstance(path, PosixPath):
        string_path = str(path)
    else:
        string_path = path
    return os.path.exists(string_path), os.path.isfile(string_path)
    
def list(directory:str, recursive:bool=True) -> List[str]:
    """
    Walk through a directory and return a list of files and subdirectories.

    Parameters:
        directory (str): The path to the directory to walk through.
        recursive (bool): Whether to walk through subdirectories recursively.

    Returns:
        list: A list of files and subdirectories in the directory.
    """
    try:
        # TODO: Check formatting of the returned list
        # Initialize an empty list to store the files and subdirectories
        files = []
        # Walk through the directory and append files and subdirectories to the list
        for root, directory, filenames in os.walk(directory):
            # print(root)
            # print(directory)
            # print(filenames)
            for filename in filenames:
                files.append(os.path.join(root, filename))
            if not recursive:
                break
        return files
    except Exception as exc:
        # Log an error message if an exception occurs
        err(f'Error walking through directory "{directory}": {exc}')
        raise exc

def move(source:str, destination:str, create_parent_directories:bool=True, overwrite:bool=True) -> bool:
    """
    Move a file from the source path to the destination path.

    Parameters:
        source (str): The path to the source file.
        destination (str): The path to the destination file.

    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    try:
        if not exists(source):
            # Log an error message if the source file does not exist
            err(f'File "{source}" does not exist.')
            return False
        
        if exists(destination):
            if overwrite:
                pass
            else:
                # Log a warning message if the destination file already exists
                err(f'File "{destination}" already exists. Call with "overwrite=True" to replace it.')
                return False
            
        shutil.move(source, destination)
        return True
    except Exception as exc:
        # Log an error message if an exception occurs
        err(f'Error moving file from {source} to {destination}: {exc}')
        return False

def read(path:PosixPath|str, force_format:str=None) -> any:
    """
    Read data from a file at the specified path.

    Depending on the file extension, the data is read in the appropriate format:
    - .json: JSON data
    - .ini: INI configuration
    - .csv: CSV data
    - .env: Environment variables
    - others: plain text

    Parameters:
        path (str): The path to the file.

    Returns:
        any: The data read from the file, or None if an error occurred.
    """
    try:
        if isinstance(path, PosixPath):
            string_path = str(path)
        else:
            string_path = path
        
        file_exists, is_file = exists(string_path)
        if file_exists:
            if is_file:
                with open(string_path, 'r') as f:
                    if force_format == 'lines':
                        # Read and return the lines of the file
                        return f.readlines()
                    elif string_path.endswith('.jsonc') or force_format == 'jsonc':
                        dirty_content = f.read()
                        # Remove comments denoted by '//' to ensure valid JSON
                        clean_content = ''.join(line for line in dirty_content.splitlines() if not line.strip().startswith('//'))
                        return json.loads(clean_content)
                    elif string_path.endswith('.json') or force_format == 'json':
                        # Load and return JSON data from the file
                        return json.load(f)
                    elif string_path.endswith('.ini') or force_format == 'ini':
                        # Initialize ConfigParser and read INI configuration
                        config = configparser.ConfigParser()
                        config.read(string_path)
                        return config
                    elif string_path.endswith('.csv') or force_format == 'csv':
                        # Read and return CSV data as a list of rows
                        return list(csv.reader(f))
                    elif string_path.endswith('.env') or force_format == 'env':
                        # Parse and return environment variables from the file
                        env_vars = {}
                        for line in f:
                            line = line.strip()
                            # Check if the line is not empty and does not start with a comment
                            if line and not line.startswith('#'):
                                # Split the line into key and value using the first '=' as delimiter
                                key, _, value = line.partition('=')
                                # Strip whitespace and set the environment variable
                                env_vars[key.strip()] = value.strip()
                        return env_vars
                    else:
                        # Read and return plain text data from the file
                        return f.read()
            else:
                file_is_folder_message = f'"{string_path}" is a directory, not a file.'
                err(file_is_folder_message)
                raise IsADirectoryError(file_is_folder_message)
        else:
            file_not_found_message = f'File "{string_path}" does not exist.'
            # Log an error message if the file does not exist
            err(file_not_found_message)
            raise FileNotFoundError(file_not_found_message)
    except Exception as exc:
        # Log an error message if an exception occurs
        err(f'Error reading file "{string_path}": {exc}')
        raise exc

def write(path:str, data:any, force_format:str=None) -> bool:
    """
    Write data to a file at the specified path.

    Depending on the file extension, the data is written in the appropriate format:
    - .json: JSON format
    - .ini: INI configuration
    - .csv: CSV format
    - others: plain text

    Parameters:
        path (str): The path to the file.
        data (any): The data to write to the file.

    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    try:
        # Open the file in write mode
        with open(path, 'w') as f:
            if force_format == 'lines':
                # Write multiple lines to the file
                f.writelines(data)
            elif path.endswith('.json') or force_format == 'json':
                # Write JSON data to the file
                json.dump(data, f)
            elif path.endswith('.ini') or force_format == 'ini':
                # Initialize ConfigParser and update with new data
                config = configparser.ConfigParser()
                config.update(data)
                # Write the updated configuration to the file
                config.write(f)
            elif path.endswith('.csv') or force_format == 'csv':
                # Create a CSV writer object
                writer = csv.writer(f)
                # Write multiple rows to the CSV file
                writer.writerows(data)
            else:
                # Write plain text data to the file
                f.write(data)
        return True
    except Exception as exc:
        # Log an error message if an exception occurs
        err(f'Error writing to file {path}: {exc}')
        raise exc