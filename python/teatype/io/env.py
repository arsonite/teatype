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

# From own imports
from teatype.io import file

def load(env_path:str|None=None) -> bool:
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