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
import os

# From own imports
from teatype.io import file

def get(key:str=None, default:str=None) -> str | dict:
    """
    Retrieve environment variables.

    This function fetches the value of a specific environment variable if a key is provided.
    If no key is provided, it returns all environment variables as a dictionary.

    Args:
        key (str, optional): The name of the environment variable to retrieve. Defaults to None.
        default (str, optional): The default value to return if the specified environment variable is not found. Defaults to None.

    Returns:
        str | dict: The value of the specified environment variable, or all environment variables if no key is provided.
    """
    # If 'key' is provided, attempt to get its value from the environment variables.
    # If 'key' is not found, return 'default'.
    # If 'key' is not provided, return the entire environment variables dictionary.
    return os.environ.get(key, default) if (key or default) else os.environ

def load(env_path:str=None) -> bool:
    """
    Load environment variables from a .env file into the environment.

    This function checks for the existence of a .env file in the current directory.
    If the file exists, it reads each line, ignoring empty lines and comments,
    and sets the corresponding environment variables.
    """
    try:
        # Load environment variables from .env file if it exists
        env_vars = file.read(env_path if env_path else '.env', force_format='env')
        os.environ.update(env_vars)
        return True
    except FileNotFoundError:
        # Log an error message if the .env file is not found
        print('No .env file found in the current directory.')
        return False
    except Exception as e:
        # Log an error message if an exception occurs
        print(f'An error occurred while loading the .env file: {e}')
        return False