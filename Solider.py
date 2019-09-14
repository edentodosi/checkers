from Position import Position
from Tkinter import PhotoImage, Button

class Solider:
    def __init__(self, master, color, position, isKing, onClick):
        self.color = color
        self.isKing = isKing
        self.position = position
        self.master = master
        self.onClick = onClick
        self.DrawImage()

    def DrawImage(self):
        pathToFile = "Assets/" + self.color + "_solider"
        if(self.isKing):
            pathToFile = pathToFile + "_king"
        pathToFile = pathToFile + ".gif"
        self.photo = PhotoImage(file=pathToFile)
        self.soliderButton = Button(
            self.master, image=self.photo, background="white", command=lambda: self.onClick(self))
        self.soliderButton.grid(row=self.position.Row, column=self.position.Column)

    def UpdatePosition(self,position):
        self.position = position
        self.soliderButton.grid(row=position.Row, column=position.Column)

    def MakeAKing(self):
        self.isKing=True
        self.Delete()
        self.DrawImage()

    def Delete(self):
        self.photo.__del__()
        self.soliderButton.destroy()

    @property 
    def IsKing(self):
        return self.isKing

    @property
    def Color(self):
        return self.color
    
    @property
    def Position(self):
        return self.position