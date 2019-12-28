import struct
import math
from message import Message

class Node():
    def __init__(self, nodes, message_buffer, index, config):
        self.tx_power = 0.0
        self.position = (0.0, 0.0)

        self.nodes = nodes                      # Global nodes dictionary
        self.message_buffer = message_buffer    # Sending message buffer array
        self.index = index                      # Index of self in nodes dictionary
        self.config = config                    # Config dictionary

        self.precalcFSPL()

    # Data message is received
    def on_data_message(self, msg:bytes):
        pass

    # Control message is received
    def on_control_message(self, msg:bytes):
        s = struct.unpack('ddd', msg)
        self.tx_power = s[0]
        self.position = (s[1], s[2])
        self.precalcFSPL()

    # Send a message to this node
    def send(self, msg:Message):
        self.message_buffer.append(msg)

    # Calculate part of free space path loss
    def precalcFSPL(self):
        Dt = float(self.config.get('radio', 'directivity_transmitter', fallback='1.0'))
        Dr = float(self.config.get('radio', 'directivity_receiver', fallback='1.0'))
        wavelength = float(self.config.get('radio', 'wavelength', fallback='1000'))/1000
        self.FSPL = Dt*Dr*wavelength*wavelength/39.4784176
        print("[%s] FSPL=%f"%(self.index, self.FSPL))

    # Calculate Received signal strength
    def calcRSSI(self, distance):
        FSPL = self.FSPL/(distance*distance)
        rssi = FSPL*self.tx_power
        return 20*math.log10(rssi)

    # Calculate distance from node with specific RSSI
    def calc_dist(self, rssi):
        return math.sqrt((self.FSPL*self.tx_power)/math.pow(10, (rssi/20)))