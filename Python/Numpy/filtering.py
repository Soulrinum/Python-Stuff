import numpy as np 
#Filtering refers to the process of selecting elements from an array that match a given condition. 

ages = np.array([[11, 12, 7, 8, 9, 15, 13, 14, 16, 18],
                 [20, 30, 25, 23, 21, 22, 28, 24, 27, 29]
                 ])

pre_teen = ages[13>ages]
print(f"Preteens: {pre_teen}")

teenages = ages[(ages >= 13) & (ages < 20)]
print(f"Teenagers: {teenages}")

Twenties = ages[(ages >= 20) & (ages < 30)]
print(f"Teenagers: {Twenties}")

Uncs = ages[(ages >= 30) & (ages < 50)]
print(f"Uncs: {Uncs}")

even = ages[ages % 2 == 0] #Where % means modulos, which it tells you what's left over after dividing one number by another. In this case if remainder equals zero place the value into a new array. 
print(f"Even Ages:{even}")

odd = ages[ages % 2 != 0] #Where % means modulos, which it tells you what's left over after dividing one number by another. In this case if remainder DOES NOT equals zero place the value into a new array. 
print(f"Odd Ages:{odd}")

eventeen = teenages[teenages % 2 == 0] #This also works with other variables. 
print(f"Even Teenage Ages:{eventeen}")

teens = np.where(ages <= 19, ages, 0) #This allows us to preserve the orignal structure of the array all the previous ones simply return a new array. np.where(condition, array, fillvalue). 
print(f"Orignial Teens: {teens}")