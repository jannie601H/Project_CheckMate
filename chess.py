#추가 필요
#폰 끝에 도달 시 변환 - 수정중
#게임 종료(맨 밑에 추가할 부분 #=====로 표시해 놓음) - 끝날때 재시작 기능 추가?


#현재 사용 패턴 - strategy, bridge, composite, prototype

from copy import deepcopy
import tkinter as tk
from abc import ABC, abstractmethod

# set color using bridge pattern  
#Piece - Color bridge pattern으로 이음
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

#strategy로 이용
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
    def __init__(self, color:Color, symbol, row, col):
        self.color = color
        self.row = row
        self.col = col
        self.symbol = symbol
        self.tag = "p"+str(Piece.numbering)
        Piece.numbering += 1
        self.name = None
        self.click = False

    #tkinter의 위젯은 deepcopy가 안 되서 tkinter 관련 변수 setting은 따로 빼놓고 복사 후 세팅
    def setGame(self, game):
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
        self.board[r][c] = self
        self.board[self.row][self.col] = None
        self.row = r
        self.col = c

    def set_loc(self, r, c):
        self.board[r][c] = self
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

    #prototype pattern(프토로타입) - chessgame의 함수(맨밑)에서 이용
    def clone(self, row, col, game):
        res = deepcopy(self)
        res.setGame(game)
        res.set_loc(row, col)
        res.tag = "p" + str(Piece.numbering)
        Piece.numbering += 1
    
    #composite pattern - chessgame 클래스 위에 composite인 PieceGroup 있음
    def setting(self, game):
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
    def __init__(self, color:Color, row, col):
        super().__init__(color, "♙", row, col)
        self.first_move = True # pawn can move 2 step forward in first move

    def get_dir(self):
        return self.color.move_dir()
        
    def movable_loc(self, board):
        #PawnBlack과 PawnWhite를 이용한 strategy 패턴
        move_dir = self.get_dir()
        movable = []
        if self.get_color() == 'black':
            en_color = 'white'
        elif self.get_color() == 'white':
            en_color = 'black'
            
        if not check_board(self.row+move_dir, self.col, self.board):
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

    def setting(self, game):
        if self.get_color() == 'white':
            for i in range(8):
                self.clone(6, i, game)

        elif self.get_color() == 'black':
            for i in range(8):
                self.clone(1, i, game)
        
    def change_piece(self, available):
        buttons = []
        num = 0
        self.canvas.create_rectangle(40, 162, 360, 238, fill='light grey', tags='button')
        for P_type in available:
            buttons.append(tk.Button(self.game.master, overrelief='solid', width=56, height=56, command=lambda: self.change(P_type, buttons)))
            buttons[-1].place(x=50+66*num, y=172)
            num += 1

    def change(self, piece:Piece, buttonlist):
        square_size = 50
        self.canvas.delete('button')
        for i in buttonlist:
            i.destroy()
        piece.clone(self.row, self.col, self.game)
        x0, y0 = self.col * square_size, self.row * square_size
        piece.draw_piece(x0, y0)
        piece.bind_key()
        self.deletion()


class Rook(Piece):
    def __init__(self, color:Color, row, col):
        super().__init__(color, "♖", row, col)

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

    def setting(self, game):
        if self.get_color() == 'white':
            for i in [0, 7]:
                self.clone(7, i, game)

        elif self.get_color() == 'black':
            for i in [0, 7]:
                self.clone(0, i, game)
        
        

class Knight(Piece):
    def __init__(self, color:Color, row, col):
        super().__init__(color, "♘", row, col)

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
    
    def setting(self, game):
        if self.get_color() == 'white':
            for i in [1, 6]:
                self.clone(7, i, game)

        elif self.get_color() == 'black':
            for i in [1, 6]:
                self.clone(0, i, game)

class Bishop(Piece):
    def __init__(self, color:Color, row, col):
        super().__init__(color, "♗", row, col)

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

    def setting(self, game):
        if self.get_color() == 'white':
            for i in [2, 5]:
                self.clone(7, i, game)

        elif self.get_color() == 'black':
            for i in [2, 5]:
                self.clone(0, i, game)


class Queen(Piece):
    def __init__(self, color:Color, row, col):
        super().__init__(color, "♕", row, col)

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
    
    def setting(self, game):
        if self.get_color() == 'white':
            self.clone(7, 3, game)

        elif self.get_color() == 'black':
            self.clone(0, 3, game)


class King(Piece):
    def __init__(self, color:Color, row, col):
        super().__init__(color, "♔", row, col)

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
    
    def setting(self, game):
        if self.get_color() == 'white':
            self.clone(7, 4, game)

        elif self.get_color() == 'black':
            self.clone(0, 4, game)

#composite pattern. Component는 Piece, 각 말의 종류가 leaf
class PieceGroup(Piece):    
    def __init__(self):
        self.pieces = []

    def add(self, piece:Piece):
        self.pieces.append(piece)

    def setName(self, name):
        self.name = name

    #최상위 composite에 사용하여 특정 색의 pawn이 변할 수 있는 말을 모아놓은 composite 호출
    def getComposite(self, name):
        for i in self.pieces:
            if i.name == 'changeable':
                for k in i.pieces:
                    if k.name == name:
                        return k.pieces

    def setting(self, game):
        for piece in self.pieces:
            piece.setting(game)

class ChessGame:
    def __init__(self, master):
        self.master = master
        self.master.title("체스 게임")
        self.pieces = PieceGroup() # 말 객체를 저장할 리스트        
        self.board = [[None] * 8 for _ in range(8)]
        self.square_size = 50
        self.current_piece = None

        self.canvas = tk.Canvas(master, width=400, height=400)
        self.canvas.pack()

        self.create_pieces()  # 말 객체 생성 및 리스트에 추가
        self.create_board()  # 보드 생성

        self.draw_board()
        ### test
        # print(self.board[6][3].movable_loc(self.board))
        # self.move_piece(1, 0, 2, 0)
        # self.draw_board()
        # print(self.board[2][0].get_loc())

    def create_pieces(self):
        # set pieces
        self.pieces.add(Pawn(PawnBlack(), None, None))
        self.pieces.add(Pawn(PawnWhite(), None, None))
        self.pieces.add(King(Black(), None, None))
        self.pieces.add(King(White(), None, None))

        #폰이 변할 수 있는 목록
        changeable = PieceGroup()
        changeable.setName('changeable')
        black = PieceGroup()
        white = PieceGroup()
        black.setName('black')
        white.setName('white')
        black.add(Queen(Black(), None, None))
        white.add(Queen(White(), None, None))
        black.add(Rook(Black(), None, None))
        white.add(Rook(White(), None, None))
        black.add(Knight(Black(), None, None))
        white.add(Knight(White(), None, None))
        black.add(Bishop(Black(), None, None))
        white.add(Bishop(White(), None, None))
        changeable.add(black)
        changeable.add(white)
        self.pieces.add(changeable)
        
        

    def create_board(self):
        self.pieces.setting(self)

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

    def move_piece(self, event): # move piece on (r, c) to (nr, nc)
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
        self.current_piece.change_loc(r, c)
        '''
        if isinstance(self.current_piece, Pawn) and (self.current_piece.row == 0 or self.current_piece.row == 7):
            self.current_piece.change_piece(self.pieces.getComposite(self.current_piece.get_color()))
        '''
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
