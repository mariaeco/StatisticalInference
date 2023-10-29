import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches #para legendas manuais
import math
import scipy.stats as st
import random

class KolmogorovSmirnovTest:
    def __init__(self, data_filename, target_column):
        #self.alpha = alpha
        self.data = pd.read_csv(data_filename)
        self.target_column = target_column
        self.prepare_data()

    def prepare_data(self):
        self.frequency_absolute = self.data[self.target_column].value_counts().reset_index()
        self.frequency_absolute.rename(columns={self.target_column: 'X_i', 'count': 'Fabs'}, inplace=True)
        self.frequency_absolute = self.frequency_absolute.sort_values(by='X_i', ascending=True).reset_index(drop=True)
        self.frequency_absolute['Fac'] = np.cumsum(self.frequency_absolute['Fabs'])
        self.N_samples = sum(self.frequency_absolute['Fabs'])
        self.frequency_absolute['Fobs'] = self.frequency_absolute['Fac'] / self.N_samples
        mu = self.data[self.target_column].mean()
        sd = self.data[self.target_column].std()
        self.frequency_absolute['Zcalc'] = ((self.frequency_absolute['X_i'] - mu) / sd).round(2)

    def calculate_expected(self):
        m = len(self.frequency_absolute['Zcalc'])
        F_esp = []

        for z in range(0, m):
            value = st.norm.cdf(self.frequency_absolute['Zcalc'][z])
            F_esp.append(round(value, 4))

        self.frequency_absolute['Fesp'] = F_esp
        self.frequency_absolute['Exp(i)_Obs(i)'] = abs(np.array(F_esp) - self.frequency_absolute['Fobs'])

        Fesp_obs2 = [round(self.frequency_absolute['Fesp'][0], 4)]
        for i in range(1, len(F_esp)):
            value = F_esp[i] - self.frequency_absolute['Fobs'][i - 1]
            Fesp_obs2.append(value)

        self.frequency_absolute['Exp(i)_Obs(i-1)'] = Fesp_obs2

    def run_test(self):
        self.a_values = [0.2, 0.15, 0.1, 0.05, 0.01]
        
        max1 = max(self.frequency_absolute['Exp(i)_Obs(i)'])
        max2 = max(self.frequency_absolute['Exp(i)_Obs(i-1)'])
        self.D_calc = max(max1, max2)
        # Achar valor critico
        self.Dcrit_values = []  # Lista para armazenar os valores de Dcrit
        criticalV = pd.read_csv("kolmogorovCriticalvalues.csv")
        
        for alpha in self.a_values:  
            if self.N_samples <= 35:
                row_index = criticalV[criticalV['n'] == self.N_samples].index[0]
                Dcrit = criticalV.loc[row_index][str(alpha)]
            else:
                match alpha:
                    case 0.2:
                        Dcrit = 1.07/math.sqrt(self.N_samples)
                    case 0.15:
                        Dcrit = 1.14/math.sqrt(self.N_samples)
                    case 0.1:
                        Dcrit = 1.22/math.sqrt(self.N_samples)
                    case 0.05:
                        Dcrit = 1.36/math.sqrt(self.N_samples)
                    case 0.01:
                        Dcrit = 1.63/math.sqrt(self.N_samples)
            self.Dcrit_values.append(round(Dcrit,3))  # Adicione o valor de Dcrit à lista

        print("\n----------- Tabela: Kolmogorov-Smirnov -----------")
        print(self.frequency_absolute)

    #PLOTANDO GRAFICO DE BARRA PQ A VARIAVEL É DISCRETA - SE FOR CONTINA DEVE PLOTAR HISTOGRAMA
    def graficos(self):
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(8, 10))
        plt.subplots_adjust(hspace=0.4) # aumento a distancia entre graficos superiores e inferiores
        
        #PLOT 1 - BARPLOT -----------------------------------------------------------------------------------------
        unique_values, counts = np.unique(self.data[self.target_column], return_counts=True)
        ax1.bar(unique_values, counts, align='center', edgecolor='black')
        variable_name = self.target_column
        ax1.set_xlabel(f'{variable_name}')
        ax1.set_ylabel('Count')  # Adicione um rótulo ao eixo y
        ax1.set_title('Grafico de Barras') 
    
        #PLOT 2 - ESPERADO X OBSERVADO -----------------------------------------------------------------------------
        ax2.scatter(self.frequency_absolute['Fesp'],self.frequency_absolute['Fobs'])
        ax2.set_title('Esperado x Observado')
        ax2.set_ylabel("Frequencia Observada")
        ax2.set_xlabel("Frequencia Esperada")
        # Define the parameters of the model (slope and intercept)
        slope = 1  # Change this to your desired slope
        intercept = 0  # Change this to your desired intercept
        # Add the line of the model
        x_model = np.linspace(0, 1, 100)  # Create x-values for the line
        y_model = slope * x_model + intercept  # Calculate y-values based on the model
        ax2.plot(x_model, y_model, linestyle='-', color='red', label=f'Model: y = {slope}x + {intercept}')
         
        #PLOT 3 - ALPHA X DCRITIC -------------------------------------------------------------------------------------
        colors = ['blue' if self.D_calc < Dcrit else 'red' for Dcrit in self.Dcrit_values]
        bin = [0 if self.D_calc > Dcrit else 1 for Dcrit in self.Dcrit_values]
        
        ax3.scatter(self.a_values,self.Dcrit_values, c = colors)
        ax3.axhline(y=self.D_calc, color='black', linestyle='--')
        ax3.set_title('Dcalculado > Dcritico: Rejeita H0')
        ax3.set_ylabel("Dcritico")
        ax3.set_xlabel("Alpha value")
        ax3.text(0.01, self.D_calc + 0.0001, f'Dcalculado: {self.D_calc:.2f}', color='black')
        handles, labels = ax3.get_legend_handles_labels() #legendas
        red_patch = mpatches.Patch(color='red', label='Rejeita H0 - Nao Normal')
        blue_patch = mpatches.Patch(color='blue', label='Aceita H0 - Dist Normal')
        ax3.legend(handles=[blue_patch, red_patch])

        ax4.scatter(self.a_values,bin, c = colors)
        ax4.set_ylabel("0 - Rejeita/ 1 - Aceita H0")
        ax4.set_xlabel("Alpha value")

        plt.show()


if __name__ == "__main__":
    ks = KolmogorovSmirnovTest("maquinaAgric2.csv", "ProdMaq")
    ks.calculate_expected()
    ks.run_test()
    #ks.plot_histograms()
    ks.graficos()
    
    
    