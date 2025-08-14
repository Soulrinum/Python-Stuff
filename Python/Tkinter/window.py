from tkinter import * 

def newwindow(): 
  new_window = Toplevel() #Top Level = new window "On Top" of of other windows. Linkd to a "Bottom Window"/Original Window it came from.
  Button(new_window, text="Create New Window", command=newwindow).pack()


window = Tk()

Button(window, text="Create New Window", command=newwindow).pack()

window.mainloop()