#
# Sistema de Liberación de Fármacos
#
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Definición de funciones
#

# Ley de Lambert-Beer: A = Ɛbc <=> c = A/(Ɛb)
def f_lambert_beer_c(p_a, p_epsilon, p_b):
    return p_a / (p_epsilon * p_b)

# Modelo Higuchi: C = k * (t ^ 0,5)
def f_higuchi(p_t, p_k):
    return p_k * p_t**0.5

# Modelo Korsmeyer-Peppas: C = k * (t ^ n)
def f_korsmeyer_peppas(p_t, p_k, p_n):
    return p_k * p_t**p_n

# Datos experimentales:
#
# Ɛ: Absortividad molar (l/mol.cm)
# b: Longitud cubeta (cm)
# t: Tiempo (min)
# a: Absorción de la luz de la solución
# c: Concentración soluto (mol/l)
#
epsilon = 13900
b       = 1
t       = np.array(np.arange(0.0, 34.0, 2.0))
a       = np.array([
            0.001, 0.015, 0.014, 0.011, 0.013, 0.018,
            0.013, 0.018, 0.034, 0.035, 0.046, 0.050,
            0.053, 0.055, 0.060, 0.066, 0.066
            ])
c       = f_lambert_beer_c(a, epsilon, b)

# Ajustar datos experimentales a modelos teóricos y obtener parámetros de ajuste
popt1, *rest = curve_fit(f_higuchi, t, c)
popt2, *rest = curve_fit(f_korsmeyer_peppas, t, c)

k1    = popt1[0]
k2, n = popt2

print(" c: ", c)
print("k1: ", k1)
print("k2: ", k2)
print(" n: ", n)

# Mostrar resultados
plt.plot(t, c, 'ro', label='Datos')
plt.plot(t, f_higuchi(t, k1), label='Higuchi')
plt.plot(t, f_korsmeyer_peppas(t, k2, n), label='Korsmeyer-Peppas')
plt.legend()
plt.show()
