import numpy as np 
import matplotlib.pyplot as plt
#A box plot, also known as a box and whisker plot, is a standardized way of displaying the distribution of data based on a five-number summary: minimum, first quartile (Q1), median (Q2), third quartile (Q3), and maximum. It provides a visual representation of the data's center, spread, and skewness. 

heights = np.random.normal(172, 8, 300) #(Mean, Std, Number Of)

plt.boxplot(heights) #Where orange/yellow line is the second quartile. Then the lines of the box are first and third quartile. Lastly the lines at the end are min and max. 
plt.show()  