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

def load_env():
    """
    Load environment variables from a .env file into the environment.

    This function checks for the existence of a .env file in the current directory.
    If the file exists, it reads each line, ignoring empty lines and comments,
    and sets the corresponding environment variables.
    """
    # Load environment variables from .env file if it exists
    env_file = file.read('.env')
    for line in env_file:
        # Check if the line is not empty and does not start with a comment
        if line.strip() and not line.startswith('#'):
            # Split the line into key and value using the first '=' as delimiter
            key, _, value = line.partition('=')
            # Strip whitespace and set the environment variable
            os.environ[key.strip()] = value.strip()