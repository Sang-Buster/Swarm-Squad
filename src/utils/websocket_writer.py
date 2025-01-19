import asyncio
import json
import threading
from datetime import datetime
from queue import Queue
from typing import Any, Dict

import websockets


class WebSocketWriter:
    def __init__(self, host="localhost", port=8051):
        self.host = host
        self.port = port
        self.connected_clients = set()
        self._server = None
        self._running = False
        self._message_queue = Queue()
        self._thread = None
        self._loop = None

    def start(self):
        """Start the WebSocket server in a separate thread"""
        if self._running:
            return

        self._running = True
        self._thread = threading.Thread(target=self._run_server, daemon=True)
        self._thread.start()

    def _run_server(self):
        """Run the WebSocket server in a new event loop"""
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)

        async def serve():
            self._server = await websockets.serve(
                self._handle_client,
                self.host,
                self.port,
                ping_interval=20,
                ping_timeout=20,
                compression=None,
            )
            print(f"WebSocket server running at ws://{self.host}:{self.port}")

            # Process messages from the queue
            while self._running:
                while not self._message_queue.empty():
                    data = self._message_queue.get()
                    await self._broadcast(data)
                await asyncio.sleep(0.01)

        self._loop.run_until_complete(serve())
        self._loop.run_forever()

    async def _handle_client(self, websocket):
        """Handle new client connections"""
        print("New client connected")
        self.connected_clients.add(websocket)
        try:
            await websocket.wait_closed()
        except websockets.exceptions.ConnectionClosedError:
            print("Client connection closed unexpectedly")
        finally:
            self.connected_clients.remove(websocket)
            print("Client disconnected")

    async def _broadcast(self, data: Dict[str, Any]):
        """Broadcast data to all connected clients"""
        if not self.connected_clients:
            return

        # Format data for WebSocket clients
        ws_data = {
            "droneCoords": [[loc] for loc in data["Location"]],
            "droneNames": [[f"Drone {name}"] for name in data["Agent Name"]],
            "dronePitch": [[pitch] for pitch in data["Pitch"]],
            "droneYaw": [[yaw] for yaw in data["Yaw"]],
            "droneRoll": [[roll] for roll in data["Roll"]],
            "timestamp": datetime.now().isoformat(),
        }

        message = json.dumps(ws_data)
        websockets_coros = [client.send(message) for client in self.connected_clients]
        await asyncio.gather(*websockets_coros, return_exceptions=True)

    def stop(self):
        """Stop the WebSocket server"""
        self._running = False
        if self._loop:
            self._loop.call_soon_threadsafe(self._loop.stop)
        if self._thread:
            self._thread.join()


# Global WebSocket writer instance
_ws_writer = None


def get_ws_writer() -> WebSocketWriter:
    """Get or create the global WebSocket writer instance"""
    global _ws_writer
    if _ws_writer is None:
        _ws_writer = WebSocketWriter()
        _ws_writer.start()
    return _ws_writer


def ws_writer(data: Dict[str, Any]):
    """Synchronous wrapper for writing data to WebSocket clients"""
    writer = get_ws_writer()
    writer._message_queue.put(data)
