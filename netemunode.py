import signal
import socket
import struct
from tcp import TCPServer, TCPClient, Timeout
from message import Message

import argparse
parser = argparse.ArgumentParser(description='NetEmu Client')
parser.add_argument('--server', '-s', dest='ip', default='127.0.0.1', help='the ip address of the NetEmu server')
parser.add_argument('--port', '-p', dest='port', default=8080, type=int, help='the port of the NetEmu server')
parser.add_argument('--local', '-l', dest='local', default=8081, type=int, help='local port to which the client uses as local connection')

# GLOBALS
running = True

# MESSAGE HANDLERS
# ----------------
def local_message(message:Message, server):
    server.send(message.packet())

def server_message(message:Message, local):
    local.send(message.packet())

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

    # Open local server
    with TCPServer(args.local) as local:
        lsock, _ = local.accept()
    print("Applicatio layer connected")

    # receive buffers
    lbuf = b''
    sbuf = b''

    # Receive messages
    lmsg = None
    smsg = None

    # Connect to server
    with TCPClient(args.ip, args.port) as server:
        while running:
            # Receive local data
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
                local_message(lmsg, server)
                lmsg = None

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
            elif not smsg.done:
                sbuf = smsg.finish(sbuf)
            if smsg!=None and smsg.done:
                server_message(smsg, lsock)
                smsg = None

    # Cleanup
    lsock.close()
    local.stop()
    server.stop()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, close_handler)
    main()