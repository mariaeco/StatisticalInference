import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches #para legendas manuais
import math
import scipy.stats as st
import random

class ShapiroWilkTest:
    def __init__(self):
        
        min_value = 15
        max_value = 46
        self.num_samples = 24  # Esse eh o numero maximo q tenho da tabela de valores criticos de kolmogorov
        self.randomVar = [random.randint(min_value, max_value) for _ in range(self.num_samples)]
        #testando com o dado p_mensal_avioes - o codigo esta todo ok,pois resulta no mesmo
        #self.randomVar = [15,16,18,19,20,22,23,23,24,24,25,28,28,29,30,30,31,32,32,34,36,36,39,46]

        self.data = pd.DataFrame({'RandomVar': self.randomVar})
        self.target_column = 'RandomVar'
        self.df = pd.DataFrame()
        self.prepare_data()

    def prepare_data(self):
        n = len(self.data)
        self.df["i"] = [i for i in range(1, (n // 2) + 1)]
        self.df["n-(i-1)"] = [n-i for i in range(0,(n // 2) )] # --->  ALTEREI AQUI <---
        self.df["a_i,n"] = [coeficientes[str(n)][i] for i in range(0,len(self.df))] # Consultando a tabela coeficientes
        self.df["X_(n-i+1)"] = [self.data[self.target_column][n-i+1] for i in range(2,len(self.df)+2)] # 2 pois a primeira linha é indice 0(+1), e o indice começa no 1(+1)
        self.df["X_i"] = [self.data[self.target_column][i] for i in range(0,len(self.df))]
        self.df["a_i,n (X_(n-i+1) - X_i)"] = self.df["a_i,n"] * (self.df["X_(n-i+1)"] - self.df["X_i"])

    def run_test(self):
        
        self.a_values = [0.01,0.02,0.05,0.1,0.5,0.9,0.95,0.98,0.99]
        media = self.data[self.target_column].mean()
        b = sum(self.df["a_i,n (X_(n-i+1) - X_i)"])
        self.w_calc = (b**2)/(sum(((xi - media)**2) for xi in self.data[self.target_column]))
        
        for xi in self.data[self.target_column]:
            print(xi)
        self.criticos= pd.DataFrame(criticos) # Tabela que iremos colocar os valores
        self.w_crit = []
        for alpha in self.a_values:
            index = self.num_samples-3
            self.w_c = self.criticos.iloc[self.num_samples-3][str(alpha)]
            self.w_crit.append(self.w_c)
        
        
        print("\n----------- Tabela: Shapiro-Wilk -----------")
        print(self.df)
        
        
        
         
    #PLOTANDO GRAFICO DE BARRA PQ A VARIAVEL É DISCRETA - SE FOR CONTINA DEVE PLOTAR HISTOGRAMA
    def grafico(self):
        fig, ((ax1, ax2),(ax3, ax4)) = plt.subplots(2, 2, figsize=(8, 10))
        plt.subplots_adjust(hspace=0.4) # aumento a distancia entre graficos superiores e inferiores
        # Use plt.bar para criar um gráfico de barras
        unique_values, counts = np.unique(self.data[self.target_column], return_counts=True)
        ax1.bar(unique_values, counts, align='center', edgecolor='black')
        variable_name = self.target_column
        ax1.set_xlabel(f'{variable_name}')
        ax1.set_ylabel('Count')  # Adicione um rótulo ao eixo y
        ax1.set_title('Grafico de Barras')  # Altere o título para "Bar Chart"
        
        #PLOT 2 - OBSERVADO X ESPERADO -------------------------------------------------------------------------------------
        dados_ordenados = np.sort(self.data[self.target_column])
        # Calcule os quantis teóricos para uma distribuição normal
        n = len(self.data)
        quantis_teoricos = np.percentile(np.random.normal(0, 1, n), np.arange(0, n))
        # Crie o gráfico Q-Q plot manualmente
        ax2.scatter(quantis_teoricos, dados_ordenados)
        ax2.set_xlabel('Quantis Teóricos')
        ax2.set_ylabel('Quantis Observados')
        ax2.set_title('Q-Q Plot')
 
        
        #PLOT 3 - ALPHA X DCRITIC -------------------------------------------------------------------------------------
        colors = ['red' if self.w_calc < Wcrit else 'blue' for Wcrit in self.w_crit]
        bin = [0 if self.w_calc < Wcrit else 1 for Wcrit in self.w_crit]
        
        ax3.scatter(self.a_values,self.w_crit, c = colors)
        ax3.axhline(y=self.w_calc, color='black', linestyle='--')
        ax3.set_title('Wcalculado < Wcritico: Rejeita H0')
        ax3.set_ylabel("Wcritico")
        ax3.set_xlabel("Alpha value")
        ax3.text(0.01, self.w_calc + 0.0001, f'Wcalculado: {self.w_calc:.2f}', color='black')
        handles, labels = ax3.get_legend_handles_labels() #legendas
        red_patch = mpatches.Patch(color='red', label='Rejeita H0 - Nao Normal')
        blue_patch = mpatches.Patch(color='blue', label='Aceita H0 - Dist Normal')
        ax3.legend(handles=[blue_patch, red_patch])

        ax4.scatter(self.a_values,bin, c = colors)
        ax4.set_ylabel("0 - Rejeita/ 1 - Aceita H0")
        ax4.set_xlabel("Alpha value")

        
        
        plt.show()


coeficientes = pd.read_csv("coeficientesShapiro.csv", na_values="NA")
criticos = pd.read_csv("valoresCriticosShapiro.csv")
sw = ShapiroWilkTest()
sw.run_test()
sw.grafico()