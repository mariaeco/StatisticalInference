#Implementacao do teste de Kolmogorov-Smirnov
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import csv


alfa = 0.05 #5%


maqAgric = pd.read_csv("maquinaAgric.csv")
#print(maqAgric)

def Dcalc(exp, obs):
    print(max(exp, obs))

#Dcalc(2,4)

Fobs = maqAgric.ProdMaq.value_counts(ascending=True)
print("\n---- Frequencia observada dos valores: ----")
print(Fobs)

soma = sum(Fobs)
print("Soma:", soma)