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

# From system imports
import configparser
import csv
import json

# From own imports
from teatype.logging import err

def append(path:str, data:any) -> bool:
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
            if path.endswith('.json'):
                # Append JSON data to the file
                json.dump(data, f)
            elif path.endswith('.ini'):
                # Initialize ConfigParser and read existing INI configuration
                config = configparser.ConfigParser()
                config.read(path)
                # Update the configuration with new data
                config.update(data)
                # Write the updated configuration back to the file
                config.write(f)
            elif path.endswith('.csv'):
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

def read(path:str, force:str|None=None) -> any:
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
        if os.path.isfile(path):
            with open(path, 'r') as f:
                if path.endswith('.json') or force == 'json':
                    # Load and return JSON data from the file
                    return json.load(f)
                elif path.endswith('.ini') or force == 'ini':
                    # Initialize ConfigParser and read INI configuration
                    config = configparser.ConfigParser()
                    config.read(path)
                    return config
                elif path.endswith('.csv') or force == 'csv':
                    # Read and return CSV data as a list of rows
                    return list(csv.reader(f))
                elif path.endswith('.env') or force == 'env':
                    # Parse and return environment variables from the file
                    env_vars = {}
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            key, _, value = line.partition('=')
                            env_vars[key.strip()] = value.strip()
                    return env_vars
                elif force == 'lines':
                    # Read and return the lines of the file
                    return f.readlines()
                else:
                    # Read and return plain text data from the file
                    return f.read()
        else:
            file_not_found_message = f'File "{path}" does not exist.'
            # Log an error message if the file does not exist
            err(file_not_found_message)
            raise FileNotFoundError(file_not_found_message)
    except Exception as exc:
        # Log an error message if an exception occurs
        err(f'Error reading file "{path}": {exc}')
        raise exc

def write(path:str, data:any, force:str|None=None) -> bool:
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
            if force == 'lines':
                # Write multiple lines to the file
                f.writelines(data)
            elif path.endswith('.json') or force == 'json':
                # Write JSON data to the file
                json.dump(data, f)
            elif path.endswith('.ini') or force == 'ini':
                # Initialize ConfigParser and update with new data
                config = configparser.ConfigParser()
                config.update(data)
                # Write the updated configuration to the file
                config.write(f)
            elif path.endswith('.csv') or force == 'csv':
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