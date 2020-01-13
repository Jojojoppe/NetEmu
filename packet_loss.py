# Function which defines if packet is dropped
# SNR: distance between noise floor and RSSI in dBm
# Returns true if packet should be dropped
def packet_loss(self, SNR=0, func='none'):
    if(func=='none'):
        return False
        
    else:
        raise Exception('%s packet loss function not known')