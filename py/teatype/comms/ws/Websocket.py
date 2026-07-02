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

# Local imports
from teatype.logging import *

class Websocket:
    """
    Connects to a WebSocket URL, reads JSON data in a background asyncio
    task, and fires registered callbacks whenever data arrives.

    Callbacks are plain async functions with signature:
        async def my_hook(data: dict) -> None

    Usage
    -----
        ws = Websocket(url, hook=my_hook)
        await ws.start()
        ...
        await ws.stop()
    """
    _bg_loop:asyncio.AbstractEventLoop
    _bg_thread:threading.Thread
    _task:asyncio.Task
    _ws:websockets.WebSocketClientProtocol
    
    has_secure_connection:bool=False
    hook:callable
    ssl_verify:bool
    url:str
    
    def __init__(self, url:str, hook:callable, *, auto_connect:bool=True, ssl_verify:bool=False):
        self.hook = hook
        self.ssl_verify = ssl_verify
        self.url = url
        
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

                if data:
                    if inspect.iscoroutinefunction(self.hook):
                        await self.hook(data)
                    else:
                        self.hook(data)

        except websockets.ConnectionClosed:
            pass

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