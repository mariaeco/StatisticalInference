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
        print(Bcritico)
        
        if(Bcalc > Bcritico):
            print("As amostras nao sao homogeneas")
        else:
            print("As amostras sao homogeneas")
            
    #def graficos(self):
        # Ordene os dados observados
        #dados_observados = np.sort(self.df[self.variavel])
        # Calcule os valores previstos com base na distribuição normal padrão
        #valores_previstos = st.norm.ppf(np.arange(1, 90, self.N))

        # Crie um gráfico Q-Q para comparar os valores observados e previstos
        #plt.figure(figsize=(6, 6))
        #plt.scatter(valores_previstos, dados_observados)
        #plt.xlabel('Valores Previstos (distribuição normal padrão)')
        #plt.ylabel('Valores Observados')
        #plt.title('Gráfico Q-Q')
        #plt.grid(True)

        #plt.show()



if __name__ == "__main__":
    bt = bartlettTest("Homogeneidade_Bartlett\dataLojas.csv", "Loja", "Nclientes")
    #bt.graficos()
    #PARA TRABALHAR COM DADOS GERADOS ALEATORIAMENTE:
    #separando duas amostras de uma mesma populacao
    '''
    mu = 30
    sd = 10
    num_samples = 90
    valor = np.random.normal(mu, sd, size=num_samples)
    categ = ['Amostra1', 'Amostra2', 'Amostra3'] * 30 # dividindo 3 amostras da mesma populacao  para serem as categorias
    randompd = pd.DataFrame({'Categorias': categ,'Valor': valor})#, 'Categorias': categ                 
    randompd.to_csv('Homogeneidade_Bartlett/randompd.csv', index=False)
    resultado = bartlettTest("Homogeneidade_Bartlett/randompd.csv", "Categorias", "Valor")
    '''
