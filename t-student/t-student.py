from barlett import bartlettTest
import random
import numpy as np
from scipy.stats import t
import pandas as pd
from scipy.stats import norm
from kolmogorov_smirnov import KolmogorovSmirnovTest
import statistics
# t-student: geralmente amostras < 30
# Teste t-Student quando o desvio-padrão populacional ( σ) não for conhecido
# TESTE t-STUDENT PARA COMPARAÇÃO DE DUAS MÉDIAS POPULACIONAIS A PARTIR DE DUAS AMOSTRAS ALEATÓRIAS INDEPENDENTES
        # Caso 1: variâncias populacionais diferentes
        # Caso 2: Variâncias populacionais homogêneas
# TESTE t-STUDENT PARA COMPARAÇÃO DE DUAS MÉDIAS POPULACIONAIS A PARTIR DE DUAS AMOSTRAS ALEATÓRIAS EMPARELHADAS
class Teste_T:
        def __init__(self, valor, alpha, data, amostras, variavel):
                self.alpha = alpha
                self.valor = valor
                self.data = data
                self.variavel = variavel # ----------------------- pensava que essa variavel era a mesma coisa de target column
                self.num_samples = len(data) # --------------------------------------- não sei se seria assim
                self.bt = bartlettTest(self.data, amostras, self.variavel)
                self.ks = KolmogorovSmirnovTest(self.data, self.variavel, self.alpha)

        def is_normal(self):
                self.ks.calculate_expected() # Terminar de calcular as variaveis da amostra
                if self.ks.run_test() == True:
                        print("A amostra segue uma distribuição normal para alfa =", self.alpha)
                        print()
                        return True
                        #self.teste() # Teste T
                else:
                        print("A amostra não segue uma distribuição normal\n   ---> Portanto o Teste T não pode ser feito")
                        return False

        def teste(self):

                media_amostra = self.data[self.variavel].mean()
                self.data = [valor for valor in self.data[self.variavel]] # transformar o df em lista para fazer os calculos

                # Calculando z_calculado
                variancia_amostra = statistics.stdev(self.data)
                erro_padrão = variancia_amostra/(self.num_samples)**(1/2)
                t_calculado = (media_amostra - self.valor)/erro_padrão

                # Calculado Zc
                # normal seguindo (mi, s) = (0, 1)
                muz = 0 # media da normal
                desvio_padrao = 1 # desvio padrão
                pr = self.alpha/2 # Pois é bicaudal
                tc = t.ppf(pr, muz, desvio_padrao)

                if t_calculado > tc:
                        print(f"Bicaudal: Como o valor {t_calculado} > {tc} aceitamos H0 a um nível de {self.alpha*100}% de significância") # Não tenho certeza se essa seria a frase
                else:
                        print("Bicaudal: Rejeitamos H0 do valor", self.valor) # Não tenho certeza se essa seria a frase

tt = Teste_T(10, 0.05, "Homogeneidade_Bartlett\dataLojas.csv", "Loja", "Nclientes")

if tt.is_normal() == True:
        tt.teste() # Teste t-Student quando o desvio-padrão populacional ( σ) não for conhecido


# TESTE t-STUDENT PARA COMPARAÇÃO DE DUAS MÉDIAS POPULACIONAIS A PARTIR DE DUAS AMOSTRAS ALEATÓRIAS INDEPENDENTES
        # Caso 1: variâncias populacionais diferentes
        # Caso 2: Variâncias populacionais homogêneas
# TESTE t-STUDENT PARA COMPARAÇÃO DE DUAS MÉDIAS POPULACIONAIS A PARTIR DE DUAS AMOSTRAS ALEATÓRIAS EMPARELHADAS

bt = bartlettTest("Homogeneidade_Bartlett\dataLojas.csv", "Loja", "Nclientes")
def is_dependente():
        # Testar se amostras são dependentes
        return True
if is_dependente() == True:
        def medias_dependentes():
                pass
elif is_dependente() == False:
        def medias_independentes():
                if bt == True: # Testar se é homogênea
                        print("A amostra é Homogênea") # Caso 2
                else:
                        print("A amostra não é homogênea") # Caso 1



