import subprocess
import atexit
import psutil
import threading
import time


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
            self.cleanup_old_websockets()
            atexit.register(self.cleanup_websocket)
            self._health_check_thread = None

    def cleanup_old_websockets(self):
        """Clean up any existing websocket processes on port 8051"""
        for proc in psutil.process_iter(["pid", "name", "cmdline"]):
            try:
                cmdline = proc.info["cmdline"]
                if cmdline and "websocket_server.py" in " ".join(cmdline):
                    proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

    def _monitor_process_health(self):
        """Monitor WebSocket process health and restart if needed"""
        while self._is_running:
            if self._websocket_process and self._websocket_process.poll() is not None:
                print("WebSocket server died, restarting...")
                self.start_websocket()
            time.sleep(1)

    def start_websocket(self):
        """Start the WebSocket server"""
        if not self._is_running:
            self._is_running = True
            self._websocket_process = subprocess.Popen(
                ["python", "src/utils/websocket_server.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            print("WebSocket server started")

            # Start health monitoring in a separate thread
            self._health_check_thread = threading.Thread(
                target=self._monitor_process_health, daemon=True
            )
            self._health_check_thread.start()

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
