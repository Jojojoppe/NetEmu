class Message():
    def __init__(self):
        self.data = b''
        self.length = 0
    # Create message object from string of bytes
    @classmethod
    def create(cls, data:bytes):
        msg = cls()
        msg.data = data
        msg.length = len(data)
        return msg
    # Reconstruct data from received message. Returns Message object and rest of data
    @classmethod
    def recreate(cls, inp:bytes):
        msg = cls()
        blen = int.from_bytes(inp[0:3], byteorder="little")
        if blen>(len(inp)-4):
            raise IndexError
        msg.length = blen
        msg.data = inp[4:4+blen]
        return msg,inp[4+blen:]
    # Create packet from message to be sent
    def packet(self):
        blen = self.length.to_bytes(4, byteorder="little")
        return blen+self.data
    # Stringify message
    def __repr__(self):
        return '%d: %s' % (self.length, str(self.data))