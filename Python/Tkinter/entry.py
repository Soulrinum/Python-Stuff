from tkinter import *

def submit():
    username = entry.get()
    print("Hello " + username)

def delete(): 
    entry.delete(0, END) #Delete all the characters from indexed 0 to the end.

def back_space(): 
    entry.delete(len(entry.get())-1, END)

window = Tk()

entry = Entry(
    window, 
    font=("Arial", 40),
    show = "*" #Replaces typed text for the symbol, perfect for passwords.
    
    )
entry.pack(side=LEFT)

submit_button = Button(window, text="Submit", command=submit)
submit_button.pack(side=RIGHT)

delete_button = Button(window, text="Delete", command=delete)
delete_button.pack(side=RIGHT)

back_space = Button(window, text="Backspace", command=back_space)
back_space.pack(side=RIGHT)

window.mainloop()


