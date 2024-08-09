import socket
import argparse
import json

class Node:
    """
    A node in the Paxos protocol.
    """
    def __init__(self, port, client_port):
        self.host = 'localhost'
        self.port = port
        self.client_host = 'localhost'
        self.client_port = client_port
        self.nodes = []
    
    def register(self):
        """
        Register with the client
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.client_host, self.client_port))
            s.sendall(json.dumps({'host': self.host, 'port': self.port}).encode())
    
    def listen(self):
        """
        Listen for connections from other nodes or the client
        """
        pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--client', type=int, default=8000, help='Client port to register with')
    parser.add_argument('-p', '--port', type=int, default=8001, help='Port to listen on')
    args = parser.parse_args()
    node = Node(args.port, args.client)
    node.register()
    node.listen()