#  Kevan Hong-Nhan Nguyen 71632979.  ICS 32 Lab sec 9.  Project #5.

import othello_set
import tkinter


# GUI / tkinter object constants
BACKGROUND_COLOR = '#696969'
GAME_COLOR = '#006000'
FONT = ('Helvetica', 30)
DIALOG_FONT = ('Helvetica', 20)
PLAYERS = {othello_set.BLACK: 'Black', othello_set.WHITE: 'White'}
VICTORY_TYPES = {othello_set.MOST_CELLS: 'Most Cells', othello_set.LEAST_CELLS: 'Least Cells'}

class GameBoard:
    def __init__(self, game_state: othello_set.OthelloGame, game_width: float,
                 game_height: float, root_window) -> None:
        # Initialize the game board's settings here
        self._game_state = game_state
        self._rows = self._game_state.get_rows()
        self._cols = self._game_state.get_columns()
        self._board = tkinter.Canvas(master = root_window,
                                     width = game_width,
                                     height = game_height,
                                     background = GAME_COLOR)

    def new_game_settings(self, game_state) -> None:
        ''' The game board's new game settings is now changed accordingly to
            the specified game state '''
        self._game_state = game_state
        self._rows = self._game_state.get_rows()
        self._cols = self._game_state.get_columns()

    def redraw_board(self) -> None:
        ''' Redraws the board '''
        self._board.delete(tkinter.ALL)
        self._redraw_lines()
        self._redraw_cells()

    def _redraw_lines(self) -> None:
        ''' Redraws the board's lines '''
        row_multiplier = float(self._board.winfo_height()) / self._rows
        col_multiplier = float(self._board.winfo_width()) / self._cols
        
        # Draw the horizontal lines first
        for row in range(1, self._rows):
            self._board.create_line(0, row * row_multiplier, self.get_board_width(), row * row_multiplier)

        # Draw the column lines next
        for col in range(1, self._cols):
            self._board.create_line(col * col_multiplier, 0, col * col_multiplier, self.get_board_height())

    def _redraw_cells(self) -> None:
        ''' Redraws all the occupied cells in the board '''
        for row in range(self._rows):
            for col in range(self._cols):
                if self._game_state.get_board()[row][col] != othello_set.NONE:
                    self._draw_cell(row, col)
                
    def _draw_cell(self, row: int, col: int) -> None:
        ''' Draws the specified cell '''
        self._board.create_oval(col * self.get_cell_width(),
                                row * self.get_cell_height(),
                                (col + 1) * self.get_cell_width(),
                                (row + 1) * self.get_cell_height(),
                                fill = PLAYERS[self._game_state.get_board()[row][col]])                               


    def update_game_state(self, game_state: othello_set.OthelloGame) -> None:
        ''' Updates our current _game_state to the specified one in the argument '''
        self._game_state = game_state

    def get_cell_width(self) -> float:
        ''' Returns a game cell's width '''
        return self.get_board_width() / self.get_columns()

    def get_cell_height(self) -> float:
        ''' Returns a game cell's height '''
        return self.get_board_height() / self.get_rows()

    def get_board_width(self) -> float:
        ''' Returns the board canvas's width '''
        return float(self._board.winfo_width())

    def get_board_height(self) -> float:
        ''' Returns the board canvas's height '''
        return float(self._board.winfo_height())

    def get_rows(self) -> int:
        ''' Returns the total number of rows in the board '''
        return self._rows

    def get_columns(self) -> int:
        ''' Returns the total number of rows in the board '''
        return self._cols

    def get_board(self) -> tkinter.Canvas:
        ''' Returns the game board '''
        return self._board


class Score:
    def __init__(self, color: str, game_state: othello_set.OthelloGame, root_window) -> None:
        ''' Initializes the score label '''
        self._player = color
        self._score = game_state.get_total_cells(self._player)
        self._score_label = tkinter.Label(master = root_window,
                                          text = self._score_text(),
                                          background = BACKGROUND_COLOR,
                                          fg = PLAYERS[color],
                                          font = FONT)

    def update_score(self, game_state: othello_set.OthelloGame) -> None:
        ''' Updates the score with the specified game state '''
        self._score = game_state.get_total_cells(self._player)
        self._change_score_text()

    def get_score_label(self) -> tkinter.Label:
        ''' Returns the score label '''
        return self._score_label

    def get_score(self) -> int:
        ''' Returns the score '''
        return self._score

    def _change_score_text(self) -> None:
        ''' Changes the score label's text '''
        self._score_label['text'] =  self._score_text()

    def _score_text(self) -> str:
        ''' Returns the score in text string format '''
        return PLAYERS[self._player] + ' - ' + str(self._score)



class Turn:
    def __init__(self, game_state: othello_set.OthelloGame, root_window) -> None:
        ''' Initializes the player's turn Label '''
        self._player = game_state.get_turn()
        self._turn_label = tkinter.Label(master = root_window,
                                          text = self._turn_text(),
                                          background = BACKGROUND_COLOR,
                                          fg = PLAYERS[self._player],
                                          font = FONT)

    def display_winner(self, winner: str) -> None:
        ''' Only called when the game is over. Displays the game winner '''
        if winner == None:
            victory_text = 'Tie game. Nobody wins!'
            text_color = 'BLACK'
        else:
            victory_text = PLAYERS[winner] + ' player wins!'
            text_color = PLAYERS[winner]
        self._turn_label['text'] = victory_text
        self._turn_label['fg'] = text_color

    def switch_turn(self, game_state: othello_set.OthelloGame) -> None:
        ''' Switch's the turn between the players '''
        self._player = game_state.get_turn()
        self.change_turn_text()

    def change_turn_text(self) -> None:
        ''' Changes the turn label's text '''
        self._turn_label['text'] = self._turn_text()
        self._turn_label['fg'] = PLAYERS[self._player]

    def get_turn_label(self) -> None:
        ''' Returns the tkinter turn label '''
        return self._turn_label

    def update_turn(self, turn: str) -> None:
        ''' Updates the turn to whatever the current game state's turn is '''
        self._player = turn
        self.change_turn_text()

    def _turn_text(self) -> None:
        ''' Returns the turn in text/string form '''
        return PLAYERS[self._player] + " player's turn"

    def _opposite_turn(self) -> None:
        ''' Returns the opposite turn of current turn '''
        return {othello_set.BLACK: othello_set.WHITE, othello_set.WHITE: othello_set.BLACK}[self._player]


# Dialog for when the user wants to change the game's settings
class OptionDialog:
    def __init__(self):
        self._dialog_window = tkinter.Toplevel()
        self._dialog_window.title("Setting")
        self._dialog_window.geometry("200x80+100+100")
        self._dialog_window.resizable(False, False)

        self.port=tkinter.Entry(self._dialog_window)
        self.port.place(x=55, y=20, width=130)

        self.port_label=tkinter.Label(self._dialog_window, text='PORT: ')
        self.port_label.place(x=10, y=20)

        self.ok_button=tkinter.Button(self._dialog_window, text="OK", command=self._on_ok_button)
        self.ok_button.place(x=100, y=50)

        self.cancel_button=tkinter.Button(self._dialog_window, text="Cancel", command=self._on_cancel_button)
        self.cancel_button.place(x=130, y=50)

        self.port_number = 0

        # Variable to determine what to do when the 'OK' button is clicked
        self._ok_clicked = False


    def show(self) -> None:
        self._dialog_window.grab_set()
        self._dialog_window.wait_window()

    def was_ok_clicked(self) -> bool:
        return self._ok_clicked

    def get_port(self):
        return self.port_number

    # Functions assigned to button commands
    def _on_ok_button(self):
        self._ok_clicked = True
        self.port_number = int(self.port.get())
        self._dialog_window.destroy()

    def _on_cancel_button(self):
        self._dialog_window.destroy()

