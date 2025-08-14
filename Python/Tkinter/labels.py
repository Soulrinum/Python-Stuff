from tkinter import * 

window = Tk()

photo = PhotoImage(file=r'C:\Users\firem\Documents\Python\Images\cow.png')
label = Label(window, 
              text="Hello World", 
              font=('Arial', 40, 'bold'), 
              fg='#00F000', 
              bg='black', 
              image=photo,
              compound=BOTTOM
              )
label.pack()

window.mainloop()



