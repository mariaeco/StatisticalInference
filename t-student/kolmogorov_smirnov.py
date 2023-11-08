import pandas as pd
import numpy as np
import math
import scipy.stats as st
from scipy.stats import ksone

class KolmogorovSmirnovTest:
    def __init__(self, data_filename, target_column, alpha):
        self.alpha = alpha
        self.data = data_filename
        self.target_column = target_column
        print(self.data)
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
        #criticalV = pd.read_csv("kolmogorovCriticalvalues.csv")
        """
        for alpha in self.a_values:  
            if self.N_samples <= 35:
                Dcrit = ksone.ppf(1-alpha/2, self.N_samples)
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
        """
        if self.N_samples <= 35:
            Dcrit = ksone.ppf(1-self.alpha/2, self.N_samples)
        else:
            match self.alpha:
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
        if Dcrit >= self.D_calc:
            return True
        else:
            return False
