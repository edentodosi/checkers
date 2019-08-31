from Tkinter import *
from Solider import Solider
from Position import Position
# https://python-textbok.readthedocs.io/en/1.0/Introduction_to_GUI_Programming.html
#from PIL import Image

# class Board:
#     def __init__(self):


# class Position:
class Board:
    def __init__(self, master):
        self.BoardPixelSize = 600
        self.NumberOfCellsInAxis = 8
        self.master = master
        self.SizeOfCell = (int)(self.BoardPixelSize / self.NumberOfCellsInAxis)

        # init the board
        self.BoardState = [[Solider for i in range(
            self.NumberOfCellsInAxis)] for j in range(self.NumberOfCellsInAxis)]

        self.boardPhoto = PhotoImage(file="Assets/board.png")
        self.BoardUi = Label(master, image=self.boardPhoto,
                             width=self.BoardPixelSize, height=self.BoardPixelSize)
        self.BoardUi.pack()

        for i in range(self.NumberOfCellsInAxis):
            self.BoardUi.columnconfigure(i, minsize=self.SizeOfCell)
            self.BoardUi.rowconfigure(i, minsize=self.SizeOfCell)

        self.ResetGame()

    def ResetGame(self):
        for i in range(self.NumberOfCellsInAxis):
            for j in range(self.NumberOfCellsInAxis):
                if((i+j) % 2 == 0):
                    if(i < 3):
                        self.BoardState[i][j] = Solider(
                            self.BoardUi, "black", Position(i, j), False, self.OnSoliderPressed)
                    elif (i > 4):
                        self.BoardState[i][j] = Solider(
                            self.BoardUi, "white", Position(i, j), False, self.OnSoliderPressed)
                    else:
                        self.BoardState[i][j] = None
                else:
                    self.BoardState[i][j] = None

        self.playerTurn = "white"
        self.whitePlayersCount = 13
        self.blackPlayersCount = 13

    def OnSoliderPressed(self, position):
        if(self.playerTurn == self.BoardState[position.Row][position.Column].Color):
            print("this is an ok press")
        else:
            print("Error - invalid press")


root = Tk()
root.configure(background='white')
root.geometry("600x600")
boarda = Board(root)
root.mainloop()
