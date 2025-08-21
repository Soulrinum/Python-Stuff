import numpy as np 
import matplotlib.pyplot as plt

rng = np.random.default_rng()
votes = rng.integers(1, 1000, size=9)

fiction = ["Yaoi", "Yuri", "Mpreg", "Shoujo", "Sci-fi", "Action", "Fantasy", "Adventure", "Shounen"]

plt.pie(votes, labels=fiction, autopct="%.1f%%") #Percentage With 1 decimal place
plt.axis()
plt.show()

