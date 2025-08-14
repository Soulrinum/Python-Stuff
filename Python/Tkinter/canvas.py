from tkinter import * 

window = Tk()

canvas = Canvas(window, height=500, width=500)
canvas.create_line(0,0,500,500, fill="blue", width=2) #Works with rectangle, polygon, arc.
canvas.pack()

window.mainloop()