import sys, os, asyncio
import websockets
from ptyprocess import *
import logging

logger = logging.getLogger('websockets')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

print("[server] starting child process")
p = PtyProcessUnicode.spawn(['python', 'test4.py'])


# producer
async def get_child_stdout():
    stdout_line = p.readline()
    return stdout_line

async def handle_child_stdout(websocket, path):
    print("starting stdout function")
    while True:
        # send stdout
        stdout_line = await get_child_stdout()
        await websocket.send(stdout_line)
    print("ending stdout function")

# consumer
async def handle_consumer(data):
    print(data)

async def handle_child_stdin(websocket, path):
    print("starting stdin function")
    async for msg in websocket:
        print("aaa")
        #await handle_consumer(msg)
    print("ending stdin function")


async def time(websocket, path):
   
    print("new connection")

    consumer_task = asyncio.ensure_future(handle_child_stdin(websocket, path))
    producer_task = asyncio.ensure_future(handle_child_stdout(websocket, path))
    done, pending = await asyncio.wait(
        [producer_task, consumer_task],
        return_when=asyncio.ALL_COMPLETED
    )

    for task in pending: task.cancel();

    print("connection closed")
        

logger.info("test")

print("[server] starting websocket server")
start_server = websockets.serve(time, "localhost", 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()


##p.write("print('hello world')\n")

print("[server] starting main stdout loop")
try:
    while(True):

        print("> " + p.readline(), end="")

except EOFError:
    print("The process ended")