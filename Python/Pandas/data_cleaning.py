import pandas as pd 

df = pd.read_csv("Datasets\pokemon.csv")

df = df.drop(columns=["Legendary"]) #Drops Irrelevant columns. 

df = df.dropna(subset=["Type 2"]) #Handles missing data. 
 
df = df.fillna({"Type 2": "None"}) #Replaces Nan (Not A Number) with None, rather then dropping the entire column. 

df["Type 1"] = df["Type 1"].replace({"Grass": "GRASS"}) #Maniuplating inconsistent values. 

df["Name"] = df["Name"].str.lower() #Makes all letters within Header "Name" to be lowercase. 
 
df["Legendary"] = df["Legendary"].astype(bool) #This turns all string values within Header "Legendary" to boolean values. This is important as True/False strings are not the same as Boolean values. 

df = df.drop_duplicates() #Drops columns of duplicated data. 

print(df.to_string()) #to_string more data to be visible. 