import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib import style
from pathlib import Path #So I can save to a specific folder

x = np.arange(100) #Makes it an array not list, 100 is the amount of values you want. 

fig, axis = plt.subplots(2, 2, figsize=(15, 10)) #(Rows, Columns), Makes it a matrix. 

axis[0, 0].plot(x, np.sin(x)) #At Row and Column zero. 
axis[0, 0].set_title("Sin Wave")

axis[0, 1].plot(x, np.cos(x)) 
axis[0, 1].set_title("Cos Wave")

axis[1, 0].plot(x, np.random.random(100)) 
axis[1, 0].set_title("Random Unction")

axis[1, 1].plot(x, np.log(x)) 
axis[1, 1].set_title("Log FUnction")


save_dir = Path("Images") #As my python folder already has an Image folder, using the absoulte path would retrun an Error message.
output_path = save_dir / "fourplots.png"
fig.savefig(output_path, dpi=1000) #Where DPI = Quality of the image.

plt.show()