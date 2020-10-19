### Server
import asyncio
import websockets
import datetime
import random
import secrets
import collections
import logging
import threading
import json
from pexpect import *
    
# logger = logging.getLogger('websockets')
# logger.setLevel(logging.DEBUG)
# logger.addHandler(logging.StreamHandler())

class transterminal:

    def __init__(self, cmd):

        self.connections = []
        self.cmd = cmd
        self.p = None

    def go(self):
        print("starting child process")
        self.p = spawn(self.cmd)

        stdout_listener_thread = threading.Thread(target=self.stdout_listener)
        stdout_listener_thread.start()

        self.run_ws_in_loop(asyncio.get_event_loop(), websockets.serve(self.ws_connection_handler, "0.0.0.0", 5678))

    async def send_user_info(self):

        users = {
            "users": []
        }
        for connection in self.connections:
            users["users"].append({
                "name": connection["name"],
                "colour": connection["colour"]
            })

        for connection in self.connections:
            await connection["websocket"].send("userdata" + json.dumps(users))

    async def listen_to_stdout(self):
        while True:
            try:

                message = self.p.read_nonblocking(1024, 0.1) #"alice was here"
                for connection in self.connections:
                    await connection["websocket"].send(message.decode("utf-8"))

                print(f"api websocket produce notification : {message}")

            except TIMEOUT:
                #print("stdout read timed out")
                pass
            #await asyncio.sleep(0.1)
        print("stopped listening to stdout")

    def stdout_listener(self):
        print("Starting stdout listener")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.listen_to_stdout())
        loop.run_forever()

    # websocket stuff

    async def consumer_handler(self, websocket, connection_object):
        while True:
            async for message in websocket:       
                print("api websocket consume message : ", message)

                # check for user data
                if message[0:8] == "userdata":
                    user_data = json.loads(message[8:])
                    connection_object["name"] = user_data["name"]
                    connection_object["colour"] = user_data["colour"]
                    print(connection_object)
                    await self.send_user_info()

                else: self.p.write(message)

    async def producer_handler(self, websocket, connection_object):
        await websocket.wait_closed()
        print("connection closed")
        self.connections.remove(connection_object)
        await self.send_user_info()

    async def ws_connection_handler(self, websocket, path):

        print(f"connection opened with {websocket.local_address[0]}")
        connection_object = {
            "websocket": websocket,
            "name": "anonymous",
            "colour": "#ffffff"
        }
        self.connections.append(connection_object)

        producer_task = asyncio.ensure_future(self.producer_handler(websocket, connection_object))
        consumer_task = asyncio.ensure_future(self.consumer_handler(websocket, connection_object))
        done, pending = await asyncio.wait([consumer_task, producer_task],
            return_when=asyncio.ALL_COMPLETED,
        )
        for task in pending:
            task.cancel()

        print(f"connection with {websocket.local_address[0]} closed")

    def run_ws_in_loop(self, loop, server):
        print("ws start websockert server in new thread")
        loop.run_until_complete(server)
        loop.run_forever()