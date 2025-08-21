import numpy as np 
import matplotlib.pyplot as plt

#Weight Change Over The Years.

years = [2025 + x for x in range(5)] #Some simple maths so we don't have to write out the values. 2007 + "x", where x can be any number between the ranges of 1-19 but NOT 19. 
weights = [57, 58, 60, 62, 61]

plt.plot(years, weights, lw=2, linestyle="--") #Can change style and line. 
plt.show()