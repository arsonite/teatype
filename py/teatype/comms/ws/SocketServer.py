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
import atexit
import multiprocessing
import os
import signal

# Third-party imports
import uvicorn
from fastapi import FastAPI

# Local imports
from teatype.logging import *

def _serve(app:FastAPI, host:str, port:int, ssl_certfile:str, ssl_keyfile:str, log_level:str):
    uvicorn.run(app,
                host=host,
                port=port,
                ssl_certfile=ssl_certfile,
                ssl_keyfile=ssl_keyfile,
                log_level=log_level)

class SocketServer:
    """
    FastAPI websocket server that runs in a background process (wss:// supported
    via ssl_certfile/ssl_keyfile). Register endpoints with register_endpoint(path,
    handler) before start(); handler is:
        async def handler(websocket: fastapi.WebSocket) -> None

    The server starts automatically on construction (auto_start=True) and is
    torn down, via the child process' pid, when this object is garbage-collected
    or the owning program exits.

    Usage
    -----
        server = SocketServer(port=8765, auto_start=False)

        async def echo(websocket):
            await websocket.accept()
            while True:
                data = await websocket.receive_text()
                await websocket.send_text(data)

        server.register_endpoint('/ws/echo', echo)
        server.start()
    """
    _process:multiprocessing.Process
    
    app:FastAPI
    host:str
    log_level:str
    port:int
    ssl_certfile:str
    ssl_keyfile:str
    
    def __init__(self,
                 host:str='0.0.0.0',
                 port:int=12345,
                 *,
                 auto_start:bool=True,
                 log_level:str='info',
                 ssl_certfile:str=None,
                 ssl_keyfile:str=None):
        self.app = FastAPI()
        self.host = host
        self.log_level = log_level
        self.port = port
        self.ssl_certfile = ssl_certfile
        self.ssl_keyfile = ssl_keyfile
        
        self._process = None
        
        # Guarantees shutdown even if __del__ never runs (e.g. interpreter exit)
        atexit.register(self.stop)
        
        if auto_start:
            self.start()
            
    ##############
    # Properties #
    ##############
    
    @property
    def pid(self) -> int:
        return self._process.pid if self.running else None
    
    @property
    def running(self) -> bool:
        return self._process is not None and self._process.is_alive()
    
    ##############
    # Public API #
    ##############
    
    def register_endpoint(self, path:str, handler:callable):
        """
        Registers an async handler(websocket) for a websocket path. Must be called before start().
        """
        if self.running:
            err('[comms.ws.SocketServer] Cannot register endpoints after the server has started',
                raise_exception=RuntimeError)
        self.app.add_api_websocket_route(path, handler)
    
    def start(self):
        if self.running:
            return
        self._process = multiprocessing.get_context('fork').Process(
            target=_serve,
            args=(self.app, self.host, self.port, self.ssl_certfile, self.ssl_keyfile, self.log_level),
            daemon=True)
        self._process.start()
        scheme = 'wss' if self.ssl_certfile else 'ws'
        log(f'[comms.ws.SocketServer] Listening on {scheme}://{self.host}:{self.port} (pid={self._process.pid})')
    
    def stop(self):
        if not self.running:
            return
        os.kill(self._process.pid, signal.SIGTERM)
        self._process.join(timeout=5)
        if self._process.is_alive():
            self._process.terminate()
            self._process.join(timeout=5)
        self._process = None
    
    def __del__(self):
        self.stop()

if __name__ == '__main__':
    from fastapi import WebSocket, WebSocketDisconnect

    async def echo(websocket:WebSocket):
        await websocket.accept()
        try:
            while True:
                data = await websocket.receive_text()
                await websocket.send_text(data)
        except WebSocketDisconnect:
            pass

    server = SocketServer(port=8765, auto_start=False)
    server.register_endpoint('/ws/echo', echo)
    server.start()

    server._process.join()
