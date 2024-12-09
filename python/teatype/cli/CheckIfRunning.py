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

# Package imports
import psutil

# From package imports
from teatype.cli import BaseCLI
from teatype.logging import err, log, nl

class CheckIfRunning(BaseCLI):
    def meta(self):
        return {
            'name': 'check-if-running',
            'shorthand': 'cr',
            'help': 'Check if a process is running',
            'flags': [
                {
                    'short': 'h',
                    'long': 'hide-output',
                    'help': 'Hide verbose output of script',
                    'required': False
                }
            ],
        }

    def execute(self):
        verbose = not self.get_flag('hide-output')
        
        if verbose:
            nl()
            
        if not hasattr(self, 'process_names'):
            err('No "self.process_names" provided in source code. Please provide a process name in the pre_execute function.',
                exit=True)
            nl()
        
        process_pids = []
        for process_name in self.process_names:
            found = False
            for process in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    # Check if process_name appears in the full command line
                    if process_name in ' '.join(process.info['cmdline']):
                        process_pid = process.info['pid']
                        process_pids.append(process_pid)
                        if verbose:
                            log(f'Process "{process_name}" is running with PID "{process_pid}"')
                        found = True
                        break
                except (psutil.NoSuchProcess, psutil.AccessDenied, KeyError):
                    # Skip processes that we can't access or have disappeared
                    continue
            
            if not found:
                if verbose:
                    log(f'Process "{process_name}" is not running')
                    
        if verbose:
            nl()
        
        return process_pids

if __name__ == '__main__':
    CheckIfRunning()