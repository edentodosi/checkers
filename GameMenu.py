from Tkinter import Label, Button, Frame

class GameMenu:
    def __init__(self, master,playerTurn, blackSoliderCount, whiteSoilderCount, resetGame):
        
        self.resetButton = Button(master, text="Reset Game",command=resetGame, pady=8,relief="groove",background="#f0e5df")
        self.resetButton.pack(fill="x")

        self.contianerFrame = Frame(master)
        self.contianerFrame.pack(fill="x")

        self.whitePlayerCount = Label(self.contianerFrame, text="White Solider: " + str(whiteSoilderCount), background="white", pady=8, width=53,relief="groove")
        self.blackPlayerCount = Label(self.contianerFrame, text="Black Solider: " + str(whiteSoilderCount), background="black", pady=8, fg="white", width=53,relief="groove")
        self.currentPlayerTurn = Label(self.contianerFrame, text="Current Player: " + str(playerTurn), pady=8, relief="groove")
        
        self.currentPlayerTurn.pack(fill="x")

        self.whitePlayerCount.pack(side="left", fill ="x")
        self.blackPlayerCount.pack(side="right", fill="x")

    
    def UpdateBlackSoliderCounter(self, numOfSoliders):
        self.blackPlayerCount['text'] = "Black Solider: " + str(numOfSoliders)

    def UpdateWhiteSoliderCounter(self, numOfSoliders):
        self.whitePlayerCount['text'] = "White Solider: " + str(numOfSoliders)
    
    def UpdatePlayerTurn(self, currentPlayer):
        self.currentPlayerTurn['text'] = "Current Player: " + str(currentPlayer)
        self.currentPlayerTurn['background'] = currentPlayer
        self.currentPlayerTurn['fg'] = "black" if currentPlayer == "white" else "white"

