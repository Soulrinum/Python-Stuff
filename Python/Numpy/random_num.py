import numpy as np 

rngint = np.random.default_rng()

print(rngint.integers(1, 7)) #The second number in this is case is exclusive, this means only values from 1-6 just like a dice would be returned.

print(rngint.integers(low=1, high=1001)) #You can use low and high to make it easier to understand when debugging. 

print(rngint.integers(low=1, high=1001, size=3)) #Allows you to set the amount of random numbers you want in a 1D array, where all the values occupy the columns. 

print(rngint.integers(low=1, high=1001, size=(3,2))) #This for a matrix. In this case 6 values would be returned as there is 2 columns, 3 rows. 


fixed_rngint = np.random.default_rng(seed=1)
print(fixed_rngint.integers(low=1, high=1001, size=(3,2))) #Allows you to keep the randomly generated numbers. 

print(np.random.uniform()) #Returns a random float between 0 and 1 where uniform allows all values to be equally chosen. 


shuffle = np.random.default_rng() #Shuffles all values within the Matrix. 
array = np.array([
  [1, 2, 3, 4, 5],
  [6, 7, 8, 9, 10]
  ])
shuffle.shuffle(array)
print(array)

shuffle = np.random.default_rng() #Shuffles all values within the Matrix. 
fetishes = np.array([
  ["Feet", "Earlobes", "Nostrils", "Armpits"]
  ])
fetish = shuffle.choice(fetishes)
print(fetish)
