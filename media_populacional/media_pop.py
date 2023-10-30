from scipy.stats import norm
from kolmogorov_smirnov import KolmogorovSmirnovTest
import random
import numpy as np
import pandas as pd
import statistics
# Para uma amostra aleatória de tamanho n
# Média desconhecida
# Variância conhecida
# Iremos fazer: Teste Bicauldal

class Teste_Z:
    def __init__(self, valor, alpha):
        self.alpha = alpha
        self.valor = valor
        self.num_samples = random.randrange(30,40)
        randomVar = np.random.normal(size=self.num_samples)
        self.data = pd.DataFrame({'RandomVar': randomVar})
        self.target_column = 'RandomVar'
        self.ks = KolmogorovSmirnovTest(self.data, self.target_column, self.alpha)
        self.is_normal()
        self.plot_grafico()

    def plot_grafico(self):
        pass
        # Aqui a gente vai fazer um grafico de linhas(variaveis contínuas) 
        # ou barras (variaveis discretas) para mostrar a variavel
        # Independentemente se a amostra é normal ou não

    def is_normal(self):
        self.ks.calculate_expected() # Terminar de calcular as variaveis da amostra
        if self.ks.run_test() == True:
            print("A amostra segue uma distribuição normal para alfa =", self.alpha)
            print()
            # Fazendo o teste:
            self.teste()
        else:
            print("A amostra não segue uma distribuição normal\n   ---> Portanto o Teste Z não pode ser feito")

    def teste(self):
        # fazer para todos os alfas q a gente tem no arquivo ou só alguns?
        m = self.data[self.target_column].mean()
        self.data = [valor for valor in self.data[self.target_column]] # transformar o df em lista para fazer os calculos
        
        # Calculando z_calculado
        variancia_amostra = statistics.stdev(self.data)
        erro_padrão = variancia_amostra/(self.num_samples)**(1/2)
        z_calculado = (m - self.valor)/erro_padrão
        
        # Calculado Zc
        # normal seguindo (mi, s) = (0, 1)
        muz = 0 # media da normal
        desvio_padrao = 1 # desvio padrão
        pr = self.alpha/2 # Pois é bicaudal
        zc = norm.ppf(pr, muz, desvio_padrao)

        if z_calculado > zc:
            print(f"Bicaudal: Como o valor {z_calculado} > {zc} aceitamos H0 a um nível de {self.alpha*100}% de significância")
        else:
            print("Bicaudal: Rejeitamos H0 do valor", self.valor)

tz = Teste_Z(10, 0.05)


"""
# H_0: mi >= 4.2g
mi = 4.2
# desvio padrão
s = 2
# amostras
n = 42
# alfa
alpha = 0.05
# nova média em relação as amostras
xb = 3.2

def z_calculado(mi, s, n, xb):
    erro_padrão = (s/(n)^1/2)
    return (xb - mi)/erro_padrão

def calcular_zc(alpha):
    # normal seguindo (mi, s) = (0, 1)
    muz = 0 # media da normal
    desvio_padrao = 1 # desvio padrão
    pr = alpha # pois é dito que a média é no minimo 4.2, então no grafico começa a partir de alpha a aceitar
    return norm.ppf(alpha, muz, desvio_padrao)

z = z_calculado(mi, s, n, xb)
zc = calcular_zc(alpha)

if z > zc:
    print(f"Como o valor {z} > {zc} aceitamos H0 a um nível de {alpha*100}% de significância")
else:
    print("Rejeitamos H0")
"""