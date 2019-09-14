from Tkinter import Label, Button

class GameMenu:
    def __init__(self, master,playerTurn, blackSoliderCount, whiteSoilderCount, resetGame):
        self.whitePlayerCount = Label(master, text="White Solider: " + str(whiteSoilderCount))
        self.blackPlayerCount = Label(master, text="Black Solider: " + str(whiteSoilderCount))
        self.currentPlayerTurn = Label(master, text="Current Player: " + str(playerTurn))

        self.whitePlayerCount.pack()
        self.blackPlayerCount.pack()
        self.currentPlayerTurn.pack()
        self.resetButton = Button(master, text="Reset Game",command=resetGame, height=2, width=15)
        self.resetButton.pack()

    
    def UpdateBlackSoliderCounter(self, numOfSoliders):
        self.blackPlayerCount['text'] = "Black Solider: " + str(numOfSoliders)

    def UpdateWhiteSoliderCounter(self, numOfSoliders):
        self.whitePlayerCount['text'] = "White Solider: " + str(numOfSoliders)
    
    def UpdatePlayerTurn(self, currentPlayer):
        self.currentPlayerTurn['text'] = "Current Player: " + str(currentPlayer)