from tkinter import * 

count = 0


def click(): 
  global count #Set as global for it to effect everywhere within the window. 
  count += 1 
  print(count)
  print("You Clicked The Button")

window = Tk()

photo = PhotoImage(file=r'C:\Users\firem\Documents\Python\Images\cow.png') #r is used for root pathing files. 

button = Button(window,
               text="Click Me", 
                command=click,
                font=('Comic Sans', 30),
                fg ='#00FF00',
                bg='black',
                activeforeground='#00FF00',
                activebackground='black',
                state=ACTIVE,  #Normally Set As Active, Disabled = Not being able to press on. 
                image=(photo), #Replaces text with an image
                compound=BOTTOM #Allows for both image and text, Direction will be relative to the text. 
                )
button.pack()


window.mainloop()

