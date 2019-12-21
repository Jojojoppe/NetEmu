import sys
import socket
import threading
import signal

from tcp import TCPServer
from message import Message
from node import Node
from server_gui import GuiThread

import argparse
parser = argparse.ArgumentParser(description='NetEmu Server')
parser.add_argument('--port', '-p', dest='port', default=8080, type=int, help='the port of the NetEmu server')
parser.add_argument('--maxcon', '-n', dest='maxcon', default=10, type=int, help='maximum amount of connections on the NetEmu server')

# GLOBALS
running = True
nodes = {}

class ThreadConnection(threading.Thread):
    def __init__(self, socket, address, port):
        global nodes
        threading.Thread.__init__(self, name='%s%d'%(address,port))
        self.socket = socket
        self.address = address
        self.port = port
        self.running = False
        self.node_idx = '%s%d'%(address, port)
        self.message_buffer = []
        nodes[self.node_idx] = Node(nodes, self.message_buffer, self.node_idx)

    def __del__(self):
        self.socket.close()

    def run(self):
        global nodes
        self.running = True
        print("> Connection opened from %s:%d"%(self.address,self.port))
        buf = b''
        msg = None
        while self.running:

            # Send data if possible
            for m in self.message_buffer:
                self.socket.send(m.packet())
            self.message_buffer = []

            # Receive data
            dat = self.recv_timeout(4096, 0.1)
            if dat!=None and dat!=b'':
                buf += dat
            elif dat==b'':
                # Node disconnected
                self.running = False
                nodes.pop(self.node_idx)
                print("> Connection closed %s:%d"%(self.address,self.port))
            # Create message object
            if msg==None:
                msg, buf = Message.recreate(buf)
            elif not msg.done:
                buf = msg.finish(buf)
            if msg!=None and msg.done:
                # Message received
                # TODO DO SOMETHING WITH DATA
                # ----------------
                print('%s:%d > %s'%(self.address, self.port, str(msg.data)))
                if msg.data[0]==0:
                    # DATA
                    nodes[self.node_idx].on_data_message(msg.data[1:])
                elif msg.data[0]==1:
                    # CONTROL
                    nodes[self.node_idx].on_control_message(msg.data[1:])
                else:
                    # UNKNOWN
                    pass
                # ----------------
                msg = None

    def stop(self):
        self.running = False

    def recv_timeout(self, bufsize, timeout):
        self.socket.settimeout(timeout)
        try:
            dat = self.socket.recv(bufsize)
        except socket.timeout:
            dat = None
        return dat

def close_handler(signal, reserved):
    global running
    print("\rClosing server...")
    running = False

def main():
    global running
    args = parser.parse_args()

    print('NetEmu Server')

    # List of all connections (active and non-active)
    connections = []

    with TCPServer(args.port, args.maxcon) as server:

        #gui_thread = GuiThread(nodes)
        #gui_thread.start()

        while running:
            # Wait for connection and create listening thread
            try:
                csock, con_info = server.accept(1.0)
                cthread = ThreadConnection(csock, *con_info)
                cthread.start()
                connections.append(cthread)
            except socket.timeout:
                continue

        #gui_thread.stop()
        # Clean up all connections
        for conn in connections:
            if conn.running:
                conn.stop()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, close_handler)
    main()