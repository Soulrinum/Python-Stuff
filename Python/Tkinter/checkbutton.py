from tkinter import * 

def display(): 
  if (x.get()==1):
    print("You Have Agreed")
  else:
    print("You Have not agreed")

window = Tk()

x = IntVar()
#x = StringVar(), To Return as a string

check_button = Checkbutton(window, 
                           text="I Agree To The Statement", #Checkbuttons store a 1 or 0 by default within the variable in this case x 
                           variable=x,
                           onvalue=1, #If you want to change value form int to bool (True, False), you would use x = Booleanvar()
                           offvalue=0,
                           command=display
                           ) 

check_button.pack()

window.mainloop()