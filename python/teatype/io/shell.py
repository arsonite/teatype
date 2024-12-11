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
import subprocess

def shell(command:str,
          sudo:bool=False,
          cwd:bool=False,
          env:dict=None,
          timeout:float=None,
          mute:bool=False,
          return_output:bool=False) -> int:
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
        
    # Run the command in a subprocess
    # shell=True allows the command to be executed through the shell
    # cwd is set to None by default, but can be specified if cwd is True
    # env is set to None by default, but can be specified with env
    # timeout is set to None by default, but can be specified with timeout
    # Not using a command list array, since I am using shell=True
    output = subprocess.run(command, 
                            shell=True,
                            cwd=None if not cwd else cwd, 
                            env=None if not env else env,
                            text=return_output, 
                            timeout=timeout,
                            stdout=subprocess.PIPE if mute else None,
                            stderr=subprocess.PIPE if mute else None)
        
    # Return the exit code of the completed process
    return output.returncode if not return_output else output.stdout.replace('\n', '')

refresh = shell('exec bash')