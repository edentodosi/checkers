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
        pathToFile = pathToFile + ".png"
        self.photo = PhotoImage(file=pathToFile)
        self.soliderButton = Button(
            self.master, image=self.photo, background="#EBC595", command=lambda: onClick(self.position))
        self.soliderButton.grid(row=position.Row, column=position.Column)
