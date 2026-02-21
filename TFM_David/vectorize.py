import numpy as np

# Crear un array bidimensional de ejemplo
array = np.array([[ 1,  2,  3,  4,  5],
                  [ 6,  7,  8,  9, 10],
                  [11, 12, 13, 14, 15],
                  [16, 17, 18, 19, 20],
                  [21, 22, 23, 24, 25]])

# Inicializar los bordes con ceros para facilitar los desplazamientos
array_expandido = np.pad(array, pad_width=1, mode='constant', constant_values=0)

# Calcular los vecinos a la izquierda y a la derecha
vecinos_izquierda = array_expandido[:, :-2]  # Desplazar una columna a la izquierda
vecinos_derecha   = array_expandido[:, 2:]   # Desplazar una columna a la derecha

# Sumar los valores del elemento actual y sus vecinos
vecinos = array_expandido[:, 1:-1] + vecinos_izquierda + vecinos_derecha

# Mostrar los resultados
print("Array original:")
print(array)

print("\nSuma de los elementos y sus vecinos:")
print(vecinos)
