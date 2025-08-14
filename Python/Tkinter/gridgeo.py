from tkinter import * 

def submit(): 
  username = firstNameEntry.get()
  password = lastNameEntry.get()
  Email = EmailEntry.get()
  print(" Welcome ", username, password, Email)
  firstNameEntry.delete(0, END)
  lastNameEntry.delete(0, END)
  EmailEntry.delete(0, END)

window = Tk()

firstNameLable = Label(window, text="First Name:")
firstNameLable.grid(row=0, column=0)
firstNameEntry = Entry(window)
firstNameEntry.grid(row=0, column=1)

lastNameLable = Label(window, text="Last Name:")
lastNameLable.grid(row=1, column=0)
lastNameEntry = Entry(window)
lastNameEntry.grid(row=1, column=1)

EmailLable = Label(window, text="Email:")
EmailLable.grid(row=2, column=0)
EmailEntry = Entry(window)
EmailEntry.grid(row=2, column=1)

sub_btn = Button(window, text="Sumbit Information", command=submit)
sub_btn.grid(row=3, column=0)


window.mainloop()