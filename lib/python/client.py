from socket import *
from msg import *

class Client:
    def __init__(self, ip:str, port_number:int):
        #server start.
        self.ip = ip
        self.port = port_number
        self.run = False

    def connect(self):
        if self.run:
            return
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect((self.ip, self.port))

    def close(self):
        if not self.run:
            return
        self.client_socket.close()

    def send(self, msg:str):
        self.client_socket.send(msg.encode('utf-8'))

    def recv(self):
        recv_msg = self.client_socket.recv(1024)
        return recv_msg.decode('utf-8')
