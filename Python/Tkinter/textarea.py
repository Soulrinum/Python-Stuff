from tkinter import * 

def click(): 
  input = text.get("1.0", END)
  print(input)

window = Tk()

text = Text(window)
text.pack()

button = Button(window, text="Click Me", command=click)
button.pack()


window.mainloop()