import socket
import json
import argparse

class Coordinator:
    def __init__(self, host='localhost', port=8081):
        self.host = host
        self.port = port
        self.nodes = []
        self.state = 'INIT'
        self.value = 0
    
    def recv_message(self, conn):
        data = b''
        while True:
            chunk = conn.recv(1024)
            if not chunk:
                break
            data += chunk
        return json.loads(data.decode())

    def send_message(self, host, port, type, value):
        serialized = json.dumps({
            'type': type,
            'value': value
        })
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            # print(f'sending {len(serialized)} bytes to {host}:{port}')
            s.sendall(serialized.encode())
            response = self.recv_message(s)
            s.close()
            return response

    def add_node(self, host, port):
        self.nodes.append((host, port))
        print(f'Added node {host}:{port}')

    def prepare(self):
        votes = []
        for node in self.nodes:
            vote = self._send_prepare(node)
            votes.append(vote)
        
        self.state = 'ENDING'
        
        if all(votes):
            return True
        else:
            return False

    def commit(self):
        for node in self.nodes:
            self._send_commit(node)
        self.state = 'PREPARING'

    def abort(self):
        for node in self.nodes:
            self._send_abort(node)
        self.state = 'PREPARING'

    def _send_prepare(self, node):
        resp = self.send_message(node[0], node[1], 'PREPARE', self.value)
        return resp['value'] == 'yes'

    def _send_commit(self, node):
        self.send_message(node[0], node[1], 'COMMIT', self.value)
        
    def _send_abort(self, node):
        self.send_message(node[0], node[1], 'ABORT', self.value)

if __name__ == '__main__':
    coordinator = Coordinator()
    while True:
        if coordinator.state == 'INIT':
            add_node = input('Add node (y/n): ')
            if add_node == 'y':
                host = input('Host: ')
                port = int(input('Port: '))
                coordinator.add_node(host, port)
            else:
                print('Initialization complete.')
                coordinator.state = 'PREPARING'
        else:
            coordinator.value = int(input('Value to Commit: '))
            print(f'Preparing value {coordinator.value}')
            success = coordinator.prepare()
            if success:
                print(f'Committing value {coordinator.value}')
                coordinator.commit()
            else:
                print('Aborting')
                coordinator.abort()