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
from typing import List

# From package imports
from teatype.enum import EscapeColor
from teatype.logging import err, log, println, warn

def prompt(prompt_text:str, options:List[any], return_bool:bool=True, colorize:bool=True) -> any:
    """
    Displays a prompt to the user with the given text and a list of available options.

    Args:
        prompt_text (str): The message to display to the user.
        options (List[any]): A list of valid options that the user can choose from.

    Returns:
        any: The user's selected option.
    """
    try:
        if return_bool:
            # Determine if the return type should be a boolean based on the user's preference
            if len(options) > 2:
                # Raise an error if more than two options are provided, as a boolean return is only valid for binary choices
                err('Cannot return a boolean value for more than two options.', exit=True)
                
        # Log the prompt text for debugging or record-keeping purposes
        log(prompt_text, pad_before=1)
        
        # Initialize the string that will display the options
        options_string = '('
        
        # Iterate over each option to build the options string
        for i, option in enumerate(options):
            options_string += f'{option}'
            # If it's the last option, append a '/' to indicate the end
            if i < len(options) - 1:
                options_string += '/'
        
        # Close the options string with a colon and space for user input
        options_string += '): '
        
        # Prompt the user for input using the constructed options string
        prompt_answer = input(options_string)
        println()
        
        # Validate the user's input against the available options
        if prompt_answer not in options:
            # Log an error message and exit if the input is invalid
            err('Invalid input. Available options are: ' + ', '.join(options), exit=True)
        
        # Return the validated user input
        return prompt_answer == options[0] if return_bool else prompt_answer
    except KeyboardInterrupt:
        warn('User interrupted the input prompt.', use_log_tag=False, verbose=False)
    except:
        err(f'An error occurred while prompting the user for input', exit=True, traceback=True)