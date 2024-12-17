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

class _File:
    def __init__(self, path:str, content:any=None, trimmed:bool=False):
        """
        Initializes a File object with various attributes based on the given path.
        
        Parameters:
            path (str): The path to the file or directory.
            content (any, optional): The content of the file. Defaults to None.
            trimmed (bool, optional): Whether to skip retrieving additional file attributes. Defaults to False.
        """
        self.path = path # Store the path to the file or directory

        self.exists = os.path.exists(path) # Check if the file or directory exists
        if self.exists:
            self.content = content # Store the content of the file
                
            # Check if the path is a file and store the result
            self.is_file = os.path.isfile(path)
            if self.is_file:
                # Extract the file extension from the path
                self.extension = os.path.splitext(path)[1]
                
            # Get the base name of the path (the final component) and store it
            self.name = os.path.basename(path)
            
            if not trimmed:
                # Retrieve the last accessed time of the file or directory
                self.accessed_at = os.path.getatime(path)
                # Retrieve the creation time of the file or directory
                self.created_at = os.path.getctime(path)
                # Get the group ID of the owner of the file or directory
                self.group = os.stat(path).st_gid
                # Check if the path is a symbolic link and store the result
                self.is_symlink = os.path.islink(path)
                # Retrieve the last modified time of the file or directory
                self.modified_at = os.path.getmtime(path)
                # Get the user ID of the owner of the file or directory
                self.owner = os.stat(path).st_uid
                # Get the parent directory of the path and store it
                self.parent = os.path.dirname(path)
                # Get the permission bits of the file and store them
                self.permissions = os.stat(path).st_mode
                
                if self.is_file:
                    # Get the size of the file in bytes and store it
                    self.size = os.path.getsize(path)
                else:
                    # Get the size of the directory in bytes
                    self.size = sum(os.path.getsize(os.path.join(dirpath, filename)) for dirpath, dirnames, filenames in os.walk(path) for filename in filenames)

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
    
def copy(source:str,
         destination:str,
         create_parent_directories:bool=True,
         overwrite:bool=True) -> bool:
    """
    Copy a file from the source path to the destination path.

    Parameters:
        source (str): The path to the source file.
        destination (str): The path to the destination file.
        create_parent_directories (bool): Whether to create parent directories if they do not exist.
        overwrite (bool): Whether to overwrite the destination file if it already exists.

    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    try:
        if not exists(source):
            # Log an error message if the source file does not exist
            err(f'File "{source}" does not exist.')
            return False
        
        if exists(destination):
            if not overwrite:
                # Log an error message if the destination file already exists
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
        # Check if the path exists and determine if it's a file
        file_exists, is_file = exists(path)
        if file_exists:
            if is_file:
                # If it's a file, log a warning indicating that a directory will be deleted
                err(f'"{path}" is a directory. Deleting the directory and its contents.')
                # Recursively remove the directory and all its contents
                shutil.rmtree(path)
            else:
                # If it's not a file (i.e., it's a regular file), remove it
                os.remove(path)
        return True
    except Exception as exc:
        # Log an error message if an exception occurs
        err(f'Error deleting file "{path}": {exc}')
        return False
    
def exists(path:PosixPath|str, return_file:bool=False, trim_file:bool=False) -> bool|_File:
    """
    Check if a file exists at the specified path.

    Parameters:
        path (str): The path to the file.
        return_file (bool): Whether to return a _File object with additional attributes.
        trim_file (bool): Whether to skip retrieving additional file attributes.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    if trim_file and not return_file:
        # Warn the user that trimming is ignored because a _File object is not being returned
        warn('Cannot trim file without returning a _File object. Ignoring "trim_file" parameter.')
    
    # Check if the provided path is a PosixPath object
    if isinstance(path, PosixPath):
        # Convert PosixPath to string for compatibility with os.path functions
        string_path = str(path)
    else:
        # Use the path as-is if it's already a string
        string_path = path
    
    # Return a _File object with the specified path and trimming option if requested
    # Otherwise, return a boolean indicating whether the path exists
    return _File(string_path, trimmed=trim_file) if return_file else os.path.exists(string_path)
    
def list(directory:str,
         walk:bool=True,
         depth:int=1,
         ignore_folders:List[str]=[],
         trim_files:bool=True) -> dict:
    """
    Walk through a directory and return a list of files and subdirectories.

    Parameters:
        directory (str): The path to the directory to walk through.
        walk (bool): Whether to walk through subdirectories recursively.
        depth (int): The maximum depth to walk through subdirectories.
        ignore_folders (list): A list of folder names to ignore.
        trim_files (bool): Whether to skip retrieving additional file attributes.

    Returns:
        list: A list of files and subdirectories in the directory.
    """
    try:
        if depth > 1 and walk == False:
            warn('Cannot specify depth without walking through subdirectories. Ignoring depth parameter.')
            
        results = []
        def walk_directory(dir_path, current_depth):
            if current_depth > depth:
                return
            for entry in os.scandir(dir_path):
                if entry.is_dir():
                    if entry.name in ignore_folders:
                        continue
                    results.append({'type': 'directory', 'name': entry.name, 'path': entry.path, 'depth': current_depth})
                    walk_directory(entry.path, current_depth + 1)
                else:
                    results.append({'type': 'file', 'name': entry.name, 'path': entry.path, 'depth': current_depth})

        if walk:
            walk_directory(directory, 1)
        else:
            for entry in os.scandir(directory):
                results.append({'type': 'directory' if entry.is_dir() else 'file', 'name': entry.name, 'path': entry.path, 'depth': 0})

        return results
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
                # Log an error message if the destination file already exists
                err(f'File "{destination}" already exists. Call with "overwrite=True" to replace it.')
                return False
            
        shutil.move(source, destination)
        return True
    except Exception as exc:
        # Log an error message if an exception occurs
        err(f'Error moving file from {source} to {destination}: {exc}')
        return False

def read(path:PosixPath|str,
         force_format:str=None,
         return_file:bool=False,
         trim_file:bool=False) -> any:
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
        
        f =_File(string_path, trimmed=trim_file)
        if f.exists:
            if f.is_file:
                content = None
                with open(string_path, 'r') as f:
                    if force_format == 'lines':
                        # Read and return the lines of the file
                        content = f.readlines()
                    elif string_path.endswith('.jsonc') or force_format == 'jsonc':
                        dirty_content = f.read()
                        # Remove comments denoted by '//' to ensure valid JSON
                        clean_content = ''.join(line for line in dirty_content.splitlines() if not line.strip().startswith('//'))
                        content = json.loads(clean_content)
                    elif string_path.endswith('.json') or force_format == 'json':
                        # Load and return JSON data from the file
                        content = json.load(f)
                    elif string_path.endswith('.ini') or force_format == 'ini':
                        # Initialize ConfigParser and read INI configuration
                        config = configparser.ConfigParser()
                        config.read(string_path)
                        content = config
                    elif string_path.endswith('.csv') or force_format == 'csv':
                        # Read and return CSV data as a list of rows
                        content = list(csv.reader(f))
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
                        content = env_vars
                    else:
                        # Read and return plain text data from the file
                        content = f.read()
                
                if content is None:
                    # Log an error if the file is empty
                    warn(f'File "{string_path}" seems to be empty. Returning "None".')
                    return None
                
                if return_file:
                    # Return a _File object with the content if requested
                    f.content = content
                    return f
                return content
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