import numpy as np 
import matplotlib.pyplot as plt

X_data = np.random.random(50) * 100 #Random only prints floats hence why we need to times it by 100. 
Y_data = np.random.random(50) * 100  

plt.scatter(X_data, Y_data, c="black") #You can use c to set the colours of the plots. 
#plt.scatter(X_data, Y_data, c="black", marker="*"), This would turn the circles into * 
#plt.scatter(X_data, Y_data, c="black", s=150), Allows you to change the size of the points 
#plt.scatter(X_data, Y_data, c="black", alpha=0.3) Makes data overlap easy to understand, the darker areas are where data overlaps most. Alpha acheives this with transparency manipulation. 



plt.show() #Need to run this unless you are using Jupiter or something similar. 