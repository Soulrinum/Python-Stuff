from tkinter import * 

window = Tk()

frame = Frame(window)
frame.pack()

Button(frame,text="W").pack(side=TOP)
Button(frame,text="A").pack(side=LEFT)
Button(frame,text="S").pack(side=LEFT)
Button(frame,text="D").pack(side=LEFT)

window.mainloop()