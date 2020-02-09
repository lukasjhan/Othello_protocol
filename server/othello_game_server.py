from server import *
from log import *
from board import *
from msg import *

import sys
import random
import queue
import threading

time_out_sec = 15

class othello_network_server(threading.Thread):
    def __init__(self, port_number=6068, queue=None):
        threading.Thread.__init__(self)
        self.port = port_number
        self.log = Log()
        self.server_socket = Server(self.port)
        self.board = Board()
        self.turn = 'b'
        self.queue = queue

        self.log.write('Server running, Port: %d open' % self.port)

    def run(self):

        self.server_socket.open()

        #black player
        self.black_player_socket, addr = self.server_socket.accept()
        self.black_player_addr = str(addr)
        self.log.write('Black(' + self.black_player_addr + ') connected')

        self.black_token = self.generate_random_token()
        self.log.write('Black token published: ' + self.black_token)
        self.server_socket.send(self.black_player_socket, gen_accept_msg('b', self.black_token, self.board.board_to_str()))

        #white player
        self.white_player_socket, addr = self.server_socket.accept()
        self.white_player_addr = str(addr)
        self.log.write('White(' + self.white_player_addr + ') connected')

        self.white_token = self.generate_random_token()
        self.log.write('White token published: ' + self.white_token)
        self.server_socket.send(self.white_player_socket, gen_accept_msg('w', self.white_token, self.board.board_to_str()))

        player_info = {
            'b': {
                'socket': self.black_player_socket,
                'addr': self.black_player_addr,
                'token': self.black_token,
                'name': 'Black'
            },
            'w': {
                'socket': self.white_player_socket,
                'addr': self.white_player_addr,
                'token': self.white_token,
                'name': 'White'
            }
        }
        
        self.log.write("======={ Game start }=======")
        error = False
        self.black_player_socket.settimeout(time_out_sec)
        self.white_player_socket.settimeout(time_out_sec)
        
        while self.board.is_end() == False:
            
            # is pass?? -> pass: switch turn
            # send turn
            # recv move
            # move..
            # update
            # switch turn

            available_list = self.board.get_valid_moves(self.turn)
            if len(available_list) == 0: # pass
                self.log.write(player_info[self.turn]['name'] + ' turn pass')
                self.switch_turn()
                continue
            
            self.log.write(player_info[self.turn]['name'] + ' available: ' + ' '.join(available_list))
            self.server_socket.send(player_info[self.turn]['socket'], gen_turn_msg(available_list))

            try:
                recv = self.server_socket.recv(player_info[self.turn]['socket'])
            except:
                self.log.write('ERROR ' + player_info[self.turn]['name'] + ' timeout')
                error = True
                break

            try:
                code, data = parse_msg(recv)
            except:
                self.log.write('ERROR ' + player_info[self.turn]['name'] + ' parse error ' + recv)
                error = True
                break

            if code != 'move':
                self.log.write('ERROR ' + player_info[self.turn]['name'] + ' invaild code ' + code + ' ' + str(data))
                error = True
                break
            
            if data['token'] != player_info[self.turn]['token']:
                self.log.write('ERROR ' + player_info[self.turn]['name'] + ' token not matched ' + code + ' ' + str(data))
                error = True
                break

            if data['move'] not in available_list:
                self.log.write('ERROR ' + player_info[self.turn]['name'] + ' invailed move ' + code + ' ' + str(data))
                error = True
                break

            self.log.write(player_info[self.turn]['name'] + " move: " + data['move'])
            self.board.make_move(self.board.convert_1A_to_ij(data['move']), self.turn)
            #move
            if self.queue:
                self.queue.put(self.board.convert_1A_to_ij(data['move']))
            self.log.write('board: ' + self.board.board_to_str())

            self.server_socket.send(self.black_player_socket, gen_update_msg(self.board.board_to_str(), data['move']))
            self.server_socket.send(self.white_player_socket, gen_update_msg(self.board.board_to_str(), data['move']))
            time.sleep(5)
            self.switch_turn()

        # game over.
        self.log.write('=== Game over ===')
        black_count, white_count = self.board.cell_count()

        if error:
            if self.turn == 'b':
                black_result = 'lose'
                white_result = 'win'
                self.log.write('Result: White win!')
            else: # 'w'
                black_result = 'win'
                white_result = 'lose'
                self.log.write('Result: Black win!')
        else:
            if black_count < white_count:
                black_result = 'win'
                white_result = 'lose'
                self.log.write('Result: Black win!')
            elif white_count < black_count:
                black_result = 'lose'
                white_result = 'win'
                self.log.write('Result: White win!')
            else: #tie
                black_result = 'tie'
                white_result = 'tie'
                self.log.write('Result: Tie!')
        
        score = str(black_count)+'b ' + str(white_count)+'w'
        self.server_socket.send(self.black_player_socket, gen_end_msg(black_result, score, self.board.board_to_str()))
        self.server_socket.send(self.white_player_socket, gen_end_msg(white_result, score, self.board.board_to_str()))
        self.log.write('Final score: ' + score)
        self.log.write('Final board: ' + self.board.board_to_str())
        self.log.write('=== Game end ===')

        self.server_socket.close()

    def generate_random_token(self):
        table = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        table_len = len(table)

        ret = ''
        for _ in range(20):
            rand = random.randrange(0, table_len)
            ret += table[rand]
        
        return ret

    def switch_turn(self):
        if self.turn == 'b':
            self.turn = 'w'
        else:
            self.turn = 'b'

def main():
    othello = othello_network_server(int(sys.argv[1]))
    othello.run()

if __name__ == '__main__':
    if len(sys.argv) != 2 or sys.argv[1].isdecimal() == False:
        print("usage: python othello_game_server.py [port number]")
        sys.exit(-1)
    main()