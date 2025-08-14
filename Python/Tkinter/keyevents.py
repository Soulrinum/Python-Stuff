from tkinter import * 

def doSomething(event): 
  print("You Pressed", event.keysym)

window = Tk()

window.bind("<Key>", doSomething) #You Have to use <Key> or nothing will appear.

window.mainloop()