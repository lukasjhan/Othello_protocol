import sys

from client import *
from msg import *
from log import *

class Othello:
    def __init__(self, ip, port):
        self.client_socket = Client(ip, port)
        self.log = Log()

        self.client_socket.connect()
        self.log.write('Server Connection Success!')

        accept_msg = self.client_socket.recv()
        try:
            code, data = parse_msg(accept_msg)
        except:
            self.log.write('ERROR: parse error ' + accept_msg)
            sys.exit(-1)

        if code != 'accept':
            self.log.write('ERROR: accept msg error: ' + code + ' ' + str(data))
            sys.exit(-1)
        
        self.color = data['color']
        self.token = data['token']
        self.board = data['board']
        
        self.log.write('Color: {color}, Token: {token}, Board: {board}'.format(color=self.color, token=self.token, board=self.board))
    
    def wait_for_turn(self):
        while True:
            msg = self.client_socket.recv()
            try:
                code, data = parse_msg(msg)
            except:
                self.log.write('ERROR: parse error ' + msg)
                sys.exit(-1)

            if code == 'turn':
                self.log.write("turn: " + data['available'])
                return code, data
            elif code == 'update':
                self.board = data['board']
                self.log.write("update: " + data['board'])
            elif code == 'end':
                self.log.write("game end: " + data['status'] + " " + data['score'])
                self.log.write('final board: ' + data['board'])
                return code, data
            else:
                self.log.write('ERROR: invaild code error: ' + code + ' ' + str(data))
                sys.exit(-1)

    def move(self, cell_corr):
        msg = gen_move_msg(cell_corr, self.token)
        self.client_socket.send(msg)

def str_to_board(board_str):
    l = 0
    board = [['0' for x in range(8)] for y in range(8)]

    for i in range(8):
        for j in range(8):
            board[i][j] = board_str[l]
            l += 1
    return board

def print_board(board):
    print("  ABCDEFGH")
    i = 1
    for row in board:
        ret = ''
        for col in row:
            ret += col
        print(str(i) + ' ' + ret)
        i += 1

def main():
    othello = Othello(sys.argv[1], int(sys.argv[2]))
    while True:
        code, data = othello.wait_for_turn()
        if code == 'end':
            print_board(str_to_board(data['board']))
            print("status: " + data['status'] + ' score: ' + data['score'])
            break
        elif code == 'turn':
            print_board(str_to_board(othello.board))
            print('available: ' + data['available'])
            input_corr = input('>>>')
            othello.move(input_corr)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("usage: python othello.py [ip address] [port number]")
        sys.exit(-1)
    main()