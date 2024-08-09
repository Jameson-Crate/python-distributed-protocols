import socket
import json
import argparse

class Client:
    """
    Client / Manager for the Paxos protocol. First the client will listen
    for all the nodes to register themselves. Then the user can start the 
    protocol.
    """
    def __init__(self, port):
        self.host = 'localhost'
        self.port = port
        self.nodes = []
        self.status = 'INIT' # INIT, WAITING, ONGOING, DONE
    
    def listen(self):
        """
        Listen for nodes to register themselves.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            while True:
                conn, addr = s.accept()
                with conn:
                    data = conn.recv(1024)
                    if not data:
                        break
                    message = json.loads(data.decode())

    def start(self):
        """
        Start the protocol.
        """
        pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=8000, help='Port to listen on')
    args = parser.parse_args()
    client = Client(args.port)
    listen = input("Listen for nodes to register? (y/n): ")
    if listen == 'y':
        client.listen()
    else:
        print("Starting the protocol...")
        client.start()