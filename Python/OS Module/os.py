from os import *
import os
from datetime import datetime #Makes time informationm from os.stat readable. 

os.chdir('C:/Users/firem/Documents/')

os.makedirs("Rat") #Makes A Directory

os.removedirs("Rat") #Removes A Directory 

os.rename("Current Want", "New Name")

mod_time = os.stat("Python").st_mtime #Prints out information of chosen directory. st_size = Size of directroy. st_mtime = Last modified time. st_ctime = Creation time. 
print(datetime.fromtimestamp(mod_time)) #Allows time information from os.stat to be readable.  

for dirpath, dirnames, filenames, in os.walk('C:/Users/firem/Documents/'): #os.walk(), is a generator that yeilds a tuple of three values as its navigating the directory tree. For each direcotry it discovers, the directory path, the directory in that path and the files in said path. 
  print('Current Path', dirpath)
  print('Directories', dirnames)
  print('Files', filenames)
  print()


print(os.listdir()) #Lists all files names within the directory. 

os.environ.get("Home") #Gets the home enviroment.
print(os.environ)

