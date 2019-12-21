class Message():
    # Create a message from data
    def __init__(self, data:bytes):
        self.length = len(data)
        self.data = data
    # Reconstruct data from received message
    def recreate(self, inp:bytes):
        pass
    # Create packet from message to be sent
    def packet(self):
        blen = self.length.to_bytes(4, byteorder="little")
        return blen+self.data
    # Stringify message
    def __repr__(self):
        print(self.length, self.data)