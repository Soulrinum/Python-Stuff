from tkinter import * 

def submit(): 
  print(" The Tempreature is "+ str(scale.get())+ " Degrees Celcius ")

window = Tk()

scale = Scale(window, 
              from_=100, 
              to = 0,
              length=600,
              orient=HORIZONTAL,
              tickinterval=10
              )
scale.pack()

button = Button(window, text="Submit", command=submit).pack()

window.mainloop()