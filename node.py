import struct
from message import Message

class Node():
    def __init__(self, nodes, message_buffer, index, config):
        self.tx_power = 0.0
        self.position = (0.0, 0.0)

        self.nodes = nodes                      # Global nodes dictionary
        self.message_buffer = message_buffer    # Sending message buffer array
        self.index = index                      # Index of self in nodes dictionary
        self.config = config                    # Config dictionary

    # Data message is received
    def on_data_message(self, msg:bytes):
        pass

    # Control message is received
    def on_control_message(self, msg:bytes):
        s = struct.unpack('ddd', msg)
        self.tx_power = s[0]
        self.position = (s[1], s[2])

    # Send a message to this node
    def send(self, msg:Message):
        self.message_buffer.append(msg)