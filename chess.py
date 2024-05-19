import tkinter as tk
from abc import ABC, abstractmethod

# set color using bridge pattern
# color API
class Color(ABC):
    @abstractmethod
    def get_color(self):
        pass

class Black(Color):
    def __init__(self):
        self.color = "black"

    def get_color(self):
        return self.color

class White(Color):
    def __init__(self):
        self.color = "white"

    def get_color(self):
        return self.color

# Piece API
class Piece:
    def __init__(self, color:Color, symbol, row, col):
        self.color = color
        self.row = row
        self.col = col
        self.symbol = symbol
        self.movable = []

    def get_symbol(self):
        return self.symbol
    
    def get_color(self):
        return self.color.get_color()
    
    def get_loc(self):
        """return location (row, col)"""
        return (self.row, self.col)
    
    def movable_loc(self):
        """return movable location list"""
        pass

# chess piece emojis R': '♜', 'N': '♞', 'B': '♝', 'Q': '♛', 'K': '♚', 'P': '♟'

def in_board(r, c): # check r, c in board
    return r <= 7 and r >= 0 and c <= 7 and c >= 0

class Pawn(Piece):
    def __init__(self, color:Color, row, col):
        super().__init__(color, "♙", row, col)

    def movable_loc(self, board): # initial position pawn can move 2 step (needed)
        r, c = self.row, self.col
        if in_board(r+1, c+1) and board[r+1][c+1] != None:
            self.movable.append((r+1, c+1))
        elif in_board(r+1, c-1) and board[r+1][c-1] != None:
            self.movable.append((r+1, c-1))
        if in_board(r+1, c) and board[r+1][c] == None:
            self.movable.append((r+1, c))
        return self.movable

class Rook(Piece):
    def __init__(self, color:Color, row, col):
        super().__init__(color, "♖", row, col)

    def movable_loc(self, board):
        r, c = self.row, self.col
        while in_board(r+1, c) and (board[r+1][c] == None):
            self.movable.append((r+1, c))
            r += 1
        if in_board(r+1, c) and (board[r+1][c] != None and board[r+1][c].get_color() != self.color.get_color()): self.movable.append((r+1, c)) # 상대말 잡는경우

        r, c = self.row, self.col
        while in_board(r-1, c) and (board[r-1][c] == None):
            self.movable.append((r-1, c))
            r -= 1
        if in_board(r-1, c) and (board[r-1][c] != None and board[r-1][c].get_color() != self.color.get_color()): self.movable.append((r-1, c))
       
        r, c = self.row, self.col
        while in_board(r, c+1) and (board[r][c+1] == None):
            self.movable.append((r, c+1))
            c += 1
        if in_board(r, c+1) and (board[r][c+1] != None and board[r][c+1].get_color() != self.color.get_color()): self.movable.append((r, c+1))
        
        r, c = self.row, self.col
        while in_board(r, c-1) and (board[r][c-1] == None):
            self.movable.append((r, c-1))
            c -= 1
        if in_board(r, c-1) and (board[r][c-1] != None and board[r][c-1].get_color() != self.color.get_color()): self.movable.append((r, c-1))
       
        return self.movable
        

class Knight(Piece):
    def __init__(self, color:Color, row, col):
        super().__init__(color, "♘", row, col)

    def movable_loc(self, board):
        r, c = self.row, self.col
        if in_board(r+2, c+1) and (board[r+2][c+1] == None or board[r+2][c+1].get_color() != self.color.get_color()):
            self.movable.append((r+2, c+1))
        
        if in_board(r+2, c-1) and (board[r+2][c-1] == None or board[r+2][c-1].get_color() != self.color.get_color()):
            self.movable.append((r+2, c-1))

        if in_board(r+1, c+2) and (board[r+1][c+2] == None or board[r+1][c+2].get_color() != self.color.get_color()):
            self.movable.append((r+1, c+2))

        if in_board(r+1, c-2) and (board[r+1][c-2] == None or board[r+1][c-2].get_color() != self.color.get_color()):
            self.movable.append((r+1, c-2))

        if in_board(r-1, c+2) and (board[r-1][c+2] == None or board[r-1][c+2].get_color() != self.color.get_color()):
            self.movable.append((r-1, c+2))

        if in_board(r-1, c-2) and (board[r-1][c-2] == None or board[r-1][c-2].get_color() != self.color.get_color()):
            self.movable.append((r-1, c-2))

        if in_board(r-2, c+1) and (board[r-2][c+1] == None or board[r-2][c+1].get_color() != self.color.get_color()):
            self.movable.append((r-2, c+1))

        if in_board(r-2, c-1) and (board[r-2][c-1] == None or board[r-2][c-1].get_color() != self.color.get_color()):
            self.movable.append((r-2, c-1))

        return self.movable

class Bishop(Piece):
    def __init__(self, color:Color, row, col):
        super().__init__(color, "♗", row, col)

    def movable_loc(self, board):
        r, c = self.row, self.col
        while in_board(r+1, c+1) and board[r+1][c+1] == None:
            self.movable.append((r+1, c+1))
            r, c = r+1, c+1
        if in_board(r+1, c+1) and (board[r+1][c+1] != None and board[r+1][c+1].get_color != self.color.get_color()): self.movable.append((r+1, c+1))

        r, c = self.row, self.col
        while in_board(r-1, c-1) and board[r-1][c-1] == None:
            self.movable.append((r-1, c-1))
            r, c = r-1, c-1
        if in_board(r-1, c-1) and (board[r-1][c-1] != None and board[r-1][c-1].get_color != self.color.get_color()): self.movable.append((r-1, c-1))

        r, c = self.row, self.col
        while in_board(r-1, c+1) and board[r-1][c+1] == None:
            self.movable.append((r-1, c+1))
            r, c = r-1, c+1
        if in_board(r-1, c+1) and (board[r-1][c+1] != None and board[r-1][c+1].get_color != self.color.get_color()): self.movable.append((r-1, c+1))

        while in_board(r+1, c-1) and board[r+1][c-1] == None:
            self.movable.append((r+1, c-1))
            r, c = r+1, c-1
        if in_board(r+1, c-1) and (board[r+1][c-1] != None and board[r+1][c-1].get_color != self.color.get_color()): self.movable.append((r+1, c-1))
        
        return self.movable

class Queen(Piece):
    def __init__(self, color:Color, row, col):
        super().__init__(color, "♕", row, col)

    def movable_loc(self, board):
        r, c = self.row, self.col
        while in_board(r+1, c) and (board[r+1][c] == None):
            self.movable.append((r+1, c))
            r += 1
        if in_board(r+1, c) and (board[r+1][c] != None and board[r+1][c].get_color() != self.color.get_color()): self.movable.append((r+1, c)) # 상대말 잡는경우

        r, c = self.row, self.col
        while in_board(r-1, c) and (board[r-1][c] == None):
            self.movable.append((r-1, c))
            r -= 1
        if in_board(r-1, c) and (board[r-1][c] != None and board[r-1][c].get_color() != self.color.get_color()): self.movable.append((r-1, c))
       
        r, c = self.row, self.col
        while in_board(r, c+1) and (board[r][c+1] == None):
            self.movable.append((r, c+1))
            c += 1
        if in_board(r, c+1) and (board[r][c+1] != None and board[r][c+1].get_color() != self.color.get_color()): self.movable.append((r, c+1))
        
        r, c = self.row, self.col
        while in_board(r, c-1) and (board[r][c-1] == None):
            self.movable.append((r, c-1))
            c -= 1
        if in_board(r, c-1) and (board[r][c-1] != None and board[r][c-1].get_color() != self.color.get_color()): self.movable.append((r, c-1))

        r, c = self.row, self.col
        while in_board(r+1, c+1) and board[r+1][c+1] == None:
            self.movable.append((r+1, c+1))
            r, c = r+1, c+1
        if in_board(r+1, c+1) and (board[r+1][c+1] != None and board[r+1][c+1].get_color != self.color.get_color()): self.movable.append((r+1, c+1))

        r, c = self.row, self.col
        while in_board(r-1, c-1) and board[r-1][c-1] == None:
            self.movable.append((r-1, c-1))
            r, c = r-1, c-1
        if in_board(r-1, c-1) and (board[r-1][c-1] != None and board[r-1][c-1].get_color != self.color.get_color()): self.movable.append((r-1, c-1))

        r, c = self.row, self.col
        while in_board(r-1, c+1) and board[r-1][c+1] == None:
            self.movable.append((r-1, c+1))
            r, c = r-1, c+1
        if in_board(r-1, c+1) and (board[r-1][c+1] != None and board[r-1][c+1].get_color != self.color.get_color()): self.movable.append((r-1, c+1))

        while in_board(r+1, c-1) and board[r+1][c-1] == None:
            self.movable.append((r+1, c-1))
            r, c = r+1, c-1
        if in_board(r+1, c-1) and (board[r+1][c-1] != None and board[r+1][c-1].get_color != self.color.get_color()): self.movable.append((r+1, c-1))
        
        return self.movable

class King(Piece):
    def __init__(self, color:Color, row, col):
        super().__init__(color, "♔", row, col)

    def movable_loc(self, board):
        r, c = self.row, self.col

        if in_board(r+1, c) and (board[r+1][c] == None or board[r+1][c].get_color() != self.color.get_color()):
            self.movable.append((r+1, c))
        
        if in_board(r+1, c+1) and (board[r+1][c+1] == None or board[r+1][c+1].get_color() != self.color.get_color()):
            self.movable.append((r+1, c+1))

        if in_board(r+1, c-1) and (board[r+1][c-1] == None or board[r+1][c-1].get_color() != self.color.get_color()):
            self.movable.append((r+1, c-1))

        if in_board(r, c+1) and (board[r][c+1] == None or board[r][c+1].get_color() != self.color.get_color()):
            self.movable.append((r, c+1))

        if in_board(r, c-1) and (board[r][c-1] == None or board[r][c-1].get_color() != self.color.get_color()):
            self.movable.append((r, c-1))

        if in_board(r-1, c) and (board[r-1][c] == None or board[r-1][c].get_color() != self.color.get_color()):
            self.movable.append((r-1, c))

        if in_board(r-1, c+1) and (board[r-1][c+1] == None or board[r-1][c+1].get_color() != self.color.get_color()):
            self.movable.append((r-1, c+1))

        if in_board(r-1, c-1) and (board[r-1][c-1] == None or board[r-1][c-1].get_color() != self.color.get_color()):
            self.movable.append((r-1, c-1))

        return self.movable

class ChessGame:
    def __init__(self, master):
        self.master = master
        self.master.title("체스 게임")
        self.pieces = []  # 말 객체를 저장할 리스트
        self.create_pieces()  # 말 객체 생성 및 리스트에 추가
        self.create_board()  # 보드 생성
        self.selected_piece = None  # 선택된 말

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
