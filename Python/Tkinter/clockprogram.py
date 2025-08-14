from tkinter import * 
from time import * 

def update(): 
  time_string = strftime("%I" ":" "%M" ":" "%S" ":" "%p") #Where %I = 12 Hour Time as a decimal number(01 - 12), %M = Minute as a decimal number (00 - 59) And %S Second as a decimal Number (00 - 61)
  time_label.config(text=time_string)
  time_label.after(1000,update)
window = Tk()

time_label = Label(window, font=("Arial", 50), fg="pink", bg="gray")
time_label.pack()

update()

window.mainloop()
