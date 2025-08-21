import numpy as np 
import matplotlib.pyplot as plt
#A histogram is a graphical representation of the distribution of numerical data, typically displayed as a series of bars. These bars represent the frequency or count of data points that fall within specified ranges or "bins".

ages = np.random.normal(20, 1.5, 1000) #(Mean, Std, Range)

plt.hist(ages, #Bins seperates data into sections. These sections are based off similar values. You Can do seperate values like bin=20 for 20 different sections. 
         bins=[ages.min(), 18, 21, ages.max()]) #Sections the histogram based off the youngest age and similar vales, 18 and similar values and so on. 
plt.show()

