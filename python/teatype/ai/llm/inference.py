# Copyright © 2025-2026 @arsonite.
#
# This software and all its associated assets, code, designs, dialogue systems, characters, and in-game logic
# are proprietary and owned exclusively by @arsonite. Permission is granted to the user to install and play
# the game for personal use. Redistribution, resale, modification, reverse-engineering, or reuse of any part
# of the game is strictly prohibited without written permission.
#
# Third-party open-source components are used under their respective licenses.
# See /third-party-licenses.md for details.
#
# THE GAME IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING, BUT
# NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE,
# NON-INFRINGEMENT, OR TITLE. @arsonite DOES NOT WARRANT THAT THE GAME WILL MEET YOUR
# REQUIREMENTS OR THAT OPERATION OF THE GAME WILL BE UNINTERRUPTED OR ERROR-FREE.
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# System imports
import itertools
import os
import sys
import threading
import time

# From system imports
from abc import ABC
from collections import deque
from typing import List, Dict, Optional

# From package imports
from llama_cpp import Llama
from teatype.ai.llm import load_model, PromptBuilder
from teatype.enum import EscapeColor
from teatype.io import env, file, path
from teatype.logging import *

ROOT_PATH = env.get('TEATYPE_WORKSPACE_PATH')
MODELS_PATH = path.join(ROOT_PATH, 'cli', 'dist', 'llm-models')

class Inferencer():
    max_tokens:int
    model:Optional[Llama]
    temperature:float
    top_p:float
    unlock_full_potential:bool
    
    def __init__(self,
                 model:str,
                 model_directory:str=None,
                 max_tokens:int=2048, # The maximum number of tokens to generate in the output - affects length of responses
                 context_size:int=4096, # The context window size of the model - Affects how much text the model can "see" at once
                 temperature:float=0.7, # Affects randomness. Lowering results in less random completions
                 cpu_cores:int=os.cpu_count(),
                 gpu_layers:int=-1,
                 auto_init:bool=True,
                 surpress_output:bool=True,
                 top_p:float=0.9, # nucleus sampling - Affects diversity. Lower values makes output more focused
                 unlock_full_potential:bool=False,
                 verbose:bool=False):
        """
        Base class for LLM inferencers.
        """
        env.set('LLAMA_SET_ROWS', '1')

        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.unlock_full_potential = unlock_full_potential
        
        self.model_name = model
        self.model_directory = model_directory if model_directory else MODELS_PATH
        
        if auto_init:
            self.initialize_model(context_size=context_size,
                                  cpu_cores=cpu_cores,
                                  gpu_layers=gpu_layers,
                                  surpress_output=surpress_output,
                                  verbose=verbose)
    
    def __call__(self,
                 user_prompt:str,
                 artificial_delay:float=0.0,
                 show_thinking:bool=True,
                 stream_response:bool=True,
                 use_prompt_builder:bool=True) -> str:
        """
        Generate text from LLaMA model with optional streaming.
        Shows a spinner until the first token or response is available.
        """
        def _spinner(stop_event):
            for symbol in itertools.cycle('|/-\\'):
                if stop_event.is_set():
                    break
                sys.stdout.write('\rThinking ' + symbol)
                sys.stdout.flush()
                time.sleep(0.1)
            sys.stdout.write('\r' + ' ' * 20 + '\r') # clear line
            
        response = ''
        if use_prompt_builder:
            input = PromptBuilder(user_prompt, unlock_full_potential=self.unlock_full_potential)
        else:
            input = user_prompt

        if show_thinking:
            # Spinner setup
            first_token = True
            stop_event = threading.Event()
            spinner_thread = threading.Thread(target=_spinner, args=(stop_event,))
            spinner_thread.start()
        
        if artificial_delay > 0:
            time.sleep(artificial_delay)

        if stream_response:
            for output in self.model(
                input,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=self.top_p,
                stream=True
            ):
                token = output['choices'][0]['text']

                if show_thinking:
                    if first_token: # stop spinner when first token arrives
                        stop_event.set()
                        spinner_thread.join()
                        first_token = False

                print(f'{EscapeColor.LIGHT_GREEN}{token}{EscapeColor.RESET}', end='', flush=True)
                response += token
            println()
        else:
            raw_output = self.model(
                input,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=self.top_p,
                stream=False
            )
            if show_thinking:
                stop_event.set()
                spinner_thread.join()
            response = raw_output['choices'][0]['text']

        # Strip leading newlines/whitespace only once at the start
        return response.lstrip()
            
    def initialize_model(self,
                         context_size:int=4096,
                         cpu_cores:int=os.cpu_count(),
                         gpu_layers:int=-1,
                         surpress_output:bool=True,
                         verbose:bool=False,) -> Llama|None:
            """
            Initializes the llama-cpp model with raw prompt-based inference.
            """
            # TODO: Download model if not present from huggingface
            found_model_files = file.list(self.model_directory)
            matching_model = [f for f in found_model_files if self.model_name in f.name][0]
            if not matching_model:
                raise ValueError(f'Model {self.model_name} not found in {MODELS_PATH}. Please place the model file there or specify a different `model_directory`.')

            self.model = load_model(model_path=matching_model.path,
                                    context_size=context_size,
                                    cpu_cores=cpu_cores,
                                    gpu_layers=gpu_layers,
                                    surpress_output=surpress_output,
                                    verbose=verbose)
            self.on_init()
    
    #########
    # Hooks #
    #########
    
    def on_init(self):
        pass