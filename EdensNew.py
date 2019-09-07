from Tkinter import *
from Solider import Solider
from Position import Position
from AdvanceOption import AdvanceOption
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

        self.boardPhoto = PhotoImage(file="Assets/board.gif")
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
        self.whitePlayersCount = 12
        self.blackPlayersCount = 12

    def OnSoliderPressed(self, solider):
        if(self.playerTurn != solider.Color):
            return

        self.lastSoliderClicked=solider
        advancedPositions=self.GetAdvancedPositionsForSolider(solider)
        self.UiOptions=AdvanceOption(self.BoardUi,advancedPositions, self.OnPositionOptionPress)

    def GetAdvancedPositionsForSolider(self, solider):
        direction=1
        if(solider.Color=="white"):
            direction=-1
        advancedPositions=[]
        #if we cant eat
        if(solider.Position.Column==0):
            if(self.BoardState[solider.Position.Row+direction][solider.Position.Column+1]==None):
                advancedPositions.append(Position(solider.Position.Row+direction,solider.Position.Column+1))
            elif(solider.color!=self.BoardState[solider.Position.Row+direction][solider.Position.Column+1].Color):
                advancedPositions.append(Position(solider.Position.Row+direction*2,solider.Position.Column+2))
        elif(solider.Position.Column==7):
            if(self.BoardState[solider.Position.Row+direction][solider.Position.Column-1]==None):
                advancedPositions.append(Position(solider.Position.Row+direction,solider.Position.Column-1))
            elif(solider.color!=self.BoardState[solider.Position.Row+direction][solider.Position.Column-1].Color):
                advancedPositions.append(Position(solider.Position.Row+direction*2,solider.Position.Column-2))
        elif(self.BoardState[solider.Position.Row+direction][solider.Position.Column-1]==None):
            advancedPositions.append(Position(solider.Position.Row+direction,solider.Position.Column-1))
            if(self.BoardState[solider.Position.Row+direction][solider.Position.Column+1]==None):
                advancedPositions.append(Position(solider.Position.Row+direction,solider.Position.Column+1))
        #if we can eat
        elif (solider.color!=self.BoardState[solider.Position.Row+direction][solider.Position.Column-1].Color):
            advancedPositions.append(Position(solider.Position.Row+direction*2,solider.Position.Column-2))
        elif (solider.color!=self.BoardState[solider.Position.Row+direction][solider.Position.Column+1].Color):
            advancedPositions.append(Position(solider.Position.Row+direction*2,solider.Position.Column+2))
       
        return advancedPositions
        
    def OnPositionOptionPress(self,position):
        previousPosition=self.lastSoliderClicked.Position
        self.BoardState[position.Row][position.Column] = self.lastSoliderClicked
        self.BoardState[previousPosition.Row][previousPosition.Column]=None
        self.UiOptions.delete()
        


    

root = Tk()
root.configure(background='white')
root.geometry("600x600")
boarda = Board(root)
root.mainloop()
