from tkinter import * 
from tkinter import filedialog

def openFile(): 
  filepath = filedialog.askopenfilename()
  file = open(filepath, 'r') #Default is normally rt for read text, r = read and rb = Read Binary. 
  print(file.read()) 
  file.close

window = Tk()

button = Button(text="Open File", command=openFile)
button.pack()

window.mainloop()