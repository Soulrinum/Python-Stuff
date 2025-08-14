from tkinter import * 
from tkinter import messagebox

def click():
  answer = messagebox.askyesnocancel(title="Date?", message="Will You Go On A Date With Me?")
  if answer is True:
    messagebox.showinfo(title="Thanks For Agreeing", message="Where Should We Go?")
    window.destroy()

  if answer is False or answer is None: 
    messagebox.showwarning(title="Warning", message="You Have A Virus")
    while True:
      messagebox.askretrycancel("Date?", message="Will You Go On A Date With Me?")
      

window = Tk()

button = Button(window, text="Click Me", command=click)
button.pack()

window.mainloop()