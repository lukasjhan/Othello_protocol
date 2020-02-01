import random

class Board:
    def __init__(self):
        self.BLACK_CELL = 'b'
        self.WHITE_CELL = 'w'
        self.EMPTY_CELL = '0'

        self.BOARD_LEN = 8
        self.dx = [-1, -1, -1, 0, 0, 1, 1, 1]
        self.dy = [-1, 0, 1, -1, 1, -1, 0, 1]

        self.init_board()

    def init_board(self):
        self.board = [[self.EMPTY_CELL for x in range(self.BOARD_LEN)] for y in range(self.BOARD_LEN)]
    
        self.board[3][3] = self.WHITE_CELL
        self.board[4][4] = self.WHITE_CELL
        self.board[3][4] = self.BLACK_CELL
        self.board[4][3] = self.BLACK_CELL

    def get_board_grid(self):
        return self.board

    def cell_count(self):
        white = 0
        black = 0

        for i in range(self.BOARD_LEN):
            for j in range(self.BOARD_LEN):
                if self.board[i][j] == self.WHITE_CELL:
                    white += 1
                elif self.board[i][j] == self.BLACK_CELL:
                    black += 1

        return black, white

    def convert_ij_to_1A(self, i, j):
        str_i = str(i+1)

        change = {
            0:'A',
            1:'B',
            2:'C',
            3:'D',
            4:'E',
            5:'F',
            6:'G',
            7:'H'
        }

        str_j = change[j]
        return str_i + str_j

    def convert_1A_to_ij(self, corr_str):
        int_i = int(corr_str[0]) - 1

        change = {
            'A':0,
            'B':1,
            'C':2,
            'D':3,
            'E':4,
            'F':5,
            'G':6,
            'H':7
        }

        int_j = change[corr_str[1]]
        return int_i, int_j

    def get_valid_moves(self, turn):
        valid_moves = []
        if turn == self.BLACK_CELL:
            opp = self.WHITE_CELL
        else:
            opp = self.BLACK_CELL
            

        for i in range(self.BOARD_LEN):
            for j in range(self.BOARD_LEN):
                if self.board[i][j] != self.EMPTY_CELL:
                    continue
                for k in range(self.BOARD_LEN):
                    count_my_cells = 0
                    count_other_cells = 0
                    cur_X = i + self.dx[k]
                    cur_Y = j + self.dy[k]
                    while self.BOARD_LEN > cur_X >= 0 and self.BOARD_LEN > cur_Y >= 0 :
                        if self.board[cur_X][cur_Y] == opp:
                            count_other_cells += 1
                            cur_X += self.dx[k]
                            cur_Y += self.dy[k]
                        elif self.board[cur_X][cur_Y] == turn:
                            count_my_cells += 1
                            break
                        else:
                            break
                    if count_my_cells > 0 and count_other_cells > 0:
                        valid_moves.append(self.convert_ij_to_1A(i,j))
                        break
        return valid_moves

    def is_end(self):
        count_white, count_black = self.cell_count()

        if count_white == 0 or count_black == 0:
            return True
        if count_white + count_black == self.BOARD_LEN * self.BOARD_LEN:
            return True
        if self.get_valid_moves(self.WHITE_CELL) == [] and self.get_valid_moves(self.BLACK_CELL) == []:
            return True

        return False

    def make_move(self, move_pos, turn):
        
        if turn == self.BLACK_CELL:
            opp = self.WHITE_CELL
        else:
            opp = self.BLACK_CELL

        i = move_pos[0]
        j = move_pos[1]
        for k in range(self.BOARD_LEN):
            count_my_cells = 0
            count_other_cells = 0
            cur_X = i + self.dx[k]
            cur_Y = j + self.dy[k]
            while self.BOARD_LEN > cur_X >= 0 and self.BOARD_LEN > cur_Y >= 0 :
                if self.board[cur_X][cur_Y] == opp:
                    count_other_cells += 1
                    cur_X += self.dx[k]
                    cur_Y += self.dy[k]
                elif self.board[cur_X][cur_Y] == turn:
                    count_my_cells += 1
                    break
                else:
                    break
            if count_my_cells > 0 and count_other_cells > 0:
                cur_X = i + self.dx[k]
                cur_Y = j + self.dy[k]
                while self.BOARD_LEN > cur_X >= 0 and self.BOARD_LEN > cur_Y >= 0 :
                    if self.board[cur_X][cur_Y] == opp:
                        self.board[cur_X][cur_Y] = turn
                        cur_X += self.dx[k]
                        cur_Y += self.dy[k]
                    else:
                        break
        self.board[i][j] = turn

    def board_to_str(self):
        ret = ''
        for i in range(self.BOARD_LEN):
            for j in range(self.BOARD_LEN):
                ret += self.board[i][j]

        return ret

    # TODO: remove this code in server
    def str_to_board(self, board_str):
        l = 0
        board = [[self.EMPTY_CELL for x in range(self.BOARD_LEN)] for y in range(self.BOARD_LEN)]

        for i in range(self.BOARD_LEN):
            for j in range(self.BOARD_LEN):
                board[i][j] = board_str[l]
                l += 1
        return board