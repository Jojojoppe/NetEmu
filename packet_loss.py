# Function which defines if packet is dropped
# SNR: distance between noise floor and RSSI in dBm
# Returns true if packet should be dropped
def packet_loss(self, SNR=0):
    return False