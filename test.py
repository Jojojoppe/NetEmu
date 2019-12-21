from tcp import TCPClient
from message import Message

with TCPClient('localhost', 8081) as server:
    msg = Message.create(bytes('Hello, this is a test','utf-8'))
    server.send(msg.packet())
    server.stop()