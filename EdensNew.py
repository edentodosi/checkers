from Tkinter import Tk,Label,Frame, PhotoImage,Button
from Solider import Solider
from Position import Position
from AdvanceOption import AdvanceOption
import tkMessageBox
#https://www.tocode.co.il/blog/2015-07-tkinter-intro
# https://python-textbok.readthedocs.io/en/1.0/Introduction_to_GUI_Programming.html
#from PIL import Image

# class Board:
#     def __init__(self):


# class Position:
class Board:
    def __init__(self, master):
        master.title("Checkers Game - Eden Todosi")
        #current_turn_text = "{}{}".format(self.playerTurn, "\'s Turn!")
        #self._turn_indicator_label.config(text = current_turn_text)
        reset = Button(master, text = "Reset Game", command =self.ResetGame, height=2, width=15)
        reset.pack()
        self.BoardPixelSize = 600
        self.NumberOfCellsInAxis = 8
        self.master = master
        self.SizeOfCell = (int)(self.BoardPixelSize / self.NumberOfCellsInAxis)
        self.UiAdvancedOptions = []
        # init the board
        self.BoardState = [[Solider for i in range(
            self.NumberOfCellsInAxis)] for j in range(self.NumberOfCellsInAxis)]

        self.BoardUi = Frame(self.master)
        self.BoardUi.pack()
        self.whiteBg = PhotoImage(file="Assets/whitebg.gif")
        self.blackBg = PhotoImage(file="Assets/blackbg.gif")
        self.background = []
        for i in range(self.NumberOfCellsInAxis):
            for j in range(self.NumberOfCellsInAxis):
                if((i+j) % 2 == 0):
                    whiteBg = Label(self.BoardUi, image=self.whiteBg, borderwidth=0)
                    whiteBg.grid(row=i, column=j)
                    self.background.append(whiteBg)
                else:
                    blackBg = Label(self.BoardUi, image=self.blackBg, borderwidth=0)
                    blackBg.grid(row=i, column=j)
                    self.background.append(blackBg)
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

        for option in self.UiAdvancedOptions:
            option.delete()

        self.lastSoliderClicked=solider
        advancedPositions=self.GetAdvancedPositionsForSolider(solider)
        for newPosition in advancedPositions:
            self.UiAdvancedOptions.append(AdvanceOption(self.BoardUi, newPosition, self.OnPositionOptionPress))

    def GetAdvancedPositionsForSolider(self, solider):
        advancedPositions=[]
        if(solider.Color == "white" or solider.IsKing):
            rightOption = self.GetAdvancePositionForSpecificDirection(solider, -1, 1)
            if(rightOption is not None):
                advancedPositions.append(rightOption)
            leftOption = self.GetAdvancePositionForSpecificDirection(solider, -1, -1)
            if(leftOption is not None):
                advancedPositions.append(leftOption)
        
        if(solider.Color == "black" or solider.IsKing):
            rightOption = self.GetAdvancePositionForSpecificDirection(solider, 1, 1)
            if(rightOption is not None):
                advancedPositions.append(rightOption)
            leftOption = self.GetAdvancePositionForSpecificDirection(solider, 1, -1)
            if(leftOption is not None):
                advancedPositions.append(leftOption)

        return advancedPositions
    
    def GetAdvancePositionForSpecificDirection(self,solider, verticalDirection, horizontalDirection):
        try:
            if(self.BoardState[solider.Position.Row+verticalDirection][solider.Position.Column+horizontalDirection]== None):
                return Position(solider.Position.Row+verticalDirection,solider.Position.Column+horizontalDirection)

            elif (solider.color!=self.BoardState[solider.Position.Row+verticalDirection][solider.Position.Column+horizontalDirection].Color):
                if(self.BoardState[solider.Position.Row+verticalDirection*2][solider.Position.Column+2*horizontalDirection] == None):
                    return Position(solider.Position.Row+verticalDirection*2,solider.Position.Column+2*horizontalDirection)
        except IndexError:
            return None

    def OnPositionOptionPress(self,position):
        for option in self.UiAdvancedOptions:
            option.delete()

        previousPosition=self.lastSoliderClicked.Position
        self.BoardState[position.Row][position.Column] = self.lastSoliderClicked
        self.BoardState[previousPosition.Row][previousPosition.Column]= None
        self.lastSoliderClicked.UpdatePosition(position)
        
        #make someone a king 
        if self.lastSoliderClicked.color=="black" and self.lastSoliderClicked.Position.Row==7:
            self.lastSoliderClicked.MakeAKing()
        
        if self.lastSoliderClicked.color=="white" and self.lastSoliderClicked.Position.Row==0:
            self.lastSoliderClicked.MakeAKing()
        
        #if we ate a solider
        if(abs(previousPosition.Row - position.Row) == 2):
            middlePosition = Position((previousPosition.Row + position.Row)/2,(previousPosition.Column + position.Column)/2)
            self.BoardState[middlePosition.Row][middlePosition.Column].Delete()
            self.BoardState[middlePosition.Row][middlePosition.Column] = None
            if self.playerTurn == "white":
                self.blackPlayersCount -=1
            else :
                self.whitePlayersCount -=1
            advancedOptions = self.GetAdvancedPositionsForSolider(self.lastSoliderClicked)
            for option in advancedOptions:
                if(abs(option.Row - self.lastSoliderClicked.Position.Row) == 2):
                    self.OnSoliderPressed(self.lastSoliderClicked)
                    return

        self.playerTurn = "black" if self.playerTurn == "white" else "white"


root = Tk()
root.configure(background='white')
root.geometry("700x700")
boarda = Board(root)
root.mainloop()
#TODO:
# after eat - can we eat again?
# check if won - (number of soliders is 0 ?  ) after each move
# if didnt eat while it can - shouled we remove the one couled eat ?  - or do not allow not eating 
# if someone cant move anymore ? 
# menu that contains player turn, count of soliders, and restart button
# fix the negative index on array