from socket import *

class Server:
    def __init__(self, port_number:int):
        #server start.
        self.port = port_number
        self.run = False

    def open(self):
        if self.run:
            return
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.bind(('', self.port))
        self.server_socket.listen(2)
        self.run = True

    def close(self):
        if not self.run:
            return
        self.server_socket.close()
        self.run = False
        
    def accept(self):
        if not self.run:
            return
        client_socket, client_addr = self.server_socket.accept()
        return client_socket, client_addr

    def send(self, client_socket, msg:str):
        if not self.run:
            return
        client_socket.send(msg.encode('utf-8'))

    def recv(self, client_socket):
        if not self.run:
            return
        recv_msg = client_socket.recv(1024)
        return recv_msg.decode('utf-8')






