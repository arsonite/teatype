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
import asyncio
import inspect
import json
import ssl
import threading

# Third-party imports
import websockets
from pydantic import ValidationError

# Local imports
from teatype.comms.ws.ContractMessage import ContractMessage
from teatype.comms.ws.MessageBuffer import MessageBuffer
from teatype.logging import *

class Websocket:
    """
    Connects to a WebSocket URL, reads JSON data in a background asyncio
    task, and dispatches it to registered callback handlers.

    Every message must satisfy the ContractMessage schema, i.e. carry a
    string 'key'. Register handlers with register_callback(key, hook); a
    handler registered under key='*' runs on every message, in addition to
    the one matching the message's 'key'. Handlers may be sync or async:
        async def my_hook(data: dict) -> None

    Usage
    -----
        ws = Websocket(url)
        ws.register_callback(key='*', hook=my_hook)
        await ws.start()
        ...
        await ws.stop()
    """
    _bg_loop:asyncio.AbstractEventLoop
    _bg_thread:threading.Thread
    _task:asyncio.Task
    _use_buffer:bool
    _ws:websockets.WebSocketClientProtocol
    
    callback_handlers:dict
    has_secure_connection:bool=False
    input_buffer:MessageBuffer
    output_buffer:MessageBuffer
    ssl_verify:bool
    url:str
    
    def __init__(self,
                 url:str,
                 *,
                 auto_connect:bool=True,
                 buffer_size:int=0,
                 ssl_verify:bool=False):
        self.ssl_verify = ssl_verify
        self.url = url
        
        self.callback_handlers = {}
        
        if buffer_size > 0:
            self._use_buffer = True
            self.input_buffer = MessageBuffer()
            self.output_buffer = MessageBuffer()
        else:
            self._use_buffer = False
            self.input_buffer = None
            self.output_buffer = None
        
        self._bg_loop = None
        self._bg_thread = None
        self._task = None
        self._ws = None
        
        if not ssl_verify:
            self.has_secure_connection = False
        elif ssl_verify and url.startswith('wss://'):
            self.has_secure_connection = True
        
        if auto_connect:
            asyncio.create_task(self.start())
            
    ##############
    # Properties #
    ##############
    
    @property
    def connected(self) -> bool:
        return self._ws is not None and not self._ws.closed
    
    #############
    # Internals #
    #############

    async def _loop(self):
        try:
            async for raw in self._ws:
                try:
                    data = json.loads(raw)
                except Exception:
                    continue

                if not data or not self._is_valid(data):
                    continue
                
                if self._use_buffer:
                    self.input_buffer.add(data)
                await self._dispatch(data)

        except websockets.ConnectionClosed:
            pass

    async def _dispatch(self, data:dict):
        # '*' is the wildcard handler, always fires alongside the keyed one
        for callback_key in {data.get('key'), '*'}:
            callback_handler = self.callback_handlers.get(callback_key)
            if callback_handler:
                if inspect.iscoroutinefunction(callback_handler):
                    await callback_handler(data)
                else:
                    callback_handler(data)

    @staticmethod
    def _is_valid(data:dict) -> bool:
        try:
            ContractMessage(**data)
            return True
        except ValidationError:
            return False

    ######################
    # Context Manager API #
    ######################

    def __enter__(self):
        self._bg_loop = asyncio.new_event_loop()
        self._bg_thread = threading.Thread(target=self._bg_loop.run_forever, daemon=True)
        self._bg_thread.start()
        future = asyncio.run_coroutine_threadsafe(self.start(), self._bg_loop)
        if not future.result(timeout=10):
            self._bg_loop.call_soon_threadsafe(self._bg_loop.stop)
            self._bg_thread.join()
            err(f'[comms.ws.Websocket] Failed to connect to {self.url}',
                raise_exception=ConnectionError)
        return self

    def __exit__(self, *_):
        asyncio.run_coroutine_threadsafe(self.stop(), self._bg_loop).result(timeout=5)
        self._bg_loop.call_soon_threadsafe(self._bg_loop.stop)
        self._bg_thread.join()
        self._bg_loop.close()
        self._bg_loop = None
        self._bg_thread = None

    ##############
    # Public API #
    ##############    

    def register_callback(self, key:str, hook:callable):
        """
        Registers hook to run when incoming data has 'key': key. Use key='*' for a wildcard hook that always runs.
        """
        self.callback_handlers[key] = hook

    async def send(self, data:dict):
        if not self._is_valid(data):
            err(f'[comms.ws.Websocket] Outgoing data does not match ContractMessage schema: {data}',
                raise_exception=ValueError)
        if self._use_buffer:
            self.output_buffer.add(data)
        await self._ws.send(json.dumps(data))

    async def start(self) -> bool:
        try:
            ssl_context = None
            if not self.ssl_verify:
                ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE
            self._ws = await websockets.connect(self.url, ssl=ssl_context)
        except Exception as exc:
            print(f'[WS] Connection failed: {exc}')
            return False
        self._task = asyncio.create_task(self._loop())
        return True

    async def stop(self):
        if self._task:
            self._task.cancel()
            self._task = None
        if self._ws:
            await self._ws.close()
            self._ws = None
            
if __name__ == '__main__':
    import asyncio

    async def main():
        async def my_hook(data):
            print(f"Received: {data}")

        ws = Websocket('wss://localhost:8765', auto_connect=False)
        ws.register_callback(key='*', hook=my_hook)
        await ws.start()

        # Send a test message
        await ws.send({"key": "test", "request_id": "123", "message": "Hello, WebSocket!"})

        # Keep the connection open for a while to receive messages
        await asyncio.sleep(10)

        await ws.stop()

    asyncio.run(main())