from tkinter import * 
from tkinter import messagebox # Imports Message Box

def click():
  #messagebox.showinfo(title="This is An Information Message Box", message="You Are So Gay")
  #while(True): #For Infinte Loop
    #messagebox.showwarning(title="This is An Information Message Box", message="You Have A Virus")

  #messagebox.showerror(title="This is An Information Message Box", message="CPU Is Overheating")

    #if messagebox.askokcancel(title="This is An Information Message Box", message="Can You Bounce On It Crazy Style?"): 
        #print("Thanks Pooky")
    #else: 
        #print("What A Bum")
        
  #if messagebox.askretrycancel(title="This is An Information Message Box", message="Do You Want to Retry To Bounce On It Crazy Style?"): 
        #print("Thanks Pookie")
  #else: 
        #print("What A Bum")

  #if messagebox.askyesno(title="Ask Yes Or No", message="Syrupy Footjob?"): 
        #print("Holy Moly")
  #else: 
        #print("Not Even Cool :(") 

  #answer = messagebox.askquestion(title="Ask Question", message="Do you love me?")
  #if(answer=="yes"): 
    #print("I Love You Too")
  #else:
    #print("So You Hate Me Then?")

    answer = messagebox.askyesnocancel(title="Yes No Cancel", message="Do You Want To Go On A Date?")
    if(answer==True): 
        print("You Like Me")
    elif(answer==False): 
        print("You Hate Me?")
    else: 
        print("You Are Actually An Opp")

window = Tk()

button = Button(window, text="Click Me", command=click)
button.pack()

window.mainloop()