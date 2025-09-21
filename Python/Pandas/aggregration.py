import pandas as pd 

#Aggregate functions are used to reduce a set of values into a single summary. 

df = pd.read_csv("Datasets/pokemon.csv")

print(df.mean(numeric_only=True)) #Prints the mean of any columns that are numeric.
print(df.sum(numeric_only=True)) #Prints the sum of any colums that are numeric. 
print(df.min(numeric_only=True)) #Prints the minium value of any colums that are numeric. 
print(df.max(numeric_only=True)) #Prints the maximum value of any colums that are numeric. 
print(df["HP"].mean()) 
print(df.count()) #Counts the number of values in each Header. 
print(df.to_string()) #Allows for greater data display. 
