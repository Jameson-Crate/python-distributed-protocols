import socket
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--hostname', type=str, default='localhost')
parser.add_argument('-p', '--port', type=int, default=5001)

class Node:
    def __init__(self, host='localhost', port=5001, coordinator_host='localhost', coordinator_port=5000):
        self.host = host
        self.port = port
        self.coordinator_host = coordinator_host
        self.coordinator_port = coordinator_port
        self.state = 'PREPARING'
        self.value = None
        self.values = []

    def send_message(self, conn, type, value):
        serialized = json.dumps({
            'type': type,
            'value': value
        })
        # print(f'sending {len(serialized)} bytes to {self.coordinator_host}:{self.coordinator_port}')
        conn.sendall(serialized.encode())

    def vote(self, conn):
        print('Voting')
        self.send_message(conn, 'VOTE', 'yes')
        
    def ack(self, conn):
        print('Acknowledging')
        print(self.values)
        self.send_message(conn, 'ACK', 'yes')
    
    def listen(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            print(f"Node listening on {self.host}:{self.port}")
            while True:
                conn, addr = s.accept()
                with conn:
                    # print(f"Connected by {addr}")
                    data = conn.recv(1024)
                    if not data:
                        break
                    message = json.loads(data.decode())
                    if message['type'] == 'PREPARE':
                        self.value = message['value']
                        self.state = 'PREPARED'
                        self.vote(conn)
                    else:
                        if message['type'] == 'COMMIT':
                            self.values.append(self.value)
                        self.state = 'READY'
                        self.ack(conn)

if __name__ == '__main__':
    args = parser.parse_args()
    node = Node(args.hostname, args.port)
    node.listen()