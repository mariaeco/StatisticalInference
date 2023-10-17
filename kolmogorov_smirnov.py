#Implementacao do teste de Kolmogorov-Smirnov
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import trunc

alfa = 0.05 #5%
maqAgric = pd.read_csv("maquinaAgric.csv")

def Dcalc(exp, obs):
    print(max(exp, obs))

#Dcalc(2,4)

#Frequencia absoluta
df = maqAgric['ProdMaq'].value_counts().reset_index()#maqAgric.ProdMaq.value_counts()
df.rename(columns={'ProdMaq': 'X_i', 'count': 'Fabs'}, inplace=True)
df = df.sort_values(by='X_i', ascending=True)

#Frequencia acumulada
df['Fac'] = np.cumsum(df['Fabs'])

#Frequencia acumulada relativa
df['Fobs'] = df['Fac']/36

#Zcalculado
mu = maqAgric['ProdMaq'].mean()
sd = maqAgric['ProdMaq'].std()
df['Zcalc'] = (df['X_i']-mu)/sd

valores_formatados = []
# Percorra cada valor em df['Zcalc']

for valor in df['Zcalc']:
    # Formate o valor para duas casas decimais sem arredondar
    valor_formatado = trunc(valor * 100) / 100
    valores_formatados.append(valor_formatado)

df['Zcalc'] = valores_formatados

normalTb = pd.read_csv("normalTable_leftcum.csv")
#print(normalTb)
n = len(normalTb['zscore']) #80
m = len(df['Zcalc']) #11 qtd de producoes distintas




'''
#Para pegar o valor correspondente na tabela z (normalTb) que eh o Fesp --> Ainda não fiz
#Lembrar que a tabela z tem na primeira coluna o valor de z com a primeira casa decimal apenas
#E a primeira linha são os nomes das colunas, que contem os valores da segunda casa decimal de z
#cruzando achamos o valor do teste
#Exemplo para z = -1.78, tenho que ir na linha 18, coluna 9 = o valor correspondente eh 0.0375
ndecimais = 11 # tenho 11 colunas, quero os resultados correspondentes a segunda casa decimal, que começa a partir da segunda coluna, pois a primeira é o z-score até a primeira casa decimal
'''

#print(normalTb)
print("\n----------- Tabela: Kolmogorov-Smirnov -----------")
print(df)


