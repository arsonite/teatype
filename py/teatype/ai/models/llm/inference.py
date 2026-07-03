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
import itertools
import os
import sys
import threading
import time
from typing import Generator, Optional

# Third-party imports
from llama_cpp import Llama, llama_chat_format
from teatype.ai.models.llm import load_model, PromptBuilder
from teatype.enum import XTerm
from teatype.io import env, file, path
from teatype.logging import *
from teatype.toolkit import colorwrap

APPLY_WHITESPACE_PATCH = True

# Reasoning-model chat templates (Qwen3, DeepSeek-R1, etc.) wrap their internal
# reasoning in these tags. We detect them in the raw token stream to color
# reasoning content in gray (or hide it) without needing per-model knowledge.
THINK_OPEN_TAG = '<think>'
THINK_CLOSE_TAG = '</think>'

class Inferencer():
    chat_format:Optional[str]
    enable_kv_cache:bool
    max_tokens:int
    model:Optional[Llama]
    model_directory:str
    model_extension:str
    model_loaded:bool
    model_name:str
    model_starts_thinking:bool
    model_path:str
    temperature:float
    top_p:float
    unlock_full_potential:bool
    
    def __init__(self,
                 model_path:str,
                 max_tokens:int=2048, # The maximum number of tokens to generate in the output - affects length of responses
                 context_size:int=4096, # The context window size of the model - Affects how much text the model can "see" at once
                 temperature:float=0.7, # Affects randomness. Lowering results in less random completions
                 chat_format:Optional[str]=None, # Force a chat template (e.g. 'chatml', 'llama-2', 'mistral-instruct') instead of auto-detecting one from the model's gguf metadata
                 cpu_cores:int=os.cpu_count(),
                 gpu_layers:int=-1,
                 auto_init:bool=True,
                 enable_kv_cache:bool=True,
                 surpress_output:bool=True,
                 top_p:float=0.9, # nucleus sampling - Affects diversity. Lower values makes output more focused
                 unlock_full_potential:bool=True,
                 verbose:bool=False):
        """
        Base class for LLM inferencers.
        """
        env.set('LLAMA_SET_ROWS', '1')

        self.reload(model_path=model_path,
                    max_tokens=max_tokens,
                    context_size=context_size,
                    temperature=temperature,
                    chat_format=chat_format,
                    cpu_cores=cpu_cores,
                    gpu_layers=gpu_layers,
                    auto_init=auto_init,
                    enable_kv_cache=enable_kv_cache,
                    surpress_output=surpress_output,
                    top_p=top_p,
                    unlock_full_potential=unlock_full_potential,
                    verbose=verbose)
    
    def _spinner(self, stop_event):
        for symbol in itertools.cycle('|/-\\'):
            if stop_event.is_set():
                break
            sys.stdout.write('\rThinking ' + symbol)
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write('\r' + ' ' * 20 + '\r') # clear line

    def _build_messages(self, user_prompt:str, use_prompt_builder:bool) -> list[dict]:
        """
        Builds the chat `messages` list. Turn structure (system/user/assistant) is applied
        by the model's own chat template in `create_chat_completion`, so no manual
        'User:'/'Assistant:' framing or stop-string guessing is needed here.
        """
        messages = []
        if use_prompt_builder:
            messages.append({'role': 'system', 'content': PromptBuilder(unlock_full_potential=self.unlock_full_potential)})
        messages.append({'role': 'user', 'content': user_prompt})
        return messages

    def _create_chat_completion(self, messages:list[dict], stream:bool, enable_thinking:bool=True):
        """
        Calls the model's chat-completion handler directly instead of `Llama.create_chat_completion`,
        because that method has a fixed signature with no **kwargs passthrough. The resolved handler
        (same resolution order llama-cpp itself uses) forwards arbitrary kwargs straight into the
        model's jinja chat template context, so `enable_thinking` reaches templates that support it
        (Qwen3, DeepSeek-R1, ...) and is silently ignored by templates that don't - a generic,
        model-family-agnostic way to actually disable reasoning at generation time rather than just
        hiding it from the printed output.
        """
        handler = (self.model.chat_handler
                  or self.model._chat_handlers.get(self.model.chat_format)
                  or llama_chat_format.get_chat_completion_handler(self.model.chat_format))
        return handler(llama=self.model,
                       messages=messages,
                       max_tokens=self.max_tokens,
                       stream=stream,
                       temperature=self.temperature,
                       top_p=self.top_p,
                       enable_thinking=enable_thinking)

    def _stream_tokens(self, messages:list[dict], enable_thinking:bool=True) -> Generator[str, None, None]:
        # NOTE: this must be the only place emitting `yield` in the streaming
        # path - if `__call__` itself contained a `yield`, Python would turn
        # the whole method into a generator function, so calling it would
        # never actually run any inference (it'd just hand back an inert
        # generator object) unless the caller iterated it.
        first_token = True
        stop_event = threading.Event()
        spinner_thread = threading.Thread(target=self._spinner, args=(stop_event,))
        spinner_thread.start()

        for output in self._create_chat_completion(messages, stream=True, enable_thinking=enable_thinking):
            token = output['choices'][0].get('delta', {}).get('content')
            if not token:
                continue # role-only or empty delta chunks

            if first_token:
                stop_event.set() # stop spinner when first token arrives
                spinner_thread.join()

                first_token = False
                if APPLY_WHITESPACE_PATCH:
                    token = token.lstrip() # Strip leading whitespace only once at the start

            yield token

        if first_token:
            # No tokens were ever produced - make sure the spinner still stops
            stop_event.set()
            spinner_thread.join()

    @staticmethod
    def strip_thinking(text:str) -> str:
        """
        Removes a leading reasoning block from a completed response, up to and
        including the first </think> tag. Handles both explicit-open templates
        (text contains '<think>...</think>') and implicit-open ones (the chat
        template itself emits '<think>' before generation starts, so only the
        closing tag shows up in the generated text). No-op if no closing tag
        is present. Useful before storing assistant turns in conversation
        history, so a model doesn't keep re-reading its own previous reasoning.
        """
        end = text.find(THINK_CLOSE_TAG)
        if end == -1:
            return text.strip()
        return text[end + len(THINK_CLOSE_TAG):].strip()

    def _render_thinking(self,
                         token_iter:Generator[str, None, None],
                         colorized_output:XTerm.Colors,
                         show_thinking:bool) -> Generator[str, None, None]:
        """
        Wraps a raw token generator, detecting <think>...</think> reasoning blocks
        (used by Qwen3, DeepSeek-R1, and similar reasoning models) and yielding
        print-ready, already-colorized chunks:
          - show_thinking=True (default): reasoning content is printed in gray.
          - show_thinking=False: reasoning content is dropped entirely.
        If a model never emits the tags, this is a no-op passthrough.
        """
        tags = (THINK_OPEN_TAG, THINK_CLOSE_TAG)
        max_partial = max(len(tag) for tag in tags) - 1

        def emit(text:str, thinking:bool) -> str:
            if not text:
                return ''
            if thinking:
                return colorwrap(text, 'gray') if show_thinking else ''
            return colorwrap(text, colorized_output) if colorized_output else text

        buffer = ''
        # Some reasoning templates (e.g. Qwen3) inject the opening <think> tag
        # themselves as part of the generation prompt, so the model's own output
        # starts already 'inside' a thinking block and only emits the closing tag.
        in_thinking = self.model_starts_thinking
        for token in token_iter:
            buffer += token
            while True:
                tag = THINK_CLOSE_TAG if in_thinking else THINK_OPEN_TAG
                idx = buffer.find(tag)
                if idx == -1:
                    break
                before, buffer = buffer[:idx], buffer[idx + len(tag):]
                out = emit(before, in_thinking)
                if out:
                    yield out
                in_thinking = not in_thinking
            # Hold back a tail that could be the start of a split tag until more arrives
            if len(buffer) > max_partial:
                safe_length = len(buffer) - max_partial
                out = emit(buffer[:safe_length], in_thinking)
                buffer = buffer[safe_length:]
                if out:
                    yield out
        if buffer:
            out = emit(buffer, in_thinking)
            if out:
                yield out

    def __call__(self,
                 user_prompt:str=None,
                 artificial_delay:float=0.0,
                 colorized_output:XTerm.Colors=None,
                 decorator:str=None,
                 enable_thinking:bool=True, # actually enable/disable the model's reasoning step at generation time (forwarded to the chat template; no-op for templates that don't support it)
                 messages:list[dict]=None, # pass a pre-built multi-turn messages list (e.g. from ConversationalAI) instead of a single user_prompt
                 show_thinking:bool=True, # print <think>...</think> reasoning content in gray; set False to hide it entirely (no-op if the model doesn't emit reasoning tags)
                 stream_response:bool=True,
                 use_prompt_builder:bool=True,
                 yield_token:bool=False) -> str|Generator[str, None, None]:
        """
        Generate text from LLaMA model with optional streaming.
        Shows a spinner until the first token or response is available.
        """
        if messages is None:
            messages = self._build_messages(user_prompt, use_prompt_builder)

        if artificial_delay > 0:
            time.sleep(artificial_delay)

        if not self.enable_kv_cache:
            self.model.reset()
        if decorator:
            print(decorator + ':', end=' ', flush=True)

        if stream_response and yield_token:
            return self._stream_tokens(messages, enable_thinking)

        if stream_response:
            response = ''
            raw_tokens = self._stream_tokens(messages, enable_thinking)
            def _tap(iterator):
                nonlocal response
                for token in iterator:
                    response += token
                    yield token
            for chunk in self._render_thinking(_tap(raw_tokens), colorized_output, show_thinking):
                print(chunk, end='', flush=True)
            println()
            return response.lstrip()

        stop_event = threading.Event()
        spinner_thread = threading.Thread(target=self._spinner, args=(stop_event,))
        spinner_thread.start()
        raw_output = self._create_chat_completion(messages, stream=False, enable_thinking=enable_thinking)
        stop_event.set()
        spinner_thread.join()

        # Strip leading newlines/whitespace only once at the start
        return raw_output['choices'][0]['message']['content'].lstrip()
    
    def reload(self,
               model_path:str,
               max_tokens:int=2048,
               context_size:int=4096,
               temperature:float=0.7,
               chat_format:Optional[str]=None,
               cpu_cores:int=os.cpu_count(),
               gpu_layers:int=-1,
               auto_init:bool=True,
               enable_kv_cache:bool=True,
               surpress_output:bool=True,
               top_p:float=0.9,
               unlock_full_potential:bool=True,
               verbose:bool=False):
        self.chat_format = chat_format
        self.enable_kv_cache = enable_kv_cache
        self.model_path = model_path
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.unlock_full_potential = unlock_full_potential
        
        self.model_directory = self.model_path.rsplit('/', 1)[0]
        self.model_extension = self.model_path.rsplit('.', 1)[-1]
        self.model_loaded = False
        self.model_name = self.model_path.rsplit('/', 1)[-1].rsplit('.', 1)[0]
        self.model_starts_thinking = False
        
        if auto_init:
            self.initialize_model(context_size=context_size,
                                  cpu_cores=cpu_cores,
                                  gpu_layers=gpu_layers,
                                  surpress_output=surpress_output,
                                  verbose=verbose)
            
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
                raise ValueError(f'Model {self.model_name} not found in {self.model_path}. Please place the model file there or specify a different `model_path`.')

            self.model = load_model(model_path=matching_model.path,
                                    context_size=context_size,
                                    cpu_cores=cpu_cores,
                                    gpu_layers=gpu_layers,
                                    chat_format=self.chat_format,
                                    surpress_output=surpress_output,
                                    verbose=verbose)
            # Detect templates that open the reasoning block themselves (e.g. Qwen3's
            # chat template appends '<think>\n' to the generation prompt), meaning the
            # model's own generated text never contains the opening tag - only '</think>'.
            chat_template = (self.model.metadata or {}).get('tokenizer.chat_template', '')
            self.model_starts_thinking = THINK_OPEN_TAG in chat_template
            self.model_loaded = True
            self.on_init()
    
    #########
    # Hooks #
    #########
    
    def on_init(self):
        pass
    
if __name__ == '__main__':
        from teatype.io import prompt
        
        verbose = True
        
        parent_directory = path.caller_parent(reverse_depth=2)
        cli_directory = path.join(parent_directory, 'cli')
        cli_dist_directory = path.join(cli_directory, 'dist')
        model_directory = path.join(cli_dist_directory, 'llm-models')
        conversational_model_directory = path.join(model_directory, 'conversational')
        if not path.exists(conversational_model_directory):
            warn(f'Conversational model directory not found at {conversational_model_directory}. Creating it. Please re-run this script after placing your model there.',
                 use_prefix=False)
            path.create(conversational_model_directory)
            println()
            exit(1)

        stream = True
        
        default_model_file_path = path.join(conversational_model_directory, 'default-model.txt')
        if not file.exists(default_model_file_path):
            file.write(default_model_file_path, '')
        
        default_model = file.read(default_model_file_path).strip()
        if default_model == '' or default_model is None:
            hint('No default model set. Select one of these available local models:',
                 use_prefix=False)
            available_local_models = [f.name.split('.gguf')[0] for f in file.list(conversational_model_directory, only_include='.gguf')]
            prompt_options = {str(i+1): model_name for i, model_name in enumerate(available_local_models)}
            for available_model_index, available_model_name in prompt_options.items():
                model_file_path = path.join(conversational_model_directory, f'{available_model_name}.gguf')
                file_size = file.size(model_file_path, human_readable=True)
                log(f'  [{available_model_index}] {available_model_name} ({file_size})')
            selection = prompt('Please enter the number corresponding to your choice:',
                               choices=prompt_options,
                               return_input=True)
            default_model = available_local_models[int(selection)-1]
            file.write(default_model_file_path, default_model)
        
        default_model = file.read(path.join(conversational_model_directory, 'default-model.txt'))
        
        user_prompt = prompt('Enter your prompt:', return_input=True)
        
        from teatype.ai.models.llm import Inferencer
        llm = Inferencer(model=default_model,
                         model_directory=conversational_model_directory)
        response = llm(user_prompt=user_prompt,
                       stream_response=stream)
        println()