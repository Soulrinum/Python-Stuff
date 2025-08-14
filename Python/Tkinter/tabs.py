from tkinter import * 
from tkinter import ttk #Provides access to widgets normally not avalible

window = Tk()

notebook = ttk.Notebook(window) #Widget that manages a colleciton of window/displays

tab1 = Frame(notebook)
tab2 = Frame(notebook)

notebook.add(tab1, text="Tab1")
notebook.add(tab2, text="Tab2")
notebook.pack(expand=True, fill="both") #Allows for the tab to adapt to the size of the window. 

Label(tab1, text="Welcome To Tab 1").pack()
Label(tab2, text="Welcome To Tab 2").pack()


window.mainloop() 