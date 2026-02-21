# Ajustando una curva de datos
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Datos
x = np.array([1, 2, 3, 4, 5])
y = np.array([1.1, 3.5, 7.2, 13.1, 21.3])

# Función a ajustar
def func(p_x, p_a, p_b, p_c):
    return p_a * p_x**2 + p_b * p_x + p_c

# Ajuste
popt, pcov, *rest = curve_fit(func, x, y)

# Coeficientes
a, b, c = popt

# Gráfica
plt.plot(x, y, 'ro', label='Datos')
plt.plot(x, func(x, a, b, c), label='Ajuste')
plt.legend()
plt.show()
