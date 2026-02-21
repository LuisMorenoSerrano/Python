"""Operaciones con matrices y funciones de rendimiento."""

import time
import numpy as np
import matrix_ops  # Módulo Fortran compilado
from utils import print_progress_start, print_progress_end

def create_matrices(n):
    """Crea matrices para las operaciones NumPy y Fortran."""
    print_progress_start("Creando matrices", new_line=True)

    try:
        matrix_a = np.asfortranarray(np.random.rand(n, n).astype(np.float64))
        matrix_b = np.asfortranarray(np.random.rand(n, n).astype(np.float64))
        matrix_c_numpy = np.zeros((n, n), dtype=np.float64, order="C")
        matrix_c_fortran = np.zeros((n, n), dtype=np.float64, order="F")

        print_progress_end(True)

        return matrix_a, matrix_b, matrix_c_numpy, matrix_c_fortran
    except Exception as e:
        print_progress_end(False)

        raise e

def multiply_numpy(matrix_a, matrix_b, matrix_c_numpy):
    """Realiza la multiplicación de matrices con NumPy y mide el tiempo."""
    start_time = time.perf_counter()
    np.dot(matrix_a, matrix_b, out=matrix_c_numpy)
    end_time = time.perf_counter()

    return end_time - start_time

def multiply_fortran(matrix_a, matrix_b, matrix_c, n):
    """Realiza la multiplicación de matrices con Fortran y mide el tiempo."""
    start_time = time.perf_counter()
    matrix_ops.dot(matrix_a, matrix_b, matrix_c, n)  # pylint: disable=c-extension-no-member
    end_time = time.perf_counter()

    return end_time - start_time

def evaluate_performance(matrix_a, matrix_b, matrix_c_numpy, matrix_c_fortran, n):
    """Evalúa el rendimiento de ambos métodos de multiplicación."""
    print_progress_start("Realizando cálculos")

    try:
        time_numpy = multiply_numpy(matrix_a, matrix_b, matrix_c_numpy)
        time_fortran = multiply_fortran(matrix_a, matrix_b, matrix_c_fortran, n)

        print_progress_end(True)

        return time_numpy, time_fortran
    except Exception as e:
        print_progress_end(False)

        raise e
