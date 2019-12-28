import signal
import struct
import random
from tcp import TCPClient
from message import Message

running = True

def close_handler(signal, reserved):
    global running
    running = False

signal.signal(signal.SIGINT, close_handler)

control = TCPClient('127.0.0.1', 8080)
control.start()

x = (random.random()-0.5)*10.0
y = (random.random()-0.5)*10.0

cdat = b'\x01' + struct.pack('<d<d<d', 1.5, x, y)
cmsg = Message.create(cdat)
control.send(cmsg.packet())

while running:
    pass

control.stop()