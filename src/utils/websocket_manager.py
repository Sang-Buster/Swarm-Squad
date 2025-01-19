import atexit
import os
import subprocess
import threading
import time

import psutil


class WebSocketManager:
    _instance = None
    _websocket_process = None
    _is_running = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WebSocketManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):
            self.initialized = True
            atexit.register(self.cleanup_websocket)
            self._health_check_thread = None

    def is_websocket_running(self):
        """Check if a websocket server is already running on port 8051"""
        for proc in psutil.process_iter(["pid", "name", "cmdline"]):
            try:
                cmdline = proc.info["cmdline"]
                if cmdline and "websocket_server.py" in " ".join(cmdline):
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return False

    def _monitor_process_health(self):
        """Monitor WebSocket process health and restart if needed"""
        while self._is_running:
            if self._websocket_process and self._websocket_process.poll() is not None:
                print("WebSocket server died, restarting...")
                self.start_websocket()
            time.sleep(1)

    def start_websocket(self):
        """Start the WebSocket server only if one isn't already running"""
        if not self.is_websocket_running():
            self._is_running = True
            script_path = os.path.join(os.path.dirname(__file__), "websocket_server.py")
            self._websocket_process = subprocess.Popen(
                ["python", script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            time.sleep(2)  # Give the server time to start
            print("WebSocket server started")

            # Start health monitoring in a separate thread
            if (
                not self._health_check_thread
                or not self._health_check_thread.is_alive()
            ):
                self._health_check_thread = threading.Thread(
                    target=self._monitor_process_health, daemon=True
                )
                self._health_check_thread.start()
        else:
            print("WebSocket server already running")
            self._is_running = True

    def cleanup_websocket(self):
        """Cleanup the WebSocket server"""
        self._is_running = False
        if self._websocket_process:
            print("Shutting down WebSocket server...")
            self._websocket_process.terminate()
            try:
                self._websocket_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self._websocket_process.kill()
            self._websocket_process = None
            print("WebSocket server stopped")
