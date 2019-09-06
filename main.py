from Tkinter import *
from PIL import Image


class MyFirstGUI:
    def __init__(self, master):
        self.master = master

        master.title("Checkers, by Eden Todosi")

        screenWidth = root.winfo_screenwidth()
        screenHeight = root.winfo_screenheight()

        menuHeight = screenHeight*0.1
        menuWidth = screenWidth*0.9

        boradHeight = 600
        boradWidth = 600

        self.gameMenu = GameMenu(master, menuWidth, menuHeight)
        self.gameBoard = GameBoard()
        self.gameBoardUi = GameBoardUi(master, min(
            boradWidth, boradHeight), self.gameBoard)

        self.greet_button = Button(master, text="Greet", command=self.greet)
        self.greet_button.pack()
        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    def greet(self):
        print("Greetings!")


class GameMenu:
    def __init__(self, master, width, height):
        self.master = master
        self.label = Label(master, text="Menu")
        self.label.pack()


class GameBoardUi:
    def __init__(self, master, size, board):
        self.board = board
        self.master = master
        self.size = size
        self.lastClicked = None
        self.optionsUi = []
        # main frame set
        soliderSize = (int)(((size / board.BoardSize) * 0.85))
        self.ResizeImagesToMatchScreenSize(size, board.BoardSize, soliderSize)
        self.boardPhoto = PhotoImage(file="Assets/board.gif")
        label = Label(master, image=self.boardPhoto,
                      width=size, height=size)
        label.pack()
        self.mainFrame = label

        # set board
        cellSize = (int)(size/board.BoardSize)
        for i in range(board.BoardSize):
            self.mainFrame.columnconfigure(i, minsize=cellSize)
            self.mainFrame.rowconfigure(i, minsize=cellSize)

        self.uiGameBoard = [[CheckersSoliderUi for i in range(
            board.BoardSize)] for j in range(board.BoardSize)]

        for i in range(board.BoardSize):
            for j in range(board.BoardSize):
                self.uiGameBoard[i][j] = CheckersSoliderUi(
                    label, board.getSoliderAtPosition(i, j), soliderSize, self.onSoliderClicked)

    def ResizeImagesToMatchScreenSize(self, boardPixelSize, boardNumOfCells, soliderPixelSize):
        boardImage = Image.open("Assets/geniune_board.png")
        boardImage = boardImage.resize(
            (boardPixelSize, boardPixelSize), Image.ANTIALIAS)
        boardImage.save("Assets/board.png")

        allSoliderImages = ["geniune_black_solider_king.png", "geniune_black_solider.png",
                            "geniune_white_solider_king.png", "geniune_white_solider.png", "geniune_circle.png"]
        for imageName in allSoliderImages:
            image = Image.open("Assets/" + imageName)
            image = image.resize(
                (soliderPixelSize, soliderPixelSize), Image.ANTIALIAS)
            image.save("Assets/" + imageName.replace("geniune_", ""))

    def onSoliderClicked(self, checkersSolider):
        for optionUi in self.optionsUi:
            optionUi.remove()

        if checkersSolider.soliderColor != self.board.currentPlayerTurn:
            self.lastClicked = None
            return []

        self.lastClicked = checkersSolider
        allOptions = self.board.getAdvancedOptionsForSolider(checkersSolider)

        for option in allOptions:
            self.optionsUi.append(AdvancedOption(
                self.mainFrame, option, self.onPositionClicked))

    def onPositionClicked(self, position):
        geniuneRow = self.lastClicked.rowPosition
        geniuneCol = self.lastClicked.columnPosition
        lastClickedUi = self.uiGameBoard[geniuneRow][geniuneCol]
        self.uiGameBoard[geniuneRow][geniuneCol] = None
        self.board.moveSolider(self.lastClicked, position)
        for optionUi in self.optionsUi:
            optionUi.remove()
        
        self.lastClicked = None
        
        self.uiGameBoard[position.row][position.col] = lastClickedUi
        lastClickedUi.updatePosition()


class AdvancedOption:
    def __init__(self, master, position, onClick):
        self.optionImage = PhotoImage(file="Assets/circle.png")
        self.soliderPhoto = Button(master, image=self.optionImage,
                                   background="#EAC593", command=lambda: onClick(position))
        self.soliderPhoto.grid(column=position.col,
                               row=position.row)

    def remove(self):
        self.optionImage.__del__()
        self.soliderPhoto.destroy()


class GameBoard:
    def __init__(self):
        BOARD_SIZE = 8
        self.board = [[CheckersSolider for i in range(
            BOARD_SIZE)] for j in range(BOARD_SIZE)]
        self.redSolidersAlive = 12
        self.whiteSolidersAlive = 12
        self.currentPlayerTurn = "white"
        self.is_game_over = False

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if (i+j) % 2 == 0:
                    if i < 3:
                        self.board[i][j] = CheckersSolider("black", i, j)
                    elif i >= BOARD_SIZE - 3:
                        self.board[i][j] = CheckersSolider("white", i, j)
                    else:
                        self.board[i][j] = None
                else:
                    self.board[i][j] = None

    @property
    def BoardSize(self):
        return 8

    def getSoliderAtPosition(self, rowPosition, culPosition):
        if rowPosition >= self.BoardSize or culPosition >= self.BoardSize or culPosition < 0 or rowPosition < 0:
            raise ValueError()
        return self.board[rowPosition][culPosition]

    @property
    def currentPlayerTurn(self):
        return self.currentPlayerTurn

    def getAdvancedOptionsForSolider(self, checkersSolider):
        options = []

        #black is attacking down
        downRightOption = None
        downLeftOption = None
        if(checkersSolider.soliderColor == "black" or checkersSolider.isKing):
            downRightOption = self.getStepOptions(1, 1, checkersSolider)
            downLeftOption = self.getStepOptions(1, -1, checkersSolider)

        #white is attacking up
        upRightOption = None
        upLeftOption = None
        if(checkersSolider.soliderColor == "white" or checkersSolider.isKing):
            upRightOption = self.getStepOptions(-1, 1, checkersSolider)
            upLeftOption = self.getStepOptions(-1, -1, checkersSolider)

        if downRightOption is not None:
            options.append(downRightOption)

        if downLeftOption is not None:
            options.append(downLeftOption)

        if upRightOption is not None:
            options.append(upRightOption)

        if upLeftOption is not None:
            options.append(upLeftOption)

        return options

    def getStepOptions(self, verticalDirecton, horizontalDirection, checkersSolider):
        try:
            oneStepDirecitons = self.getSoliderAtPosition(
                checkersSolider.rowPosition + verticalDirecton, checkersSolider.columnPosition + horizontalDirection)
            if oneStepDirecitons is None:
                return Position(checkersSolider.rowPosition + verticalDirecton, checkersSolider.columnPosition + horizontalDirection)
            elif oneStepDirecitons.soliderColor != checkersSolider.soliderColor:
                twoStepsDirection = self.getSoliderAtPosition(
                    checkersSolider.rowPosition + 2*verticalDirecton, checkersSolider.columnPosition + 2*horizontalDirection)
                if twoStepsDirection is None:
                    return Position(checkersSolider.rowPosition + 2*verticalDirecton,
                                    checkersSolider.columnPosition + 2*horizontalDirection)

        except ValueError:
            print("doesnt exist")
            return None
            # ignore

    def moveSolider(self, solider, position):
        self.board[solider.rowPosition][solider.columnPosition] = None
        solider.setPosition(position)
        self.board[position.row][position.col] = solider

        self.currentPlayerTurn = "white" if self.currentPlayerTurn == "black" else "black"
        

class Position:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    @property
    def row(self):
        return self.row

    @property
    def col(self):
        return self.col


class CheckersSoliderUi:
    def __init__(self, master, checkersSolider, size, onClick):
        self.checkersSolider = checkersSolider
        if(checkersSolider is None):
            return

        extension = "_solider_king.gif" if checkersSolider.isKing else "_solider.gif"
        fileName = checkersSolider.soliderColor + extension

        self.soliderImage = PhotoImage(file="Assets/" + fileName)
        self.soliderPhoto = Button(master, image=self.soliderImage, width=size, height=size,
                                   background="#EAC593", command=lambda: onClick(checkersSolider))
        self.soliderPhoto.grid(column=checkersSolider.columnPosition,
                               row=checkersSolider.rowPosition)

    @property
    def Solider(self):
        return self.checkersSolider

    def updatePosition(self):
        self.soliderPhoto.grid(
            column=self.checkersSolider.columnPosition, row=self.checkersSolider.rowPosition)


class CheckersSolider:
    row = 0
    cul = 0
    color = ""

    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col
        self.isKing = False

    @property
    def rowPosition(self):
        return self.row

    @property
    def columnPosition(self):
        return self.col

    @property
    def isKing(self):
        return self.isKing

    @property
    def soliderColor(self):
        return self.color

    def setPosition(self, position):
        self.row = position.row
        self.col = position.col


root = Tk()
root.configure(background='black')
my_gui = MyFirstGUI(root)
root.mainloop()
