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
import tempfile
from pathlib import Path

# Third-party imports
import psutil
import uvicorn
from fastapi import FastAPI
from teatype.io import prompt
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
    or the owning program exits. The pid is also persisted to a pid file (keyed
    by port) so a stale server from a previous, uncleanly-exited run can be
    detected and reclaimed on the next start().

    If the target port is already occupied on start(), the occupying process is
    either killed automatically (force_kill=True) or the user is prompted for
    confirmation.

    Usage
    -----
        server = SocketServer(port=12345, auto_start=False)

        async def echo(websocket):
            await websocket.accept()
            while True:
                data = await websocket.receive_text()
                await websocket.send_text(data)

        server.register_endpoint('/ws/echo', echo)
        server.start()
    """
    _pid_file:Path
    _process:multiprocessing.Process
    
    app:FastAPI
    force_kill:bool
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
                 force_kill:bool=False,
                 log_level:str='info',
                 ssl_certfile:str=None,
                 ssl_keyfile:str=None):
        self.app = FastAPI()
        self.force_kill = force_kill
        self.host = host
        self.log_level = log_level
        self.port = port
        self.ssl_certfile = ssl_certfile
        self.ssl_keyfile = ssl_keyfile
        
        self._pid_file = Path(tempfile.gettempdir()) / f'teatype_socketserver_{port}.pid'
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
        self._reclaim_port()
        self._process = multiprocessing.get_context('fork').Process(
            target=_serve,
            args=(self.app, self.host, self.port, self.ssl_certfile, self.ssl_keyfile, self.log_level),
            daemon=True)
        self._process.start()
        self._pid_file.write_text(str(self._process.pid))
        scheme = 'wss' if self.ssl_certfile else 'ws'
        log(f'[comms.ws.SocketServer] Listening on {scheme}://{self.host}:{self.port} (pid={self._process.pid})')
    
    def stop(self):
        if not self.running:
            return
        try:
            os.kill(self._process.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        self._process.join(timeout=5)
        if self._process.is_alive():
            self._process.terminate()
            self._process.join(timeout=5)
        self._process = None
        self._pid_file.unlink(missing_ok=True)
    
    def __del__(self):
        self.stop()

    #################
    # Port Conflict #
    #################

    def _reclaim_port(self):
        """
        Kills whatever process is already listening on self.port, either
        automatically (force_kill) or after prompting for confirmation.
        """
        owner_pid = self._port_owner_pid()
        if owner_pid is None:
            return
        
        if not self.force_kill:
            answer = prompt(f'[comms.ws.SocketServer] Port {self.port} is already in use by PID {owner_pid}. Kill it?')
            if not answer:
                err(f'[comms.ws.SocketServer] Port {self.port} is occupied by PID {owner_pid}',
                    raise_exception=RuntimeError)
        
        log(f'[comms.ws.SocketServer] Killing process occupying port {self.port} (pid={owner_pid})')
        try:
            os.kill(owner_pid, signal.SIGTERM)
            psutil.Process(owner_pid).wait(timeout=5)
        except psutil.NoSuchProcess:
            pass
        except psutil.TimeoutExpired:
            os.kill(owner_pid, signal.SIGKILL)

    def _port_owner_pid(self) -> int:
        """
        Returns the pid of whatever process is listening on self.port, or None.
        """
        for connection in psutil.net_connections(kind='inet'):
            if connection.status == psutil.CONN_LISTEN and \
               connection.laddr.port == self.port and \
               connection.pid and \
               connection.pid != os.getpid():
                return connection.pid
        return None

if __name__ == '__main__':
    from fastapi import WebSocket, WebSocketDisconnect

    async def echo(websocket:WebSocket):
        await websocket.accept()
        try:
            while True:
                data = await websocket.receive_text()
                print(f'[comms.ws.SocketServer] Received: {data}')
                await websocket.send_text(data)
        except WebSocketDisconnect:
            pass

    server = SocketServer(port=12345, auto_start=False)
    # server.register_endpoint('/ws/echo', echo)
    server.start()

    server._process.join()
