from Position import Position
from Tkinter import PhotoImage, Button

class AdvanceOption:
    def __init__(self,master,advancedPositions):
        self.master=master
        self.advancedPositions=advancedPositions
        self.photo = PhotoImage(file="Assets/circle.gif")
        self.uiOptions = []
        for positionOption in advancedPositions:
            newUiOption = Button(self.master, image=self.photo, background="#EBC595")#, command=lambda: onClick(self))
            newUiOption.grid(row=positionOption.Row, column=positionOption.Column)
            self.uiOptions.append(newUiOption)    