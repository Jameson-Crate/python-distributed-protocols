import socket
import json
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-n', '--hostname', type=str, default='localhost')
parser.add_argument('-p', '--port', type=int, default=8080)
parser.add_argument('-i', '--id', type=int, required=True)
parser.add_argument('-v', '--vector', action='store_true')
args = parser.parse_args()


class LamportNode:
    def __init__(self, id):
        self.clock = 0
        self.id = id
        self.messages = []

    def send_message(self, host, port, message):
        self.clock += 1
        json_message = {
            'id': int(self.id),
            'clock': self.clock,
            'message': message
        }
        self.messages.append(json_message)
        if host != 'None':
            serialized = json.dumps(json_message)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                print(f'sending {len(serialized)} bytes to {host}:{port}')
                s.sendall(serialized.encode())

    def start_listening(self, host, port):
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((host, port))
                print(f'Listening on {host}:{port}')
                s.listen()
                conn, addr = s.accept()
                with conn:
                    print(f"Connected by {addr}")
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        json_data = json.loads(data.decode())
                        self.messages.append(json_data)
                        if json_data['id'] == 0:
                            self.send_message(json_data['host'], json_data['port'], json_data['message'])
                        else:
                            if json_data['clock'] > self.clock:
                                self.clock = json_data['clock']
                            self.clock += 1
                print(f'Clock: {self.clock}')


class VectorNode:
    def __init__(self, id):
        self.id = id
        self.clocks = {id: 0}
        self.messages = []

    def send_message(self, host, port, message):
        self.clocks[self.id] += 1
        json_message = {
            'id': int(self.id),
            'clocks': self.clocks,
            'message': message
        }
        self.messages.append(json_message)
        if host != 'None':
            serialized = json.dumps(json_message)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                print(f'sending {len(serialized)} bytes to {host}:{port}')
                s.sendall(serialized.encode())

    def start_listening(self, host, port):
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((host, port))
                print(f'Listening on {host}:{port}')
                s.listen()
                conn, addr = s.accept()
                with conn:
                    print(f"Connected by {addr}")
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        json_data = json.loads(data.decode())
                        self.messages.append(json_data)
                        if json_data['id'] == 0:
                            self.send_message(json_data['host'], json_data['port'], json_data['message'])
                        else:
                            self.clocks[self.id] += 1
                            for i in json_data['clocks']:
                                value = json_data['clocks'][i]
                                i = int(i)
                                if i in self.clocks:
                                    self.clocks[i] = max(self.clocks[i], value)
                                else:
                                    self.clocks[i] = value
                print(f'Clocks: {self.clocks}')


if __name__ == "__main__":
    if args.vector:
        node = VectorNode(args.id)
    else:
        node = LamportNode(args.id)
    node.start_listening(args.hostname, args.port)
