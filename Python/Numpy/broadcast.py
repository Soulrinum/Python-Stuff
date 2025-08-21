import numpy as np 

#Broadcasting allows Numpy to perform operations on arrays with different shapes by virtually expanding dimensons, so they can match the large arrays shape. 
#The Dimensons must have the same size or one of the dimensons has the size of 1. 
#You Read Dimesons Right to Left.

#The arrangement of arrays is Columns, Rows, 

array1 = np.array([[1, 2, 3, 4]]) #One Row, Four columns
array2 = np.array([[1], [2], [3], [4]]) #Four Rows but one column 

print(array1.shape)
print(array2.shape)

print(array1 * array2)

#array3 = np.array([
  #[1, 2, 3, 4]
  #[5, 6, 7, 8]
  #])

#print(array3*array2) #This would result in an error as array3 has two rows which does isn't one nor does it match the amount of rows in array 2. 

array4 = np.array([
  [1, 2, 3, 4],
  [5, 6, 7, 8],
  [9, 10, 11, 12],
  [13, 14, 15, 16]
  ])

print(array4.shape)

print(array4*array2) #In this It would work as array2 is (4,1) while array4 is (4,4). The 4 values match eachother while every number works with one as stated eariler. 
