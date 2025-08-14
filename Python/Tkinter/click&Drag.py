from tkinter import *

def drag_start(event): 
  widget = event.widget #Adding this line of code solves the issue completely. 
  widget.startX = event.x
  widget.startY = event.y 

def drag_motion(event): 
  widget = event.widget 
  x = widget.winfo_x() - widget.startX + event.x #Gets top left x coordinates of the label relative to the window. 
  y = widget.winfo_y() - widget.startY + event.y #Gets top Right x coordinates of the label relative to the window. 
  widget.place(x=x,y=y)

#Current functions won't be compataible with more than one widget. 

window = Tk()

lable = Label(window, bg="green", width=10, height=5)
lable.place(x=0, y=0)

lable.bind("<Button-1>", drag_start) #Button 1 Would be the event in this case while drag_start is the command. 
lable.bind("<B1-Motion>", drag_motion) 

lable1 = Label(window, bg="blue", width=10, height=5)
lable1.place(x=100, y=100)

lable1.bind("<Button-1>", drag_start) #Button 1 Would be the event in this case while drag_start is the command. 
lable1.bind("<B1-Motion>", drag_motion) 

window.mainloop()