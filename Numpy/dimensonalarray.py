import numpy as np 

array0 = np.array("A") #Zero Dimensons 

array1 = np.array(["A", "E"]) #One Dimenson, as there is one list.

array2 = np.array([["A", "B", "C", "S"]]) #Adding to lists into the brackets In this case would make it two dimensonal.

matrix = np.array([["A", "B", "C"],
                   ["D", "E", "F"],
                   ["G", "H", "I"]]) #2D arrays are also known as matrixs. Where the lists themselves are rows and the values columns. 

array3 = np.array([[["A", "B", "C"],["D", "E", "F"],["G", "H", "I"]], #For both 2D and 3D arrays you need homogoneous values, you cannot have 3 values in all the boxes to then have 2 hence the extra A at the end. 
                   [["J", "K", "L"],["M", "N", "O"],["P", "Q", "R"]], 
                   [["S", "T", "U"],["V", "W", "X"],["Y", "Z", "A"]]
                   ]) #Dimensons can be infinite.


print(array3.ndim) #Where ndim = Number of Dimensons.

print(array3.shape) #Returns a tuple of intergers where it shows you the depth, rows, and columns. 

print(array3[2, 2, 1]) #Returns the Value A. As you have selected depth 0, Row 0 and Column Zero. If you wanted the Letter Z in this case you would use [2, 2, 1]. This is known as multidimesonal Indexing. 

cow = array3[0, 0, 2] + array3[1, 1, 2] + array3[2, 1, 1] #This allows you to Return Cow 
print(cow)

Sexy = array2[0, 3] + array1[1] + array3[2, 1, 2] + array3[2, 2, 0] #You can also combine values from different arrays. 
print(Sexy)