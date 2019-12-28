import signal
import struct
from tcp import TCPClient
from message import Message

running = True

def close_handler(signal, reserved):
    global running
    running = False

signal.signal(signal.SIGINT, close_handler)

#loopback = TCPClient('127.0.0.1', 8081)
#loopback.start()
control = TCPClient('127.0.0.1', 8082)
control.start()

cdat = struct.pack('ddd', 1.5, 0.0, 0.0)
cmsg = Message.create(cdat)
control.send(cmsg.packet())

while running:
    pass

#loopback.stop()
control.stop()