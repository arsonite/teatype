# Copyright (C) 2024-2026 Burak Günaydin
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

# Standard-library imports
import os
from abc import ABC
from collections import deque
from typing import List, Dict, Optional

# Third-party imports
from llama_cpp import Llama
from teatype.ai.models.llm import Inferencer, PromptBuilder
from teatype.io import env, path
from teatype.logging import *

class ConversationalAI(Inferencer):
    chat_history:deque
    messages:List[Dict[str, str]]
    
    def __init__(self,
                 model:str,
                 model_directory:str=None,
                 max_tokens:int=2048,
                 context_size:int=4096,
                 temperature:float=0.7,
                 chat_format:Optional[str]=None, # Force a chat template (e.g. 'chatml', 'llama-2', 'mistral-instruct') instead of auto-detecting one from the model's gguf metadata
                 cpu_cores:int=os.cpu_count(),
                 gpu_layers:int=-1,
                 auto_init:bool=True,
                 max_history:int=10, # max number of turns to keep in memory
                 surpress_output:bool=True,
                 top_p:float=0.9,
                 verbose:bool=False):
        super().__init__(model_path=path.join(model_directory, model),
                         max_tokens=max_tokens,
                         context_size=context_size,
                         temperature=temperature,
                         chat_format=chat_format,
                         cpu_cores=cpu_cores,
                         gpu_layers=gpu_layers,
                         auto_init=auto_init,
                         surpress_output=surpress_output,
                         top_p=top_p,
                         verbose=verbose)
        self.chat_history: deque[Dict[str, str]] = deque(maxlen=max_history)

        def conversional_directive() -> str:
            return """You will reply conversationally, keeping context from earlier turns in the chat. Engage in a conversational manner. Remember previous interactions and provide contextually relevant responses."""
        self.system_prompt = PromptBuilder(additional_runtime_calls=[conversional_directive],
                                           unlock_full_potential=True)

    def _build_conversation_messages(self, user_prompt:str) -> List[Dict[str, str]]:
        """
        Build the full messages list including history + current user input.
        """
        messages = [{'role': 'system', 'content': self.system_prompt}]

        for turn in self.chat_history:
            messages.append({'role': 'user', 'content': turn['user']})
            messages.append({'role': 'assistant', 'content': turn['assistant']})

        messages.append({'role': 'user', 'content': user_prompt})
        return messages

    def chat(self,
             user_prompt:str,
             artificial_delay:float=0.0,
             show_thinking:bool=True,
             stream_response:bool=True) -> str:
        """
        One conversational turn. Tracks history automatically.
        """
        messages = self._build_conversation_messages(user_prompt)
        response = super().__call__(
            messages=messages,
            artificial_delay=artificial_delay,
            show_thinking=show_thinking,
            stream_response=stream_response
        )
        # Save to history
        self.chat_history.append({"user": user_prompt, "assistant": response})
        return response
