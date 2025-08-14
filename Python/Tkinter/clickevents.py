from tkinter import *

def doSomething(event): 
  print("Mouse Coords:" + str(event.x) + "," + str(event.y))

window = Tk()

window.bind("<Button-1>", doSomething)

window.mainloop()