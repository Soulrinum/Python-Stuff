import numpy as np 

my_list = [1, 2, 3 , 4]*2 # This would dupe the dataset. 
print(my_list)

my_list_numpyy = np.array([1, 2, 3 , 4])*2 #This would multiply all the values in the list by 2. 
print(my_list_numpyy)