'''
TESTE DE HOMOGENEIDADE DE BARTLETT
As variancias das populacionais de k amostras sejam iguais
Implementacao do testes χ2 de Bartlett (1937),
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches #para legendas manuais
import math
import scipy.stats as st
import random

class bartlettTest:
    def __init__(self, data_filename, amostras, variavel):
        #amostras - coluna das amostras a serem comparadas (como fatores aqui)
        #variavel - a variavel a ser testada entre amostras
        self.categorias = amostras
        self.variavel = variavel
        self.df = pd.read_csv(data_filename)
        self.k = self.df[self.categorias].nunique() # k e o numero de tratamentos (amostras)
        self.n = self.df.groupby(self.categorias).size()# eh o tamanho de cada amostra
        self.N = sum(self.n) # tamanho total 
        self.runTest()
        
    def runTest(self):
        
        #calculando o q
        variancia = self.df.groupby(self.categorias)[self.variavel].var()
        Sp2 = sum((self.n-1)*variancia)/(self.N-self.k)
        q = (self.N-self.k)*np.log(Sp2)-(sum((self.n-1)*np.log(variancia)))       
        #calculando o c
        c = 1+(1/(3*(self.k-1)))*(sum((1/(self.n-1))-(1/(self.N-self.k))))       
       #Bcalculado
        Bcalc = q/c
        Bcritico = st.chi2.ppf(0.95, self.k-1)
        
        if(Bcalc > Bcritico):
            return False #As amostras nao sao homogeneas
        else:
            return True # As amostras sao homogeneas



if __name__ == "__main__":
    bt = bartlettTest("Homogeneidade_Bartlett\dataLojas.csv", "Loja", "Nclientes")