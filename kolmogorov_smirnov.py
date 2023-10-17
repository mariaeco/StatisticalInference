#Implementacao do teste de Kolmogorov-Smirnov
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
#from math import trunc
#pip install scipy  #INSTALAR ASSIM PRIMEIRO
import scipy.stats as st 


alfa = 0.05 #5%
maqAgric = pd.read_csv("maquinaAgric.csv")


#Frequencia absoluta
df = maqAgric['ProdMaq'].value_counts().reset_index()#maqAgric.ProdMaq.value_counts()
df.rename(columns={'ProdMaq': 'X_i', 'count': 'Fabs'}, inplace=True)
df = df.sort_values(by='X_i', ascending=True).reset_index(drop=True)

#Frequencia acumulada
df['Fac'] = np.cumsum(df['Fabs'])

#Frequencia acumulada relativa
Namostras = sum(df['Fabs'])
df['Fobs'] = df['Fac']/Namostras

#Zcalculado
mu = maqAgric['ProdMaq'].mean()
sd = maqAgric['ProdMaq'].std()
df['Zcalc'] = (df['X_i']-mu)/sd

valores_formatados = []
# Percorra cada valor em df['Zcalc']

for valor in df['Zcalc']:
    # Formate o valor para duas casas decimais sem arredondar
    valor_formatado = round(valor,2)
    #valor_formatado = trunc(valor * 100) / 100 #aqui faço o corte do valor sem arredondar, pq estava diferenca o final sem arredondar
    valores_formatados.append(valor_formatado)

df['Zcalc'] = valores_formatados

normalTb = pd.read_csv("normalTable_leftcum.csv")
#print(normalTb)

m = len(df['Zcalc']) #11 qtd de producoes distintas
Fesp = []

for z in range(0, m):
    valor = st.norm.cdf(df['Zcalc'][z])
    #valor = trunc(valor * 10000) / 10000 
    Fesp.append(round(valor,4))

df['Fesp'] = Fesp
df['Exp(i)_Obs(i)'] = abs(Fesp-df['Fobs'])


Fespobs2 = [round(df['Fesp'][0],4)]
for i in range(1, len(Fesp)):
    valor = Fesp[i] - df['Fobs'][i-1]
    Fespobs2.append(valor)

df['Exp(i)_Obs(i-1)'] = Fespobs2

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


max1 = max(df['Exp(i)_Obs(i)'])
max2 = max(df['Exp(i)_Obs(i-1)'])

Dcalc = max(max1,max2)
print("\nDcalculado: ", round(Dcalc,3))

#ver arquivo Tabela-Kolmogorov-valoresCriticos.pdf
Dcrit = 1.36/math.sqrt(Namostras)
print("DCritico: ", round(Dcrit,3))
#caso modifique o numero das seja <35 preciso modificar essa funcao do Dcritico para procurar na tabela
#criticalV = pd.read_csv("kolmogorovCriticalvalues.csv")
#print(criticalV)

if(Dcalc > Dcrit):
    print(" --> A variavel Producao de Maquinas em 36 meses NAO Segue uma Distribuicao Normal <--")
else:
    print(" --> A variavel Producao de Maquinas em 36 meses Segue uma Distribuicao Normal <-- ")
    


plt.hist(df['Exp(i)_Obs(i)'], bins=6, edgecolor='black')  # 'bins' define o número de caixas no histograma
plt.show()


