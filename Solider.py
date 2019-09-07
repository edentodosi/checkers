from Position import Position
from Tkinter import PhotoImage, Button


class Solider:
    def __init__(self, master, color, position, isKing, onClick):
        self.color = color
        self.isKing = isKing
        self.position = position
        self.master = master

        pathToFile = "Assets/" + color + "_solider"
        if(self.isKing):
            pathToFile = pathToFile + "_king"
        pathToFile = pathToFile + ".gif"
        self.photo = PhotoImage(file=pathToFile)
        self.soliderButton = Button(
            self.master, image=self.photo, background="white", command=lambda: onClick(self))
        self.soliderButton.grid(row=position.Row, column=position.Column)

    @property
    def Color(self):
        return self.color
    
    @property
    def Position(self):
        return self.position