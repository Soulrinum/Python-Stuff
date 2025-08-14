from tkinter import *

def submit(): 
  order = listbox.get(listbox.curselection())
  print(" You Have Orderd A: " + order)


def newitem(): 
  new = listbox.insert(listbox.size(), entrybox.get())


def delete(): 
  selected_index = listbox.curselection()
  listbox.delete(selected_index)
  print("You Have Successfully Deleted This Menu Item")

window = Tk()

listbox = Listbox(window)
listbox.pack()

listbox.insert(1, "Pizza")
listbox.insert(2, "Hamburger")
listbox.insert(3, "Hotdog")
listbox.insert(4, "Cheese Sticks")
listbox.insert(5, "Onion Rings")

submitButton = Button(window, text="Submit", command=submit)
submitButton.pack()

entrybox = Entry(window)
entrybox.pack()

addButton = Button(window, text="Add", command=newitem)
addButton.pack()

delbutton = Button(window, text="Delete Item From Menu", command=delete)
delbutton.pack()

window.mainloop()