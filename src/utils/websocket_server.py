import asyncio
import websockets
import json
import sqlite3
import pandas as pd
from datetime import datetime
from websockets.exceptions import ConnectionClosedError
from functools import lru_cache
from time import time


class DroneWebsocketServer:
    def __init__(self, host="localhost", port=8051):
        self.host = host
        self.port = port
        self.connected_clients = set()
        self.last_update = 0
        self.cache_ttl = 0.1  # 100ms cache TTL

    @lru_cache(maxsize=1)
    def get_drone_data(self, timestamp):
        """Cache drone data for short periods to reduce database load"""
        conn = sqlite3.connect("./src/data/swarm_squad.db")
        df = pd.read_sql_query("SELECT * from telemetry", conn)
        conn.close()

        return {
            "droneCoords": [[row["Location"]] for _, row in df.iterrows()],
            "droneNames": [[f"Drone {row['Agent Name']}"] for _, row in df.iterrows()],
            "dronePitch": [[row["Pitch"]] for _, row in df.iterrows()],
            "droneYaw": [[row["Yaw"]] for _, row in df.iterrows()],
            "droneRoll": [[row["Roll"]] for _, row in df.iterrows()],
            "timestamp": datetime.now().isoformat(),
        }

    async def broadcast_drone_data(self):
        while True:
            try:
                current_time = time()
                if current_time - self.last_update >= self.cache_ttl:
                    drone_data = self.get_drone_data(
                        int(current_time * 10)
                    )  # Round to 100ms
                    self.last_update = current_time

                    if self.connected_clients:
                        websockets_coros = [
                            client.send(json.dumps(drone_data))
                            for client in self.connected_clients
                        ]
                        await asyncio.gather(*websockets_coros, return_exceptions=True)

            except Exception as e:
                print(f"Error broadcasting data: {e}")

            await asyncio.sleep(0.1)  # 100ms update rate

    async def handle_client(self, websocket):
        print("New client connected")
        self.connected_clients.add(websocket)
        try:
            await websocket.wait_closed()
        except ConnectionClosedError:
            print("Client connection closed unexpectedly")
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            self.connected_clients.remove(websocket)
            print("Client disconnected")

    async def start_server(self):
        async with websockets.serve(
            self.handle_client,
            self.host,
            self.port,
            ping_interval=20,
            ping_timeout=20,
            compression=None,
        ):
            print(f"WebSocket server running at ws://{self.host}:{self.port}")
            await self.broadcast_drone_data()

    def run(self):
        try:
            asyncio.run(self.start_server())
        except KeyboardInterrupt:
            print("\nServer stopped by user")
        except Exception as e:
            print(f"Server error: {e}")


if __name__ == "__main__":
    server = DroneWebsocketServer()
    server.run()
