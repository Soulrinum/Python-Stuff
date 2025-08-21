import numpy as np 
#Aggergrate functions summarize data and typicall return a single value. 

array = np.array([[1, 2, 3 , 4, 5], 
                  [6, 7, 8, 9, 10]
                  ])

print(np.sum(array)) # Returns Sum of all values within the array. 

print(np.mean(array)) #Returns mean of all values within the array. 

print(np.std(array)) #Returns standard deviation. 

print(np.var(array)) #Returns Variance std^2

print(np.min(array)) #Returns Lowest Value 

print(np.max(array)) #Returns Highest Value

print(np.argmin(array)) #Returns the indexed position of the lowest value.

print(np.argmax(array)) #Returns the indexed position of the highest value.

print(np.sum(array, axis=0)) #Sums all columns.

print(np.sum(array, axis=1)) #Sums all rows. 

