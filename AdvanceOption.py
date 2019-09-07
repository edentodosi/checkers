from Position import Position
from Tkinter import PhotoImage, Button

class AdvanceOption:
    def __init__(self,master,position,onClick):
        self.master=master
        self.position = position
        self.photo = PhotoImage(file="Assets/circle.gif")
        self.UiOption = Button(self.master, image=self.photo, background="white", command=lambda: onClick(position))
        self.UiOption.grid(row=position.Row, column=position.Column)

    def delete(self):
        self.UiOption.destroy()