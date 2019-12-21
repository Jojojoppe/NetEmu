import signal
import socket
import struct
from tcp import TCPServer, TCPClient, Timeout
from message import Message

import argparse
parser = argparse.ArgumentParser(description='NetEmu Client')
parser.add_argument('--server', '-s', dest='ip', default='127.0.0.1', help='the ip address of the NetEmu server')
parser.add_argument('--port', '-p', dest='port', default=8080, type=int, help='the port of the NetEmu server')
parser.add_argument('--loopback', '-l', dest='loopback', default=8081, type=int, help='local port to which the client uses as loopback')
parser.add_argument('--control', '-c', dest='control', default=8082, type=int, help='local port to which the client uses as control channel')

# GLOBALS
running = True

# NODE PARAMETERS
# ---------------
node_tx_power = 0.0
node_pos = (0.0,0.0)
# ---------------

# MESSAGE HANDLERS
# ----------------
def loopback_message(message:Message, server):
    dat = b'\x00' + message.data
    msg = Message.create(dat)
    server.send(msg.packet())

def control_message(message:Message, server):
    global node_tx_power, node_pos
    s = struct.unpack('ddd', message.data)
    node_tx_power = s[0]
    node_pos = (s[1],s[2])

    # Send to-server-message type message
    dat = b'\x01' + message.data
    msg = Message.create(dat)
    server.send(msg.packet())

def server_message(message:Message, loopback):
    loopback.send(message.packet())

# ----------------

def recv_timeout(socket, bufsize, timeout):
    socket.settimeout(timeout)
    try:
        dat = socket.recv(bufsize)
    except Timeout:
        dat = None
    return dat

def close_handler(signal, reserved):
    global running
    print("\rClosing client...")
    running = False

def main():
    global running
    args = parser.parse_args()

    print('NetEmu Client')

    # Open loopback server
    with TCPServer(args.loopback) as loopback:
        lsock, _ = loopback.accept()
    # Open control server
    with TCPServer(args.control) as control:
        csock, _ = control.accept()
    print("Applicatio layer connected")

    # receive buffers
    lbuf = b''
    cbuf = b''
    sbuf = b''

    # Receive messages
    lmsg = None
    cmsg = None
    smsg = None

    # Connect to server
    with TCPClient(args.ip, args.port) as server:
        while running:
            # Receive loopback data
            dat = recv_timeout(lsock, 4096, 0.1)
            if dat!=None and dat!=b'':
                lbuf += dat
            elif dat==b'':
                # Application disconnected
                running = False
                print("Application layer disconnected")
            # Create message object
            if lmsg==None:
                lmsg, lbuf = Message.recreate(lbuf)
            elif not lmsg.done:
                lbuf = lmsg.finish(lbuf)
            if lmsg!=None and lmsg.done:
                loopback_message(lmsg, server)
                lmsg = None

            # Receive control data
            dat = recv_timeout(csock, 4096, 0.1)
            if dat!=None and dat!=b'':
                cbuf += dat
            elif dat==b'':
                running = False
                print("Application layer disconnected")
            # Create message object
            if cmsg==None:
                cmsg, cbuf = Message.recreate(cbuf)
            elif not cmsg.done:
                cbuf = cmsg.finish(lbuf)
            if cmsg!=None and cmsg.done:
                control_message(cmsg, server)
                cmsg = None
            
            # Receive data from server
            dat = server.recv_timeout(4096, 0.1)
            if dat!=None and dat!=b'':
                sbuf += dat
            elif dat==b'':
                running = False
                print("Server disconnected")
            # Create message object
            if smsg==None:
                smsg, sbuf = Message.recreate(sbuf)
            elif not cmsg.done:
                sbuf = smsg.finish(sbuf)
            if smsg!=None and smsg.done:
                server_message(smsg, lsock)
                smsg = None

    # Cleanup
    lsock.close()
    csock.close()
    loopback.stop()
    control.stop()
    server.stop()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, close_handler)
    main()