from tkinter import * 
import time 

WIDTH = 500 
HEIGHT = 500
xVelocity = 1 
yVelocity = 1

window = Tk()

canvas = Canvas(window, width=WIDTH, height=HEIGHT)
canvas.pack()

photo_image = PhotoImage(file=r"C:\Users\firem\Documents\Python\Images\cow.png")
my_image = canvas.create_image(0, 0, image=photo_image, anchor=NW)

image_width = photo_image.width()
image_height = photo_image.height()

while True: 
  coodrinates = canvas.coords(my_image) #Gets coordinates of linked Image.
  print(coodrinates)
  if(coodrinates[0]>= (WIDTH - image_width) or coodrinates[0]<0): #If the coordinates at postion x of element zero is greater or equal to the Width minus current image width or if the coordinates of element zero are less than zero then the image would move backwards.
    xVelocity = -xVelocity
  
  if(coodrinates[1]>= (HEIGHT - image_height) or coodrinates[1]<0):
    yVelocity = -yVelocity

  canvas.move(my_image, xVelocity, yVelocity) #Takes three arguements, What you want to move? How far on each axis and coordinate (counts as 2, since x and y)? 
  window.update() #Update window 
  time.sleep(0.01)

window.mainloop()