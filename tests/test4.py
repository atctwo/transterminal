
import asyncio
import datetime
import random
import websockets
import time

while True:

    now = datetime.datetime.utcnow().isoformat() + "Z"
    print("the time is " + now)
    #time.sleep(1)