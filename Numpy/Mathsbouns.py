import numpy as np

#Finding e/m relationship: 

#Finding B Field.
permability = np.array([1.25663706*10**-6])
Coils = np.array([500])
Current = np.array([10])
Resistance = np.array([20])
Constant = np.array([4/5])
Constant2 = np.array([Constant ** 3/2])

B_Filed = (Constant * permability * Coils * Current)/20
print(B_Filed)

#Finding e/m With B Field Value. 
Voltage = Current/Resistance 
B_Filed2 = np.array([B_Filed**2])
em_relationship = (2 * Voltage)/(B_Filed2)
si = np.format_float_scientific(em_relationship, precision=2, exp_digits=2)
print(si)