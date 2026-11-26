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
import importlib
from importlib.util import find_spec

# Probing for the backend is enough to know about GPU support; actually importing the
# engines pulls in teatype.comms/teatype.modulo and makes every `import teatype.ai` slow.
__GPU_SUPPORT__ = find_spec('llama_cpp') is not None

_LAZY_ATTRS = {
    'BaseAIEngine': ('.engines.BaseAIEngine', 'BaseAIEngine'),
    'LLMEngine': ('.engines.LLMEngine', 'LLMEngine'),
    'load_llm_model': ('.models.llm.loader', 'load_model'),
    'LLMInferencer': ('.models.llm.inference', 'Inferencer'),
    'OpenGPT': ('.OpenGPT', 'OpenGPT'),
}

def __getattr__(name):
    if name in _LAZY_ATTRS:
        module_name, attribute = _LAZY_ATTRS[name]
        return getattr(importlib.import_module(module_name, __name__), attribute)
    raise AttributeError(f'module {__name__!r} has no attribute {name!r}')