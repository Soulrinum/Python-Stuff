from tkinter import * 
from tkinter.ttk import * #Provide widgets not normally found 
import time

def start(): 
  task = 10 
  x = 0 
  while(x<task):
    time.sleep(1)
    bar['value']+=10
    x += 1
    window.update_idletasks() #Updates the window

window = Tk()

bar = Progressbar(window, orient=HORIZONTAL, length=300)
bar.pack(pady=10)

button = Button(window, text="Download", command=start)
button.pack()

window.mainloop()