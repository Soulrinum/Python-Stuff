from tkinter import *
from tkinter import colorchooser #Imports Colour Chooser. 

def click():
 colour = colorchooser.askcolor()
 colorHex = colour[1]
 window.config(bg=colorHex)
 print(colorHex)


window = Tk()

window.geometry("420x330")

button = Button(text="Click Me", command=click)
button.pack()

window.mainloop()