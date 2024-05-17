import tkinter as tk

#말이 판 밖으로 나가는지 여부 판별(0~7)
def InsideOfBoard(x, y):
    if 0 <= x and x <= 7 and 0 <= y and y <= 7:
        return True
    else: 
        return False

#말의 색 상위 클래스
class PieceColor:
    def __init__(self):
        self.color = None

#검/흰 색 클래스 - 폰 제외 나머지 말에 사용
class BlackPiece(PieceColor):
    def __init__(self):
        self.color = 'black'

class WhitePiece(PieceColor):
    def __init__(self):
        self.color = 'white'

#검/흰 클래스 - 폰에 사용 - 흰색이 아래
class WhiteOfPawn(WhitePiece):
    def __init__(self):
        #첫 이동시 두 칸 이동 가능 위해(True/False)
        self.IsFirstMove = True
    
    def move(self, x, y):
        #이 리턴값은 여기를 수정하거나 pawn에서 앞에 말이 있는지를 판별하여
        #이동 가능여부 한번 더 봐줘야함

        #폰은 끝에 도달 시 변화하기에 InsideOfBoard 불필요

        #대각선 앞에 적 있으면 대각선으로 이동하는 것 추가 필요
        if self.IsFirstMove:
            return (x, y+1), (x, y+2)
        else:
            return (x, y+1)
        
class BlackOfPawn(BlackPiece):
    def __init__(self):
        #첫 이동시 두 칸 이동 가능 위해(True/False)
        self.IsFirstMove = True
    
    def move(self, x, y):
        #이 리턴값은 여기를 수정하거나 pawn에서 앞에 말이 있는지를 판별하여
        #이동 가능여부 한번 더 봐줘야함

        #폰은 끝에 도달 시 변화하기에 InsideOfBoard 불필요

        #대각선 앞에 적 있으면 대각선으로 이동하는 것 추가 필요
        if self.IsFirstMove:
            return (x, y-1), (x, y-2)
        #폰은 끝에 도달 시 변화하기에 InsideOfBoard 불필요
        else:
            return (x, y-1)
        


#말 상위 클래스
class Pieces:
    #전체 움직임 횟수 측정(필요 여부 불투명)
    #짝수면 흰말 활성화, 홀수면 검은말 활성화 해서 이용 가능할듯
    total_moves = 0

    #bridge pattern
    def __init__(self, color:PieceColor):
        pass
        '''
        self.color = color
        self.x = None
        self.y = None
        self.tag = None
        self.draw()
        self.ables
        #클릭 -> 테두리 red, 재클릭 -> 취소 위함
        self.switch
        '''

    #움직임 - 움직일 위치 리턴
    def moveables(self):
        pass


class Queen(Pieces):
    #x, y는 좌측 상단의 위치
    def __init__(self, canvas, x, y, color:PieceColor):
        self.color = color
        self.canvas = canvas
        self.x = x
        self.y = y
        #그림들의 tag. outline은 tag+'out'
        self.tag = self.color.color + 'Queen'
        self.Draw_Queen()
        self.ables = None
        self.switch = False

        self.canvas.tag_bind(self.tag, "<Button-1>", self.clickObject)
        self.canvas.tag_bind(self.tag+"out", "<Button-1>", self.clickObject)
        self.canvas.tag_bind(self.tag, "<Button-3>", self.deletion)
        self.canvas.tag_bind(self.tag+"out", "<Button-3>", self.deletion)
        
        
    #크기는 임의로 정함
    def Draw_Queen(self):
        x = self.x
        y = self.y
        size = 10
        tag = self.tag
        self.canvas.create_rectangle(x, y, x+18*size, y+18*size, fill='lightgrey', outline='black', tags=tag+'out')
        self.canvas.create_polygon(x+2*size, y+7*size, x+4*size, y+14*size, x+3*size, y+15*size, x+15*size, y+15*size, x+14*size, y+14*size, x+16*size, y+7*size, x+12*size, y+10*size, x+12*size, y+4*size, x+9*size, y+9*size, x+6*size, y+4*size, x+6*size, y+10*size, fill=self.color.color, outline='black', tags=tag)
        self.canvas.create_oval(x+1*size, y+6*size, x+3*size, y+8*size, fill=self.color.color, outline='black', tags=tag)
        self.canvas.create_oval(x+5*size, y+3*size, x+7*size, y+5*size, fill=self.color.color, outline='black', tags=tag)
        self.canvas.create_oval(x+11*size, y+3*size, x+13*size, y+5*size, fill=self.color.color, outline='black', tags=tag)
        self.canvas.create_oval(x+15*size, y+6*size, x+17*size, y+8*size, fill=self.color.color, outline='black', tags=tag)

    def moveable(self):
        t_x = self.x
        t_y = self.y
        ables = []
        for i in range(-1, 2, 2):
            for k in range(-1, 2, 2):
               m = 1
               while(InsideOfBoard(self.x+m*i, self.y+m*k)):
                    ables.append((self.x+m*i, self.y+m*k))
                    m += 1
        return ables

    #클릭 시
    def clickObject(self, event):
        if self.switch:
            self.canvas.itemconfig(self.tag + "out", outline='black')
        else:    
            self.canvas.itemconfig(self.tag + "out", outline='red')
            self.ables = self.moveable()
            print(self.ables)
        self.switch = not self.switch

    #삭제 - 일단 우클릭과 바인드. 후에 먹힐 때 없애려면 입력에 event 필요 없을 듯
    def deletion(self, event):
        self.canvas.delete(self.tag)
        self.canvas.delete(self.tag+"out")
        del self

    #구현 안 함
    def move(self):
        pass


#사이즈 변경 가능 창은 보류하는 것이 좋을 듯.
#안의 도형들의 크기도 따라 변하게 하려면 꽤나 골치 아파보임
#후에 기능 추가 가능성 생각해서 남겨놓음
'''
#캔버스 1:1 비율 유지
#builder 패턴으로 취급 가능할듯?
class ResizableCanvas:
    def __init__(self, win, width, height):
        self.win = win
        self.width = width
        self.height = height
        self.ratio = width / height
        
        self.canvas = tk.Canvas(win, width = width, height = height, background = 'white')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.win.bind('<Configure>', self.resize_canvas)
    
    def resize_canvas(self, event):
        # 현재 창 크기 가져오기
        curWinWidth = self.win.winfo_width()
        curWinHeight = self.win.winfo_height()

        # 비율 유지하며 크기 조정
        if curWinWidth / self.ratio < curWinHeight:
            new_width = curWinWidth
            new_height = int(curWinWidth / self.ratio)
        else:
            new_height = curWinHeight
            new_width = int(curWinHeight * self.ratio)

        # Canvas 크기 설정
        self.canvas.config(width=new_width, height=new_height)
        self.canvas.place(x=(curWinWidth - new_width) // 2, y=(curWinHeight - new_height) // 2)
'''



win = tk.Tk()
win.title("Chess")
win.option_add("*Fonts", "맑은고딕 25")
win.geometry("800x800")

# ResizableCanvas 인스턴스 생성
canv = tk.Canvas(win, width = 1280, height = 800, background = 'white')
canv.pack(padx = 0, pady = 0)

#====================================================================
#생성 부분
white = WhitePiece()
black = BlackPiece()
q1 = Queen(canv, 5, 5, white)

#현재 x, y 좌표는 0~800인 반면, 보드 밖으로 나갔는지 여부는 0~7로 판별하여
#q2는 이동 가능 위치 미출력됨. 
q2 = Queen(canv, 600, 600, black)
#====================================================================

win.mainloop()
