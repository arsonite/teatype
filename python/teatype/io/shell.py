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
import getpass
import subprocess
import sys

# From package imports
from teatype.enum import EscapeColor
from teatype.logging import err, log

# From-as package imports
from teatype.io import env as current_env

def clear(use_ansi:bool=True) -> None:
    """
    Clears the terminal screen using ANSI escape sequences.

    This function prints ANSI escape codes to reset the terminal cursor position and clear the screen.
    It serves as an alternative to using the 'clear' shell command via subprocess, which can be choppy and slow.
    """
    if use_ansi:
        # Using ANSI escape sequences to clear the terminal instead of clear, since clear is too choppy and slow
        # '\033[H' moves the cursor to the home position (top-left corner) of the terminal.
        # '\033[J' clears the screen from the cursor down.
        print('\033[H\033[J')
    else:
        subprocess.run('clear', shell=True)

def shell(command:str,
          sudo:bool=False,
          cwd:bool=False,
          env:dict=None,
          timeout:float=None,
          mute:bool=False,
          return_output:bool=False,
          ignore_errors:bool=False) -> int:
    """
    Executes a shell command using the subprocess module.

    This method runs a shell command in a subprocess and returns the exit code of the command.
    It provides options to run the command with sudo, set the current working directory,
    pass environment variables, and specify a timeout for the command execution.

    Args:
        command (str): The shell command to be executed.
        sudo (bool): Whether to run the command with sudo privileges. Default is False.
        cwd (bool): Whether to set the current working directory for the command. Default is False.
        env (dict): A dictionary of environment variables to be passed to the command. Default is None.
        timeout (float): The timeout in seconds for the command execution. Default is None.

    Returns:
        int: The exit code of the completed process.
    """
    
    # If sudo is True, prepend 'sudo' to the command
    if sudo:
        # Asking for sudo permissions before script executes any further and suppresses usage information
        subprocess.run('sudo 2>/dev/null', shell=True)
        command = f'sudo {command}'
    
    try:
        # Run the command in a subprocess
        # shell=True allows the command to be executed through the shell
        # cwd is set to None by default, but can be specified if cwd is True
        # env is set to None by default, but can be specified with env
        # timeout is set to None by default, but can be specified with timeout
        # Not using a command list array, since I am using shell=True
        output = subprocess.run(command, 
                                check=not ignore_errors, # Raise an exception if the command fails
                                shell=True, # Execute the command through the shell
                                cwd=None if not cwd else cwd,
                                env=env if not env else current_env.get(),
                                text=return_output,
                                timeout=timeout,
                                stdout=subprocess.PIPE if mute else None,
                                stderr=subprocess.PIPE if mute else None)
        
        if not ignore_errors:
            stderr = str(output.stderr)
            
            # Edge case: If a python subprocess install fails
            if 'exit code: 1' in stderr:
                err(f'Shell command "{command}" seems to have thrown an error.' \
                    'If you believe this to be a mistake, set "ignore_warnings=True",' \
                    'otherwise set "mute=False" to debug.',
                    pad_before=1,
                    pad_after=1)
                output.returncode = 1
    except:
        # If an exception is raised, return the exit code 1 as a failsafe
        # Sometimes the command may fail due to a non-zero exit code, but still return
        # an exit code of 0. In such cases, the exception will be caught and the exit code will be set to 1.
        output.returncode = 1
        
    # Return the exit code of the completed process
    return output.returncode if not return_output else output.stdout.replace('\n', '')

def sudo(max_fail_count:int=3) -> None:
    """
    Executes a sudo command with suppressed error output.

    This function runs the 'sudo' command to elevate privileges without displaying
    any error messages. It is intended to be used as a preliminary step before executing
    other shell commands that require root access.

    Returns:
        None
    """
    log(f'{EscapeColor.LIGHT_GREEN}Elevated privileges required. Please enter your password:')
    password = getpass.getpass('Password: ')
    # Invoke the 'sudo' command to elevate privileges
    # The '2>/dev/null' redirects standard error to null, suppressing any error messages
    # 'shell=True' allows the command to be executed through the shell
    # output = subprocess.run(f'echo {password} | sudo -S ls 2>&1 > /dev/null', shell=True)
    output = subprocess.run(f'echo {password} | sudo -S -v >/dev/null 2>&1', shell=True)
    if output.returncode != 0:
        log(f'{EscapeColor.RED}Invalid password. Abort.', pad_before=1, pad_after=1)
        sys.exit(1)
    else:
        log('Privileges elevated successfully.')

# TODO: Disabled for now, since it will break the shell
# refresh = shell('exec bash')