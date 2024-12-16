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

# From system imports
from pathlib import Path

def parent(reverse_depth: int = 1, stringify: bool = True) -> str:
    """
    Retrieve the parent directory of the script's path.

    Args:
        reverse_depth (int): The number of levels to traverse up the directory tree.
                             Defaults to 1.
        stringify (bool): If True, returns the parent path as a string.
                           If False, returns as a Path object. Defaults to True.

    Returns:
        str: The parent directory path as a string if stringify is True.
        Path: The parent directory as a Path object if stringify is False.
    """
    script_path = script(stringify=False)  # Get the script path as a Path object
    parent = script_path.parent # Get the immediate parent directory
    for _ in range(reverse_depth - 1):
        parent = parent.parent # Traverse up the directory tree
    return str(parent) if stringify else parent # Return the parent path as string or Path object

def script(stringify: bool = True) -> str:
    """
    Retrieve the absolute path of the current script.

    Args:
        stringify (bool): If True, returns the script path as a string.
                           If False, returns as a Path object. Defaults to True.

    Returns:
        str: The absolute script path as a string if stringify is True.
        Path: The absolute script path as a Path object if stringify is False.
    """
    script_path = Path(__file__).resolve() # Resolve the absolute path of the current script
    return str(script_path) if stringify else script_path # Return as string or Path object

def workdir(stringify: bool = True) -> str:
    """
    Retrieve the current working directory.

    Args:
        stringify (bool): If True, returns the working directory as a string.
                           If False, returns as a Path object. Defaults to True.

    Returns:
        str: The current working directory as a string if stringify is True.
        Path: The current working directory as a Path object if stringify is False.
    """
    cwd_path = Path.cwd() # Get the current working directory as a Path object
    return str(cwd_path) if stringify else cwd_path # Return as string or Path object