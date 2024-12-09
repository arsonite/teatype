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

# From system imports
from typing import List

# TODO: Implement as package class
# TODO: Ommit commands in favor of flags with values (e.g. --name "John Doe" or maybe even "=" assignement e.g. --name="John Doe")
class Command:
    """
    Represents a command-line command.

    Attributes:
        name (str): The name of the command.
        help (str): A brief description of the command.
        help_extension (List[str], optional): Additional help information for the command.
        value (Any): The value of the command, initially set to None.
    """
    def __init__(self,
                name:str,
                shorthand:str,
                help:str|List[str]):
        self.name = name
        self.shorthand = shorthand
        self.help = help
        
        self.value = None