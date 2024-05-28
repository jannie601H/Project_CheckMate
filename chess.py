#추가 필요
#폰 끝에 도달 시 변환
#게임 종료(맨 밑에 추가할 부분 #=====로 표시해 놓음)
#prototype 패턴 위한 clone 함수

#현재 strategy와 bridge 패턴 사용

import tkinter as tk
from abc import ABC, abstractmethod
import copy

# set color using bridge pattern
# color API
class Color(ABC):
    @abstractmethod
    def get_color(self):
        pass

# Bridge pattern - Black/White
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

# Strategy pattern - PawnBlack/PawnWhite
class PawnBlack(Black):
    def move_dir(self):
        return 1
    
class PawnWhite(White):
    def move_dir(self):
        return -1
    


# Piece API
class Piece:
    #switch = True -> white 차례
    switch = True
    numbering = 0
    def __init__(self, color:Color, symbol, row, col, game):
        self.color = color
        self.row = row
        self.col = col
        self.symbol = symbol
        self.tag = "p"+str(Piece.numbering)
        Piece.numbering += 1
        self.click = False
        self.canvas = game.canvas
        self.board = game.board
        self.game = game
 
    def get_symbol(self):
        return self.symbol
    
    def get_color(self):
        return self.color.get_color()
    
    def get_loc(self):
        """return location (row, col)"""
        return (self.row, self.col)
    
    def change_loc(self, r, c):
        self.row = r
        self.col = c
    
    def movable_loc(self):
        """return movable location list"""
        pass

    def draw_piece(self, x0, y0):
        self.canvas.create_rectangle(x0+1, y0+1, x0+49, y0+49, outline='', width=1, tags=self.tag + 'out')
        self.canvas.create_text(x0 + 25, y0 + 25, text=self.symbol, font=("Arial", 24), fill=self.color.get_color(), tags=self.tag)
        

    def bind_key(self):
        self.canvas.tag_bind(self.tag, "<Button-1>", self.click_piece)
        self.canvas.tag_bind(self.tag+'out', "<Button-1>", self.click_piece)

    def deletion(self):
        self.canvas.delete(self.tag)
        self.canvas.delete(self.tag+'out')
        del(self)

    def move_piece(self, x0, y0):
        self.canvas.delete(self.tag)
        self.canvas.delete(self.tag+'out')
        self.draw_piece(x0, y0)

    def click_piece(self, event):
        if (Piece.switch and self.color.get_color() == 'white') or (not Piece.switch and self.color.get_color() == 'black'):
            movable = []
            if self.click:
                self.canvas.itemconfig(self.tag + "out", outline='')
                self.game.set_current(None)
            else:
                if self.game.current_piece:
                    self.game.current_piece.another_click()
                self.canvas.itemconfig(self.tag + "out", outline='red')
                movable = self.movable_loc(self.board)
                self.game.set_current(self)
            self.click = not self.click
            self.game.check_moveables(movable)

    def another_click(self):
        self.click = False
        self.canvas.itemconfig(self.tag + "out", outline='')

    # clone method for Prototype pattern
    def clone(self, r, c):
        pass

# chess piece emojis R': '♜', 'N': '♞', 'B': '♝', 'Q': '♛', 'K': '♚', 'P': '♟'

def in_board(r, c): # check r, c in board
    return r <= 7 and r >= 0 and c <= 7 and c >= 0

def check_board(r, c, board):
    if board[r][c] == None:
        return False
    elif board[r][c].get_color() == 'black':
        return 'black'
    elif board[r][c].get_color() == 'white':
        return 'white'

class Pawn(Piece):
    def __init__(self, color:Color, row, col, game):
        super().__init__(color, "♙", row, col, game)
        self.first_move = True # pawn can move 2 step forward in first move

    # Strategy pattern application
    def get_dir(self):
        return self.color.move_dir()
        
    def movable_loc(self, board):
        move_dir = self.get_dir()
        movable = []
        if self.get_color() == 'black':
            en_color = 'white'
        elif self.get_color() == 'white':
            en_color = 'black'
            
        if in_board(self.row+move_dir, self.col) and not check_board(self.row+move_dir, self.col, self.board):
            movable.append((self.row + move_dir, self.col))

            if self.first_move and not check_board(self.row + 2*move_dir, self.col, self.board):
                movable.append((self.row + 2*move_dir, self.col))

        if in_board(self.row+move_dir, self.col+1) and check_board(self.row+move_dir, self.col+1, self.board) == en_color:
            movable.append((self.row+move_dir, self.col+1))

        if in_board(self.row+move_dir, self.col-1) and check_board(self.row+move_dir, self.col-1, self.board) == en_color:
            movable.append((self.row+move_dir, self.col-1))
        return movable

    def move_piece(self, x0, y0):
        if self.first_move:
            self.first_move = False
        super().move_piece(x0, y0)
    
    def clone(self, r, c):
        # Create a shallow copy of the piece
        cloned_piece = copy.copy(self)
        # Manually reset mutable attributes that shouldn't be shared
        cloned_piece.change_loc(r, c)
        cloned_piece.tag = "p" + str(Piece.numbering)
        Piece.numbering += 1
        # Reassign the game-specific attributes
        cloned_piece.canvas = self.game.canvas
        cloned_piece.board = self.game.board
        cloned_piece.game = self.game
        return cloned_piece


class Rook(Piece):
    def __init__(self, color:Color, row, col, game):
        super().__init__(color, "♖", row, col, game)

    def movable_loc(self, board):
        movable = []
        r_dir = [0, 1, 0, -1]
        c_dir = [1, 0, -1, 0]
        for i in range(4):
            r = self.row + r_dir[i]
            c = self.col + c_dir[i]
            while in_board(r, c):
                res = check_board(r, c, self.board)
                if res == self.get_color():
                    break
                movable.append((r, c))
                if res:
                    break
                r += r_dir[i]
                c += c_dir[i]
        return movable
        

class Knight(Piece):
    def __init__(self, color:Color, row, col, game):
        super().__init__(color, "♘", row, col, game)

    def movable_loc(self, board):
        movable = []
        r, c = self.row, self.col
        if in_board(r+2, c+1) and (board[r+2][c+1] == None or board[r+2][c+1].get_color() != self.color.get_color()):
            movable.append((r+2, c+1))
        
        if in_board(r+2, c-1) and (board[r+2][c-1] == None or board[r+2][c-1].get_color() != self.color.get_color()):
            movable.append((r+2, c-1))

        if in_board(r+1, c+2) and (board[r+1][c+2] == None or board[r+1][c+2].get_color() != self.color.get_color()):
            movable.append((r+1, c+2))

        if in_board(r+1, c-2) and (board[r+1][c-2] == None or board[r+1][c-2].get_color() != self.color.get_color()):
            movable.append((r+1, c-2))

        if in_board(r-1, c+2) and (board[r-1][c+2] == None or board[r-1][c+2].get_color() != self.color.get_color()):
            movable.append((r-1, c+2))

        if in_board(r-1, c-2) and (board[r-1][c-2] == None or board[r-1][c-2].get_color() != self.color.get_color()):
            movable.append((r-1, c-2))

        if in_board(r-2, c+1) and (board[r-2][c+1] == None or board[r-2][c+1].get_color() != self.color.get_color()):
            movable.append((r-2, c+1))

        if in_board(r-2, c-1) and (board[r-2][c-1] == None or board[r-2][c-1].get_color() != self.color.get_color()):
            movable.append((r-2, c-1))

        return movable
    

class Bishop(Piece):
    def __init__(self, color:Color, row, col, game):
        super().__init__(color, "♗", row, col, game)

    def movable_loc(self, board):
        movable = []
        r_dir = [1, 1, -1, -1]
        c_dir = [1, -1, -1, 1]
        for i in range(4):
            r = self.row + r_dir[i]
            c = self.col + c_dir[i]
            while in_board(r, c):
                res = check_board(r, c, self.board)
                if res == self.get_color():
                    break
                movable.append((r, c))
                if res:
                    break
                r += r_dir[i]
                c += c_dir[i]
        return movable
    


class Queen(Piece):
    def __init__(self, color:Color, row, col, game):
        super().__init__(color, "♕", row, col, game)

    def movable_loc(self, board):
        movable = []
        r_dir = [0, 1, 1, 1, 0, -1, -1, -1]
        c_dir = [1, 1, 0, -1, -1, -1, 0, 1]
        for i in range(8):
            r = self.row + r_dir[i]
            c = self.col + c_dir[i]
            while in_board(r, c):
                res = check_board(r, c, self.board)
                if res == self.get_color():
                    break
                movable.append((r, c))
                if res:
                    break
                r += r_dir[i]
                c += c_dir[i]
        return movable
    

class King(Piece):
    def __init__(self, color:Color, row, col, game):
        super().__init__(color, "♔", row, col, game)

    def movable_loc(self, board):
        movable = []
        r, c = self.row, self.col

        if in_board(r+1, c) and (board[r+1][c] == None or board[r+1][c].get_color() != self.color.get_color()):
            movable.append((r+1, c))
        
        if in_board(r+1, c+1) and (board[r+1][c+1] == None or board[r+1][c+1].get_color() != self.color.get_color()):
            movable.append((r+1, c+1))

        if in_board(r+1, c-1) and (board[r+1][c-1] == None or board[r+1][c-1].get_color() != self.color.get_color()):
            movable.append((r+1, c-1))

        if in_board(r, c+1) and (board[r][c+1] == None or board[r][c+1].get_color() != self.color.get_color()):
            movable.append((r, c+1))

        if in_board(r, c-1) and (board[r][c-1] == None or board[r][c-1].get_color() != self.color.get_color()):
            movable.append((r, c-1))

        if in_board(r-1, c) and (board[r-1][c] == None or board[r-1][c].get_color() != self.color.get_color()):
            movable.append((r-1, c))

        if in_board(r-1, c+1) and (board[r-1][c+1] == None or board[r-1][c+1].get_color() != self.color.get_color()):
            movable.append((r-1, c+1))

        if in_board(r-1, c-1) and (board[r-1][c-1] == None or board[r-1][c-1].get_color() != self.color.get_color()):
            movable.append((r-1, c-1))

        return movable
    

class ChessGame:
    def __init__(self, master):
        self.master = master
        self.master.title("체스 게임")
        self.pieces = []  # 말 객체를 저장할 리스트        
        self.board = [[None] * 8 for _ in range(8)]
        self.square_size = 50
        self.current_piece = None

        self.canvas = tk.Canvas(master, width=400, height=400)
        self.canvas.pack()

        self.create_pieces()  # 말 객체 생성 및 리스트에 추가
        self.create_board()  # 보드 생성

        self.draw_board()

    def create_pieces(self):
        # Prototype here
        # set black pawn
        bp = Pawn(PawnBlack(), None, None, self) # Prototype
        for col in range(8):
            self.pieces.append(bp.clone(1, col))
        
        # set white pawn
        wp = Pawn(PawnWhite(), None, None, self) # Prototype
        for col in range(8):
            self.pieces.append(wp.clone(6, col))

        # set pieces
        for row in [0, 7]:
            for col, piece_class in enumerate([Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]):
                if row == 0:
                    self.pieces.append(piece_class(Black(), row, col, self))
                else:
                    self.pieces.append(piece_class(White(), row, col, self))

        # set pawns
        # for row in [1, 6]:
        #     for col, piece_class in enumerate([Pawn]*8):
        #         if row == 1:
        #             self.pieces.append(piece_class(PawnBlack(), row, col, self))
        #         else:
        #             self.pieces.append(piece_class(PawnWhite(), row, col, self))

    def create_board(self):
        for piece in self.pieces:
            if piece:
                self.board[piece.row][piece.col] = piece

    def draw_board(self):
        dark_color = "#769656"
        light_color = "#CFE6B3"
        for row in range(8):
            for col in range(8):
                x0, y0 = col * self.square_size, row * self.square_size
                x1, y1 = x0 + self.square_size, y0 + self.square_size
                color = dark_color if (row + col) % 2 == 0 else light_color
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, tags="square")
                piece = self.board[row][col]
                if piece is not None:
                    piece.draw_piece(x0, y0)
                    piece.bind_key()

    def move_piece(self, event):
        dest = event.widget.find_withtag('current')[0]
        x, y = self.canvas.coords(dest)[0:2]
        self.canvas.delete('moveables')
        r, c = round(y/self.square_size-0.3), round(x/self.square_size-0.3)
        dest_loc = self.board[r][c]
        if isinstance(dest_loc, King):
            self.end_game(self.current_piece.get_color())
        if dest_loc != None:
            dest_loc.deletion()
        self.current_piece.move_piece(x - 0.3*self.square_size, y-0.3*self.square_size)
        self.board[r][c] = self.current_piece
        self.board[self.current_piece.row][self.current_piece.col] = None
        self.current_piece.change_loc(r, c)
        Piece.switch = not Piece.switch
        

    def check_moveables(self, loc_list):
        self.canvas.delete('moveables')
        for loc in loc_list:
            self.canvas.create_oval((loc[1]+0.3)*self.square_size, (loc[0]+0.3)*self.square_size, (loc[1]+0.7)*self.square_size, (loc[0]+0.7)*self.square_size, fill='blue', tags='moveables')
        self.canvas.tag_bind('moveables', '<Button-1>', self.move_piece)
        
    def set_current(self, piece):
        self.current_piece = piece
#================================================================================================
#================================================================================================
#================================================================================================
#================================================================================================
#================================================================================================
    def end_game(self, win):
        print(win)
#================================================================================================
#================================================================================================
#================================================================================================
#================================================================================================
#================================================================================================

root = tk.Tk()
game = ChessGame(root)

root.mainloop()
