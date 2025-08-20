import numpy as np 

array2 = np.array([
  [1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]
  ]) #Matrix 

# array[start:end:step]

print(array2[0]) #Returns the first row as it is indexed at zero. 

print(array2[-1]) #Returns last row, Negative indexing also works. 

print(array2[0:2]) #Retuns all values within index 0 to index 2, but not including two itself. 

print(array2[0:4:2]) #Gives every second row. 

print(array2[::2]) #Ommits Start and End in this case only leaving the step. 

print(array2[::-1]) #Prints all rows reversed. 

print(array2[::-2]) #Prints every second row but reversed. 

print(array2[:,0]) #Selects all rows with index Zero. Returns 1, 5, 9, 13. 

print(array2[:, 0:3])# Selects all columns with within the range of index 0 to 3 but excluding 3. 

