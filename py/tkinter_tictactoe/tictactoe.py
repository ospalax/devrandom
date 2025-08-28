#!/usr/bin/env python3

__all__ = [
    "__title__",
    "__summary__",
    "__version__",
    "__author__",
]

__title__ = "tictactoe"
__summary__ = "Dumb Tic Tac Toe in Tkinter"
__version__ = "1.0.0"
__author__ = "Petr Ospalý"

import sys
import tkinter as tk
import tkinter.font as font

PLAYER1 = "X"
PLAYER1_COLOR = "blue"
PLAYER2 = "O"
PLAYER2_COLOR = "red"

PLAY = 0
WINNER1 = 1
WINNER2 = 2
TIE = 3

#GAME_START = f"{PLAYER1} Starts Game!"
GAME_START = "Start Game!"

class MyButton(tk.Button):
    def __init__(self, row, col, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.row_index = row
        self.col_index = col
        self.player = None

class Game(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tic Tac Toe")
        self.size = 3 # for now
        self.board = self._make_board(self.size)
        self.game = self._start_game()
        self.setup_gui()

    def _make_board(self, size):
        if not isinstance(size, int):
            raise ValueError("Size of the board must be an integer")

        board = [ [ None for c in range(size) ]
                    for r in range(size) ]
        return board

    def _start_game(self):
        state = {}

        state["last"] = None
        state["next"] = PLAYER1
        state["state"] = PLAY # WINNER1 WINNER2 TIE

        return state

    def reset_game(self):
        for row in self.board:
            for button in row:
                button.config(text="")
        self.game_status.config(text=GAME_START)
        self.game_status["fg"] = "black"
        self.game = self._start_game()

    def setup_gui(self):
        menu = tk.Menu(master=self)
        self.config(menu=menu)
        menu_items = tk.Menu(master=menu)
        menu_items.add_command(label="New Game",
                               command=self.reset_game)
        menu_items.add_command(label="Quit",
                               command=quit)
        menu.add_cascade(label="Menu", menu=menu_items)

        grid = tk.Frame(master=self)
        grid.pack()
        for row in range(self.size):
            self.rowconfigure(row, weight=1, minsize=100)
            self.columnconfigure(row, weight=1, minsize=100)
            for col in range(self.size):
                button = MyButton(
                    row=row,
                    col=col,
                    master=grid,
                    text="",
                    fg="black",
                    highlightbackground="yellow",
                    font=font.Font(family="Monospace",
                                   size=40, weight="bold"),
                    width=4,
                    height=2,
                )
                #button.bind("<ButtonPress-1>", self.test)
                button.bind("<ButtonPress-1>", self.play)
                self.board[row][col] = button
                button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

        status = tk.Frame(master=self)
        status.pack(fill=tk.X)
        self.game_status = tk.Label(
            master=status,
            text=GAME_START,
            font=font.Font(family="Monospace",
                           size=32, weight="bold"),
        )
        self.game_status.pack()

    def test(self, event):
        button = event.widget
        row = button.row_index
        col = button.col_index
        if button["text"] == "":
            button.config(text=f"{row},{col}")
        else:
            button.config(text="")

    def play(self, event):
        if self.game["state"] != PLAY:
            return

        button = event.widget
        row = button.row_index
        col = button.col_index

        current = self.game["next"]
        if current == PLAYER1:
            self.game["next"] = PLAYER2
            self.game["last"] = PLAYER1
        else:
            self.game["next"] = PLAYER1
            self.game["last"] = PLAYER2

        self._update_button(button, current)

        self._check_game()

        self._update_status()

    def _update_button(self, button, player):
        if player == PLAYER1:
            button.config(text=f"{player}",
                          fg=PLAYER1_COLOR)
        else:
            button.config(text=f"{player}",
                          fg=PLAYER2_COLOR)

    def _update_status(self):
        if self.game["state"] == PLAY:
            next = self.game["next"]
            self.game_status["text"] = f"{next} has turn!"
            if next == PLAYER1:
                self.game_status["fg"] = PLAYER1_COLOR
            else:
                self.game_status["fg"] = PLAYER2_COLOR

        if self.game["state"] == WINNER1:
            self.game_status["text"] = f"{PLAYER1} WON!"
            self.game_status["fg"] = PLAYER1_COLOR
        elif self.game["state"] == WINNER2:
            self.game_status["text"] = f"{PLAYER2} WON!"
            self.game_status["fg"] = PLAYER2_COLOR
        elif self.game["state"] == TIE:
            self.game_status["text"] = "IT IS A TIE!"
            self.game_status["fg"] = "black"

    def _check_game(self):
        player1 = [ [ 0 for c in range(self.size) ]
                    for r in range(self.size) ]
        player2 = [ [ 0 for c in range(self.size) ]
                    for r in range(self.size) ]
        full_board = True

        for row in self.board:
            for button in row:
                if button["text"] == PLAYER1:
                    player1[button.row_index][button.col_index] = 1
                elif button["text"] == PLAYER2:
                    player2[button.row_index][button.col_index] = 1
                else:
                    full_board = False

        # quick and dirty...
        player1_completed = False
        player2_completed = False

        # rows
        for row in range(self.size):
            player1_count = 0
            player2_count = 0

            for col in range(self.size):
                player1_count += player1[row][col]
                player2_count += player2[row][col]

            if player1_count == 3:
                player1_completed = True

            if player2_count == 3:
                player2_completed = True

        # cols
        for col in range(self.size):
            player1_count = 0
            player2_count = 0

            for row in range(self.size):
                player1_count += player1[row][col]
                player2_count += player2[row][col]

            if player1_count == 3:
                player1_completed = True

            if player2_count == 3:
                player2_completed = True

        # diagonals
        player1_diag1_count = 0
        player1_diag2_count = 0
        player2_diag1_count = 0
        player2_diag2_count = 0

        for i in range(self.size):
            player1_diag1_count += player1[i][i]
            player1_diag2_count += player1[i][self.size - i -1]

            player2_diag1_count += player2[i][i]
            player2_diag2_count += player2[i][self.size - i -1]

        if (player1_diag1_count == 3) or (player1_diag2_count == 3):
            player1_completed = True

        if (player2_diag1_count == 3) or (player2_diag2_count == 3):
            player2_completed = True

        if player1_completed and player2_completed:
            self.game["state"] = TIE
        elif player1_completed:
            self.game["state"] = WINNER1
        elif player2_completed:
            self.game["state"] = WINNER2
        elif full_board:
            self.game["state"] = TIE


def main():
    game = Game()
    game.mainloop()
    return 0

if __name__ == "__main__":
    sys.exit(main())
