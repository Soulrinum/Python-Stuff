from tkinter import * 
from tkinter import filedialog

def open(): 
  openfile = filedialog.askopenfilename()
  file = open(openfile, 'r')


def save(): 
  savefile = filedialog.asksaveasfile()

window = Tk()

menubar = Menu(window) 
window.config(menu=menubar)

filemenu = Menu(menubar, tearoff=0) #Adds Filemenu into menu bar rather then window. Tearoff removes lines above lables. 
menubar.add_cascade(label="File Menu", menu=filemenu) #Dropdown Menubar 
filemenu.add_command(label="Open", command=open)
filemenu.add_command(label="Save", command=save)
filemenu.add_separator() #Adds A Seperator. 
filemenu.add_command(label="Exit", command=quit)


window.mainloop()