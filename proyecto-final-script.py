import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statistics
import scipy.stats as stats

# Ruta completa del archivo CSV en la unidad C:
archivo_csv = r'C:\Users\USER\OneDrive\Desktop\PF\ECH_2022 - BD Proyecto Final PyE 2023.csv'

# Leer el archivo CSV con separador (;)
datos_csv = pd.read_csv(archivo_csv, sep=';')

# Acceder a las columnas y convertirlas en vector
ID=datos_csv['ID']
AÑO=datos_csv['anio']
MES=datos_csv['mes']
SEXO=datos_csv['Sexo']
EDAD=datos_csv['Edad']
REGION=datos_csv['region']
PEA=datos_csv['PEA']
DESEMPLEO=datos_csv['Desempleo']
filtro = datos_csv[(PEA == 1) & (DESEMPLEO == 0)]
SALARIO = filtro['Salario']

# A1.a) Tasa de desempleo para la muestra
td=DESEMPLEO.sum()/PEA.sum()*100
print("La tasa de desempleo es: {:.2f}%".format(td))

# A1.b) Gráfico de tasa de desempleo por edad
filtro = datos_csv[(EDAD >= 14) & (EDAD <= 17)]
td1 = filtro['Desempleo'].sum()/filtro['PEA'].sum()*100

filtro = datos_csv[(EDAD >= 18) & (EDAD <= 25)]
td2 = filtro['Desempleo'].sum()/filtro['PEA'].sum()*100

filtro = datos_csv[(EDAD >= 26) & (EDAD <= 40)]
td3 = filtro['Desempleo'].sum()/filtro['PEA'].sum()*100

filtro = datos_csv[(EDAD >= 41)]
td4 = filtro['Desempleo'].sum()/filtro['PEA'].sum()*100

plt.bar(["14-17", "18-25", "26-40", "Más de 40"], [td1, td2, td3, td4])
plt.title("Tasa de desempleo por rango de edad")
plt.xlabel("Rango de edad")
plt.ylabel("Tasa de desempleo (%)")
plt.show()

# A2.a) Histograma de salarios
plt.hist(SALARIO, bins=100, edgecolor='blue', density=True)
plt.title("Histograma de Salarios")
plt.xlabel("Salarios")
plt.ylabel("Frecuencia Relativa")
plt.show()

# A2.b) Elaborar y corregir Boxplot de salarios
plt.boxplot(SALARIO)
plt.title("Boxplot de Salarios")
plt.ylabel("Salario")
plt.show()
Q1 = np.quantile(SALARIO, 0.1)
Q3 = np.quantile(SALARIO, 0.9)
IQR = Q3 - Q1
li = Q1 - 1.5 * IQR
ls = Q3 + 1.5 * IQR
SALARIO_corregido = np.where((SALARIO < li) | (SALARIO > ls), np.nan, SALARIO)
SALARIO_corregido = SALARIO_corregido[~np.isnan(SALARIO_corregido)]
plt.boxplot(SALARIO_corregido)
plt.title("Boxplot de Salarios Corregidos")
plt.ylabel("Salario")
plt.show()

# A2.c) Calcular media, mediana y moda de salarios.
print("\nLa media de salarios:", np.mean(SALARIO))
print("La mediana de salarios:", np.median(SALARIO))
print("La moda de salarios:", statistics.mode(SALARIO))

# A2.d) Calcular mínimo, máximo y cuartiles de salario.
salario_minimo = np.min(SALARIO)
salario_maximo = np.max(SALARIO)
cuartiles = np.percentile(SALARIO, [25, 50, 75])
print("\nEl salario mínimo es: ", np.min(SALARIO))
print("El salario máximo es: ", np.max(SALARIO))
print("Los cuartiles de salario son: ", np.percentile(SALARIO, [25, 50, 75]))

# A2.e) Presentar boxplot de salario por género y región
filtro1 = datos_csv[SEXO == 1]
filtro2 = datos_csv[SEXO == 2]
plt.figure(figsize=(8, 6))
plt.boxplot([filtro1['Salario'], filtro2['Salario']], labels=['Varones', 'Mujeres'])
plt.title("Boxplot de Salarios por Género")
plt.xlabel("Género")
plt.ylabel("Salario")
plt.show()
filtro1 = datos_csv[REGION == 1]
filtro2 = datos_csv[REGION != 1]
plt.figure(figsize=(8, 6))
plt.boxplot([filtro1['Salario'], filtro2['Salario']], labels=['Montevideo', 'Interior'])
plt.title("Boxplot de Salarios por Región")
plt.xlabel("Región")
plt.ylabel("Salario")
plt.show()

# B1) Estimar el desempleo del total de la población
print("\nEl desempleo estimado es: ", int(td/100*1757161))

# B2) Elaborar IC para la variable desempleo al 95%
zo = stats.norm.ppf(1 - 0.05/2)
ET = (td/100*(1-td/100)/PEA.sum())**0.5
LCi = td/100-ET*zo
LCs = td/100+ET*zo
print("\nEl IC para el desempleo: ", [int(LCi*1757161),int(LCs*1757161)])

# C1) Prueba de Hipótesis - Desempleo
zo = stats.norm.ppf(0.05)
ET = (7/100*(1-7/100)/PEA.sum())**0.5
RAi = 7/100+ET*zo
if td >= 7:
    print("\nLa tasa de desempleo aumentó respecto del 2021")
else:
    print("\nLa tasa de desempleo disminuyó respecto del 2021")
# C2) Prueba de Hipótesis - Salario
filtro1 = datos_csv[(PEA == 1) & (DESEMPLEO == 0) & (SEXO == 1)]
filtro2 = datos_csv[(PEA == 1) & (DESEMPLEO == 0) & (SEXO == 2)]
zo = stats.norm.ppf(1 - 0.01/2)
n1 = len(filtro1)
n2 = len(filtro2)
S1 = np.std(filtro1['Salario'])
S2 = np.std(filtro2['Salario'])
ET = (S1**2/n1+S2**2/n2)**0.5
RAi = 0-ET*zo
RAs = 0+ET*zo
m1 = np.mean(filtro1['Salario'])
m2 = np.mean(filtro2['Salario'])
if ((m1-m2 >= RAi) & (m1-m2 <= RAs)):
    print("\nLos salario de varones y mujeres son iguales")
else:
    print("\nLos salario de varones y mujeres son distintos")
