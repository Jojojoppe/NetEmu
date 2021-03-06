import sys
import socket
import threading
import signal
import configparser

from tcp import TCPServer
from message import Message
from node import Node
from server_gui import GuiThread

import argparse
parser = argparse.ArgumentParser(description='NetEmu Server')
parser.add_argument('config_file', default='config.ini', type=str, help='Config file')

# GLOBALS
running = True
nodes = {}
config = {}

class ThreadConnection(threading.Thread):
    def __init__(self, socket, address, port):
        global nodes, config
        threading.Thread.__init__(self, name='%s%d'%(address,port))
        self.socket = socket
        self.address = address
        self.port = port
        self.running = False
        self.node_idx = '%s%d'%(address, port)
        self.message_buffer = []
        nodes[self.node_idx] = Node(nodes, self.message_buffer, self.node_idx, config)

    def __del__(self):
        self.socket.close()

    def run(self):
        global nodes, config
        self.running = True
        if config.get('logging', 'connection_status', fallback='false')=='true':
            print("> Connection opened from %s:%d"%(self.address,self.port))
        buf = b''
        msg = None
        while self.running:

            # Send data if possible
            for m in nodes[self.node_idx].message_buffer:
                print("Send [%s]: %s"%(self.node_idx, m))
                self.socket.send(m)
            nodes[self.node_idx].message_buffer = []

            # Receive data
            dat = self.recv_timeout(4096, 0.1)
            if dat!=None and dat!=b'':
                buf += dat
            elif dat==b'':
                # Node disconnected
                self.running = False
                nodes.pop(self.node_idx)
                if config.get('logging', 'connection_status', fallback='false')=='true':
                    print("> Connection closed %s:%d"%(self.address,self.port))
            # Create message object
            if msg==None:
                msg, buf = Message.recreate(buf)
            elif not msg.done:
                buf = msg.finish(buf)
            if msg!=None and msg.done:
                # Message received
                # ----------------
                if config.get('logging', 'raw_message', fallback='false')=='true':
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
    global running, config
    args = parser.parse_args()

    print('NetEmu Server')
    print('Ctr-C to close')

    # Get configuration
    config = configparser.ConfigParser()
    config.read(args.config_file)
    port = config.get('connection', 'port', fallback='8080')
    maxcon = config.get('connection', 'maxcon', fallback='10')
    ip = config.get('connection', 'ip', fallback="localhost")

    # List of all connections (active and non-active)
    connections = []

    with TCPServer(int(port), int(maxcon), ip=ip) as server:

        gui_thread = GuiThread(nodes, config)
        gui_thread.start()

        while running:
            # Wait for connection and create listening thread
            try:
                csock, con_info = server.accept(1.0)
                cthread = ThreadConnection(csock, *con_info)
                cthread.start()
                connections.append(cthread)
            except socket.timeout:
                continue

        gui_thread.stop()
        # Clean up all connections
        for conn in connections:
            if conn.running:
                conn.stop()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, close_handler)
    main()