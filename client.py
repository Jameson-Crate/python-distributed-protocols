import socket
import json


def send_message(host, port, host_2, port_2, message):
    serialized = json.dumps({
        'id': 0,
        'host': host_2,
        'port': port_2,
        'message': message
    })
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print(f'sending {len(serialized)} bytes to {host}:{port}')
        s.sendall(serialized.encode())


if __name__ == '__main__':
    while True:
        host = input('Host 1: ')
        port = int(input('Port 1: '))
        host_2 = input('Host 2: ')
        port_2 = int(input('Port 2: '))
        message = input('Message: ')
        send_message(host, port, host_2, port_2, message)
