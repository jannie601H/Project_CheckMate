import tkinter as tk
from abc import ABC, abstractmethod

# chess piece emojis R': '♜', 'N': '♞', 'B': '♝', 'Q': '♛', 'K': '♚', 'P': '♟'

# set color using bridge pattern
# color API
class Color(ABC):
    @abstractmethod
    def get_color(self):
        pass

class Black(Color):
    def get_color(self):
        return "black"

class White(Color):
    def get_color(self):
        return "white"

# Piece API
class Piece:
    def __init__(self, color:Color, symbol, row, col):
        self.color = color
        self.row = row
        self.col = col
        self.symbol = symbol

    def get_symbol(self):
        return self.symbol

class Pawn(Piece):
    def __init__(self, color:Color, row, col):
        super().__init__(color, "♙", row, col)

class Rook(Piece):
    def __init__(self, color:Color, row, col):
        super().__init__(color, "♖", row, col)

class Knight(Piece):
    def __init__(self, color:Color, row, col):
        super().__init__(color, "♘", row, col)

class Bishop(Piece):
    def __init__(self, color:Color, row, col):
        super().__init__(color, "♗", row, col)

class Queen(Piece):
    def __init__(self, color:Color, row, col):
        super().__init__(color, "♕", row, col)

class King(Piece):
    def __init__(self, color:Color, row, col):
        super().__init__(color, "♔", row, col)

class ChessGame:
    def __init__(self, master):
        self.master = master
        self.master.title("체스 게임")
        self.pieces = []  # 말 객체를 저장할 리스트
        self.create_pieces()  # 말 객체 생성 및 리스트에 추가
        self.create_board()  # 보드 생성

        self.canvas = tk.Canvas(master, width=400, height=400)
        self.canvas.pack()
        self.draw_board()

    def create_pieces(self):
        # set pieces
        for row in [0, -1]:
            for col, piece_class in enumerate([Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]):
                if row == 0:
                    self.pieces.append(piece_class(Black(), row, col))
                else:
                    self.pieces.append(piece_class(White(), row, col))

        # set pawns
        for row in [1, -2]:
            for col, piece_class in enumerate([Pawn]*8):
                if row == 1:
                    self.pieces.append(piece_class(Black(), row, col))
                else:
                    self.pieces.append(piece_class(White(), row, col))

    def create_board(self):
        self.board = [[None] * 8 for _ in range(8)]
        for piece in self.pieces:
            if piece:
                self.board[piece.row][piece.col] = piece

    def draw_board(self):
        dark_color = "#769656"
        light_color = "#eeeed2"
        square_size = 50
        for row in range(8):
            for col in range(8):
                x0, y0 = col * square_size, row * square_size
                x1, y1 = x0 + square_size, y0 + square_size
                color = dark_color if (row + col) % 2 == 0 else light_color
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, tags="square")
                piece = self.board[row][col]
                if piece is not None:
                    self.canvas.create_text(x0 + 25, y0 + 25, text=piece.get_symbol(), font=("Arial", 24), fill=piece.color.get_color(), tags="piece")

root = tk.Tk()
game = ChessGame(root)
root.mainloop()
