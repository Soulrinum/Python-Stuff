import numpy as np 

array = np.array([1, 2, 3])

#Scalar Math Functions. 
print(array + 1)#Adds 1 to each value. 
print(array - 1)
print(array * 3)#Multiplies 
print(array / 3)#Divide 
print(array ** 5)#Power Of. 

#Vectorized Math Functions. 
print(np.sqrt(array)) #This is a vectorized maths function, we can apply a function on an enitre array without writing a loop. This is not possible without numpy. 
print(np.round(array)) #Rounds Numbers 
print(np.floor(array)) #Rounds Numbers Down 
print(np.ceil(array)) #Rounds Numbers Up
print(np.pi) #Returns first 10 digits of pi. 

#Combination Of Both 
print(np.round(np.pi * array ** 2))#To Calcuate The Area Of A Circle, rounded. 

scores = np.array([90, 60, 70, 80, 55, 63, 58])
filterd_scores = scores[scores>55]
print(filterd_scores) #Helps with removing small unwanted values. 

