from tkinter import * 

window = Tk()
window.geometry("330x440") 
window.title("Window GUI")

icon = PhotoImage(file=r'C:\Users\firem\Documents\Python\Images\cow.png') # Use = r for root pathing to files outside of the script directory. 
window.iconphoto(True, icon)
window.config(bg="lightblue") # Sets background color of the window. You can also use hex values like "#00FF00" for green.. 

window.mainloop() 