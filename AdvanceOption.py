from Position import Position
from Tkinter import PhotoImage, Button

class AdvanceOption:
    def __init__(self,master,advancedPositions,onClick):
        self.master=master
        self.advancedPositions=advancedPositions
        self.photo = PhotoImage(file="Assets/circle.gif")
        self.uiOptions = []
        for positionOption in advancedPositions:
            newUiOption = Button(self.master, image=self.photo, background="white", command=lambda: onClick(positionOption))
            newUiOption.grid(row=positionOption.Row, column=positionOption.Column)
            self.uiOptions.append(newUiOption)

    def delete(self):
        for positionOption in self.uiOptions:
            positionOption.destroy()