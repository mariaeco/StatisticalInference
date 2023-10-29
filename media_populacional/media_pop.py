from scipy.stats import norm
# Para uma amostra aleatória de tamanho n
# Média desconhecida
# Variância conhecida

"""
Um fabricante de cereais afirma que a quantidade média de fibra alimentar em cada porção do seu produto é no mínimo 4.2g 
com desvio padrão de 1g. Uma agência de saúde deseja verificar se essa afirmação procede, coletando uma amostra de 42 porções,
obtendo uma média de 3.2g. Com um nível de significância de 5%, existem evidências para rejeitar a afirmação? 
Use um desvio padrão de 2g.
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