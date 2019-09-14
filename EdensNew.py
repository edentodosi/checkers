from Tkinter import Tk, Label, Frame, PhotoImage, Button, Toplevel
from Solider import Solider
from Position import Position
from AdvanceOption import AdvanceOption
from GameMenu import GameMenu
import tkMessageBox

class Board:
    def __init__(self, master):
        master.title("Checkers Game - Eden Todosi")
        self.BoardPixelSize = 600
        self.NumberOfCellsInAxis = 8
        self.master = master
        self.SizeOfCell = (int)(self.BoardPixelSize / self.NumberOfCellsInAxis)
        self.UiAdvancedOptions = []
        self.lastSoliderClicked = None
        self.InAMiddleOfEating=False
        self.someoneWin=False

        self.gameMenu = GameMenu(master, "",0,0, self.ResetGame)

        self.BoardUi = Frame(self.master,borderwidth=2, background="#080808")
        self.BoardUi.place(x=75, y=140)
        self.DrawBackgroundBoard()

        # init the board
        self.BoardState = [[None for i in range(
            self.NumberOfCellsInAxis)] for j in range(self.NumberOfCellsInAxis)]
        self.ResetGame()

    def DrawBackgroundBoard(self):
        self.background = []
        self.whiteBg = PhotoImage(file="Assets/whitebg.gif")
        self.blackBg = PhotoImage(file="Assets/blackbg.gif")

        for i in range(self.NumberOfCellsInAxis):
            for j in range(self.NumberOfCellsInAxis):
                if((i+j) % 2 == 0):
                    whiteBg = Label(
                        self.BoardUi, image=self.whiteBg, borderwidth=0)
                    whiteBg.grid(row=i, column=j)
                    self.background.append(whiteBg)
                else:
                    blackBg = Label(
                        self.BoardUi, image=self.blackBg, borderwidth=0)
                    blackBg.grid(row=i, column=j)
                    self.background.append(blackBg)

    def ResetGame(self):
        for option in self.UiAdvancedOptions:
            option.Delete()
        self.UiAdvancedOptions = []
        self.InAMiddleOfEating=False
        self.someoneWin=False

        for i in range(self.NumberOfCellsInAxis):
            for j in range(self.NumberOfCellsInAxis):
                if(self.BoardState[i][j] is not None):
                    self.BoardState[i][j].Delete()
                    self.BoardState[i][j] = None
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

        self.gameMenu.UpdateBlackSoliderCounter(self.blackPlayersCount)
        self.gameMenu.UpdateWhiteSoliderCounter(self.whitePlayersCount)
        self.gameMenu.UpdatePlayerTurn(self.playerTurn)

    def OnSoliderPressed(self, solider):
        if(self.playerTurn != solider.Color):
            return
        if (self.InAMiddleOfEating):
            if(solider != self.lastSoliderClicked):
                return
        if(self.someoneWin):
            return

        for option in self.UiAdvancedOptions:
            option.Delete()
        self.UiAdvancedOptions = []

        self.lastSoliderClicked = solider
        advancedPositions = self.GetAdvancedPositionsForSolider(solider)
        
        for newPosition in advancedPositions:
            if(self.InAMiddleOfEating):
                if(abs(newPosition.Row - self.lastSoliderClicked.Position.Row) == 2):
                    self.UiAdvancedOptions.append(AdvanceOption(self.BoardUi, newPosition, self.OnPositionOptionPress))
            else:
                self.UiAdvancedOptions.append(AdvanceOption(self.BoardUi, newPosition, self.OnPositionOptionPress))

    def GetAdvancedPositionsForSolider(self, solider):
        advancedPositions = []
        if(solider.Color == "white" or solider.IsKing):
            rightOption = self.GetAdvancePositionForSpecificDirection(
                solider, -1, 1)
            if(rightOption is not None):
                advancedPositions.append(rightOption)
            leftOption = self.GetAdvancePositionForSpecificDirection(
                solider, -1, -1)
            if(leftOption is not None):
                advancedPositions.append(leftOption)

        if(solider.Color == "black" or solider.IsKing):
            rightOption = self.GetAdvancePositionForSpecificDirection(
                solider, 1, 1)
            if(rightOption is not None):
                advancedPositions.append(rightOption)
            leftOption = self.GetAdvancePositionForSpecificDirection(
                solider, 1, -1)
            if(leftOption is not None):
                advancedPositions.append(leftOption)

        return advancedPositions

    def GetAdvancePositionForSpecificDirection(self, solider, verticalDirection, horizontalDirection):
        try:
            if(solider.Position.Row+verticalDirection < 0 or solider.Position.Column+horizontalDirection < 0):
                return None
            if(self.BoardState[solider.Position.Row+verticalDirection][solider.Position.Column+horizontalDirection] == None):
                return Position(solider.Position.Row+verticalDirection, solider.Position.Column+horizontalDirection)
            
            if(solider.Position.Row+2*verticalDirection < 0 or solider.Position.Column+2*horizontalDirection < 0):
                return None

            if(solider.color != self.BoardState[solider.Position.Row+verticalDirection][solider.Position.Column+horizontalDirection].Color):
                if(self.BoardState[solider.Position.Row+verticalDirection*2][solider.Position.Column+2*horizontalDirection] == None):
                    return Position(solider.Position.Row+verticalDirection*2, solider.Position.Column+2*horizontalDirection)
        except IndexError:
            return None

    def CheckIfNotMovesLeft(self):
        for i in range(self.NumberOfCellsInAxis):
            for j in range(self.NumberOfCellsInAxis):
                if(self.BoardState[i][j] is not None):
                    if(self.BoardState[i][j].Color== self.playerTurn):
                        advancedOptions = self.GetAdvancedPositionsForSolider(
                            self.BoardState[i][j])
                        if(len(advancedOptions)!=0):
                            return False
        return True


    def OnPositionOptionPress(self, position):
        for option in self.UiAdvancedOptions:
            option.Delete()
        self.UiAdvancedOptions = []

        previousPosition = self.lastSoliderClicked.Position
        self.BoardState[position.Row][position.Column] = self.lastSoliderClicked
        self.BoardState[previousPosition.Row][previousPosition.Column] = None
        self.lastSoliderClicked.UpdatePosition(position)

        # make someone a king
        if self.lastSoliderClicked.color == "black" and self.lastSoliderClicked.Position.Row == 7:
            self.lastSoliderClicked.MakeAKing()

        if self.lastSoliderClicked.color == "white" and self.lastSoliderClicked.Position.Row == 0:
            self.lastSoliderClicked.MakeAKing()

        # if we ate a solider
        if(abs(previousPosition.Row - position.Row) == 2):
            middlePosition = Position(
                (previousPosition.Row + position.Row)/2, (previousPosition.Column + position.Column)/2)
            self.BoardState[middlePosition.Row][middlePosition.Column].Delete()
            self.BoardState[middlePosition.Row][middlePosition.Column] = None
            if self.playerTurn == "white":
                self.DecrementCounter("black")
            else:
                self.DecrementCounter("white")

            advancedOptions = self.GetAdvancedPositionsForSolider(
                self.lastSoliderClicked)
            for option in advancedOptions:
                # can we eat again ?
                if(abs(option.Row - self.lastSoliderClicked.Position.Row) == 2):
                    self.InAMiddleOfEating=True
                    self.OnSoliderPressed(self.lastSoliderClicked)
                    return
      
        self.playerTurn = "black" if self.playerTurn == "white" else "white"
        self.InAMiddleOfEating=False
      
        if(self.CheckIfNotMovesLeft()):
            self.Winning("black" if self.playerTurn == "white" else "white")
        self.gameMenu.UpdatePlayerTurn(self.playerTurn)

    def DecrementCounter(self,color):
        if( color == "white"):
            self.whitePlayersCount -=1
            self.gameMenu.UpdateWhiteSoliderCounter(self.whitePlayersCount)
            if(self.whitePlayersCount==0):
                self.Winning("black")
        elif (color =="black"):
            self.blackPlayersCount -=1
            self.gameMenu.UpdateBlackSoliderCounter(self.blackPlayersCount)
            if(self.blackPlayersCount==0):
                self.Winning("white")
   
    def Winning(self,color):
        self.someoneWin=True
        window = Toplevel(self.master, background="#f0e5df")
        window.attributes('-topmost', True)
        window.title("we have a winner!")
        window.geometry("300x200")

        message=Label(window, text="The winner is \n" + str(color), background="#f0e5df",font=("Courier", 20))
        message.place(x=150, y= 80, anchor="center")

        resetButton = Button(window, text="Reset Game",command=lambda : 
        (
         (self.ResetGame())
        ,(window.destroy()),
        (self.master.attributes('-topmost', True))
        ),
         height=2, width=15)

        resetButton.place(x=150, y= 160, anchor="center")
        center(window)


def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))

root = Tk()
root.configure(background='#f0e5df')
root.geometry("750x780")
boarda = Board(root)
center(root)
root.mainloop()
# TODO:
# if didnt eat while it can - shouled we remove the one couled eat ?  - or do not allow not eating
# if someone cant move anymore ?