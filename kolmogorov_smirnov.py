#Implementacao do teste de Kolmogorov-Smirnov
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
#from math import trunc
#pip install scipy  #INSTALAR ASSIM PRIMEIRO
import scipy.stats as st 

class Kolmogorov:
    def __init__(self, arquivo, alfa):
        self.alfa = alfa
        amostra = pd.read_csv(arquivo)
        media = amostra.iloc[:, 1].mean()
        sd = amostra.iloc[:, 1].std()
        # Frequência Absoluta
        df = amostra.iloc[:, 1].value_counts().reset_index()
                 # ver valores na segunda coluna
        df.rename(columns={df.columns[0]: 'X_i', df.columns[1]: 'F_absoluta'}, inplace=True)
        df = df.sort_values(by='X_i', ascending=True).reset_index(drop=True)

        # Frequência Acumulada
        df['F_acumulada'] = np.cumsum(df['F_absoluta'])

        # Frequência Acumulada Relativa
        num_amostras = sum(df['F_absoluta'])
        self.num_amostras = num_amostras
        df['F_observada'] = df['F_acumulada']/num_amostras

        # Zcalculado
        df['Zcalc'] = round((df['X_i'] - media)/sd,2)

        # Calculando F_esperado(X_i) - F_observado(X_i)
        m = len(df['Zcalc']) # qtd de producoes distintas
        F_esp = []
        for z in range(0, m):
            valor = st.norm.cdf(df['Zcalc'][z]) # Calcular distribuição normal acumulada
            F_esp.append(round(valor,4))

        df['F_esperado'] = F_esp
        df['F_esp(X_i)-F_obs(X_i)'] = abs(F_esp-df['F_observada'])
        
        # Calculando F_esperado(X_i) - F_observado(X_i-1)
        F_espobs2 = [round(df['F_esperado'][0],4)] # a primeira linha não muda quanto ao F_esperado
        for i in range(1, len(F_esp)):
            valor = abs(F_esp[i] - df['F_observada'][i-1])
            F_espobs2.append(valor)

        df['F_esp(X_i)-F_obs(X_i-1)'] = F_espobs2

        #
        self.df = df

    def show_tabela(self):
        print("\n----------- Tabela: Kolmogorov-Smirnov -----------")
        print(self.df)

    def is_normal(self):
        max1 = max(self.df['F_esp(X_i)-F_obs(X_i)'])
        max2 = max(self.df['F_esp(X_i)-F_obs(X_i-1)'])
        Dcalc = max(max1,max2)
        print("\nDcalculado: ", round(Dcalc,3))

        # Achar valor critico
        criticalV = pd.read_csv("kolmogorovCriticalvalues.csv")
        
        if self.num_amostras <= 35:
            Dcrit = criticalV.columns['self.alfa'][self.num_amostras]
        else:
            match self.alfa:
                case 0.2:
                    Dcrit = 1.07/math.sqrt(self.num_amostras)
                case 0.15:
                    Dcrit = 1.14/math.sqrt(self.num_amostras)
                case 0.1:
                    Dcrit = 1.22/math.sqrt(self.num_amostras)
                case 0.05:
                    Dcrit = 1.36/math.sqrt(self.num_amostras)
                case 0.01:
                    Dcrit = 1.63/math.sqrt(self.num_amostras)

        print("DCritico: ", round(Dcrit,3))
        if(Dcalc > Dcrit):
            print(" --> A variavel Producao de Maquinas em 36 meses NAO Segue uma Distribuicao Normal <--")
        else:
            print(" --> A variavel Producao de Maquinas em 36 meses Segue uma Distribuicao Normal <-- ")
            
    def plot_grafico(self):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        ax1.hist(self.df['F_absoluta'], bins=6, edgecolor='black')  # 'bins' define o número de caixas no histograma
        ax1.set_title('Frequencia absoluta')

        ax2.hist(self.df['F_esp(X_i)-F_obs(X_i)'], bins=6, edgecolor='black')  # 'bins' define o número de caixas no histograma
        ax2.set_title('F_esp(X_i)-F_obs(X_i)')

        plt.show()

normalTb = pd.read_csv("normalTable_leftcum.csv")       
ks = Kolmogorov("maquinaAgric.csv", 0.05)
ks.show_tabela()
ks.is_normal()
ks.plot_grafico()