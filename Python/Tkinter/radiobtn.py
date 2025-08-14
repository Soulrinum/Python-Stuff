from tkinter import *

food = ["Pizza", "Hamburger", "Hotdog"]

def order():
  if (x.get()==0): 
    print("You Orderd Pizza")
  elif(x.get()==1): 
    print("You Orderd A Hamburger")
  elif(x.get()==2): 
    print("You Orderd A Hotdog")
  else:
    print("You Orderd Nothing")

window = Tk()

x = IntVar()

for index in range(len(food)): #Interate once through all elements within the list 
  radio_button = Radiobutton(window, 
                             text=food[index], 
                             variable=x, #Groups radio buttons together if they share the same variable.
                             value=index, #Assings each radio button a different value which ensures they are not selected all at once. 
                             command=order
                             ) 
  radio_button.pack(anchor=W) #Lines up Radio buttons to the west. 
window.mainloop() 