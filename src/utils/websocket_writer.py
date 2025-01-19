from datetime import datetime
from queue import Queue
from typing import Any, Dict

from .websocket_manager import WebSocketManager


class WebSocketWriter:
    def __init__(self, host="localhost", port=8051):
        self.host = host
        self.port = port
        self._message_queue = Queue()
        # Initialize the WebSocket manager
        self.ws_manager = WebSocketManager()
        self.ws_manager.start_websocket()  # Start the WebSocket server

    def ws_writer(self, data: Dict[str, Any]):
        """Write data to the WebSocket server through the database"""
        # Format data for WebSocket clients
        ws_data = {
            "droneCoords": [[loc] for loc in data["Location"]],
            "droneNames": [[f"Drone {name}"] for name in data["Agent Name"]],
            "dronePitch": [[pitch] for pitch in data["Pitch"]],
            "droneYaw": [[yaw] for yaw in data["Yaw"]],
            "droneRoll": [[roll] for roll in data["Roll"]],
            "timestamp": datetime.now().isoformat(),
        }
        self._message_queue.put(ws_data)


# Global WebSocket writer instance
_ws_writer = None


def get_ws_writer() -> WebSocketWriter:
    """Get or create the global WebSocket writer instance"""
    global _ws_writer
    if _ws_writer is None:
        _ws_writer = WebSocketWriter()
    return _ws_writer


def ws_writer(data: Dict[str, Any]):
    """Synchronous wrapper for writing data to WebSocket clients"""
    writer = get_ws_writer()
    writer.ws_writer(data)
