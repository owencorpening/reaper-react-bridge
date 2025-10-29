#!/usr/bin/env python3
"""REAPER React Bridge - Python WebSocket Server"""

import asyncio
import json
import logging
from typing import Set, Dict
from datetime import datetime

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn

from reaper_api import ReaperAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="REAPER React Bridge")
reaper = ReaperAPI()

active_connections: Set[WebSocket] = set()
current_state: Dict[str, Dict[str, float]] = {}

@app.get("/")
async def root():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head><title>REAPER React Bridge</title></head>
    <body style="font-family: sans-serif; max-width: 800px; margin: 50px auto; background: #1a1a1a; color: #fff; padding: 20px;">
        <h1>REAPER React Bridge</h1>
        <p><strong>Status:</strong> <span style="color: #4ade80;">Running</span></p>
        <p><strong>WebSocket:</strong> <code>ws://localhost:8765/ws</code></p>
        <h2>Quick Start</h2>
        <ol>
            <li>Start React: <code>cd react-ui && npm start</code></li>
            <li>Add JSFX in REAPER</li>
            <li>Control from browser</li>
        </ol>
    </body>
    </html>
    """)

@app.get("/health")
async def health():
    return JSONResponse({
        "status": "ok",
        "connections": len(active_connections),
        "reaper": "connected" if reaper.is_connected() else "disconnected"
    })

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.add(websocket)
    logger.info(f"Client connected. Total: {len(active_connections)}")
    
    try:
        while True:
            data = await websocket.receive_json()
            
            if data.get("type") == "set_param":
                effect = data["effect"]
                param = data["param"]
                value = data["value"]
                
                success = reaper.set_parameter(effect, param, value)
                
                if success:
                    if effect not in current_state:
                        current_state[effect] = {}
                    current_state[effect][param] = value
                    
                    for conn in active_connections:
                        if conn != websocket:
                            await conn.send_json({
                                "type": "param_update",
                                "effect": effect,
                                "param": param,
                                "value": value,
                                "source": "ui"
                            })
                    
                    logger.info(f"Set {effect}.{param} = {value}")
            
            elif data.get("type") == "ping":
                await websocket.send_json({"type": "pong"})
    
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        logger.info(f"Client disconnected. Total: {len(active_connections)}")

if __name__ == "__main__":
    logger.info("Starting REAPER React Bridge on localhost:8765")
    uvicorn.run("bridge:app", host="127.0.0.1", port=8765, reload=True)
