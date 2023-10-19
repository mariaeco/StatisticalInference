import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import scipy.stats as st

class ShapiroWilkTest:
    def __init__(self, data_filename, target_column, alpha):
        self.alpha = alpha
        self.data = pd.read_csv(data_filename)
        self.target_column = target_column
        self.df = pd.DataFrame() # Tabela que iremos colocar os valores
        self.prepare_data()

    def prepare_data(self):
        n = len(self.data)
        self.df["i"] = [i for i in range(1, (n // 2) + 1)]
        self.df["n-(i-1)"] = [n-i+1 for i in range(1,(n // 2) + 1)]
        self.df["a_i,n"] = [coeficientes[str(n)][i] for i in range(0,len(self.df))] # Consultando a tabela coeficientes
        self.df["X_(n-i+1)"] = [self.data[self.target_column][n-i+1] for i in range(2,len(self.df)+2)] # 2 pois a primeira linha é indice 0(+1), e o indice começa no 1(+1)
        self.df["X_i"] = [self.data[self.target_column][i] for i in range(0,len(self.df))]
        self.df["a_i,n (X_(n-i+1) - X_i)"] = self.df["a_i,n"] * (self.df["X_(n-i+1)"] - self.df["X_i"])

    def run_test(self):
        media = self.data[self.target_column].mean()
        b = sum(self.df["a_i,n (X_(n-i+1) - X_i)"])
        w_calc = (b**2)/(sum((xi - media)**2 for xi in self.data[self.target_column]))
        w_crit = criticos[str(self.alpha)][len(self.data)-3] # pois a amostra começa tamanho 3
        print("\n----------- Tabela: Shapiro-Wilk -----------")
        print(self.df)

        print("\nWcalculado:", round(w_calc, 3))
        print("WCritico:", round(w_crit, 3))

        if w_calc > w_crit:
            print(" --> A variável NAO Segue uma Distribuicao Normal <--")
        else:
            print(" --> A variável Segue uma Distribuicao Normal <--")

coeficientes = pd.read_csv("coeficientesShapiro.csv", na_values="NA")
criticos = pd.read_csv("valoresCriticosShapiro.csv")
sw = ShapiroWilkTest("p_mensal_avioes.csv", "prodAvioes", 0.01)
sw.run_test()