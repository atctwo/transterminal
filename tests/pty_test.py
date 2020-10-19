import asyncio
import websockets
import datetime
import random
import secrets
import collections
import logging
import sys
from ptyprocess import *
    
# logger = logging.getLogger('websockets')
# logger.setLevel(logging.DEBUG)
# logger.addHandler(logging.StreamHandler())

print("[server] starting child process")
p = PtyProcessUnicode.spawn(['python', 'test3.py'])

while True:
    print(p.read(), end="")
    print("a")