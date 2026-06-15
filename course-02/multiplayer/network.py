import asyncio
import json


class NetworkClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.reader = None
        self.writer = None

        self.player_id = None
        self.map_data = None
        self.state = None

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(
            self.host,
            self.port,
            limit=10 * 1024 * 1024,
        )
        message = await self.read_message()

        if message["type"] != "init":
            raise RuntimeError("Expected init message from server")

        self.player_id = message["player_id"]
        self.map_data = message["map"]

    async def read_message(self):
        line = await self.reader.readline()

        if not line:
            raise ConnectionError("Server disconnected")

        return json.loads(line.decode())

    async def listen(self):
        while True:
            message = await self.read_message()

            if message["type"] == "state":
                self.state = message

    async def send_input(self, input_state):
        if self.writer is None:
            return

        message = {
            "type": "input",
            **input_state,
        }

        self.writer.write(json.dumps(message).encode() + b"\n")
        await self.writer.drain()
