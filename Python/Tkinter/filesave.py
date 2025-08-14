from tkinter import * 
from tkinter import filedialog 

def Save():
  file = filedialog.asksaveasfile(
    defaultextension='.txt', 
    filetypes=[
      ("Text File", ".txt"),
      ("Png", ".png")
      ])
  if file is None: 
    return

  filetext = str(text.get(1.0, END))
  file.write(filetext)
  file.close()

window = Tk()

text = Text(window)
text.pack()

btn = Button(text="Save Text", command=Save)
btn.pack()

window.mainloop()