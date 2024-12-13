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
import time

from teatype.enum import EscapeColor
from teatype.logging import err, log

class GLOBAL_STOPWATCH_CONFIG:
    """
    Global configuration for the stopwatch utility.
    """
    DETECT_UNCLOSED_STOPWATCHES:bool=False # Debug option to detect unclosed stopwatches on runtime
    DISABLE_STOPWATCHES:bool=True
    PRINT_START:bool=False
    TIME_CONVERSION:bool=False

def stopwatch(label:str=None):
    """
    Using class and function closure to measure execution time between calls.
    If called with a label, it starts the timer and stores the label.
    If called without a label, it prints the elapsed time since the last labeled call.
    """
        
    # Check if the stopwatches are disabled
    if GLOBAL_STOPWATCH_CONFIG.DISABLE_STOPWATCHES:
        return
    
    # Class closure internal state to track the timer
    state = getattr(stopwatch, '_state', None)
    if state is None:
        stopwatch._state = state = {}
        
    # Debug option to detect unclosed stopwatches on runtime
    if GLOBAL_STOPWATCH_CONFIG.DETECT_UNCLOSED_STOPWATCHES:
        last_label = state.get('last_label')
        if last_label:
            keys = list(state.keys())
            if keys[-1] != last_label:
                print(state)
                err(f'Stopwatch "{keys[-1]}" was never closed.', traceback=True)
                return

    if label:
        # Start a timer for the given label
        state['last_label'] = label
        state[label] = time.time()
        if GLOBAL_STOPWATCH_CONFIG.PRINT_START:
            log(f'Started stopwatch for "{label}".')
    else:
        # Ensure there is a previous label to calculate elapsed time
        last_label = state.get('last_label')
        if last_label and last_label in state:
            elapsed = time.time() - state[last_label]
            
            if GLOBAL_STOPWATCH_CONFIG.TIME_CONVERSION:
                if elapsed < 1e-6:
                    elapsed = f'{elapsed * 1e9:.2f} nanoseconds'
                elif elapsed < 1e-3:
                    elapsed = f'{elapsed * 1e6:.2f} microseconds'
                elif elapsed < 1:
                    elapsed = f'{elapsed * 1e3:.2f} milliseconds'
                elif elapsed < 60:
                    elapsed = f'{elapsed:.2f} seconds'
                elif elapsed < 3600:
                    minutes = int(elapsed // 60)
                    seconds = elapsed % 60
                    elapsed = f'{minutes} minutes, {seconds:.2f} seconds'
                else:
                    hours = int(elapsed // 3600)
                    minutes = int((elapsed % 3600) // 60)
                    seconds = elapsed % 60
                    elapsed = f'{hours} hours, {minutes} minutes, {seconds:.2f}'
            else:
                elapsed = f'{elapsed:.4f} seconds'
            
            log(f'{EscapeColor.BLUE}Stopwatch {EscapeColor.LIGHT_CYAN}[{last_label}]{EscapeColor.LIGHT_GREEN}: {elapsed}.')
        else:
            # Replace with proper critical logger without an exit
            raise ValueError('No label found to measure elapsed time.')