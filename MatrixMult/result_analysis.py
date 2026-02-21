"""Funciones para analizar y comparar resultados."""

import numpy as np
from config import CONFIG, SYMBOLS
from utils import print_section_header, print_progress_start, print_progress_end

def print_execution_times(time_numpy, time_fortran):
    """Imprime los tiempos de ejecución con formato consistente."""
    print_section_header("TIEMPOS DE EJECUCIÓN")
    print(f"NumPy   (np.dot)........: {time_numpy:.6f} segundos")
    print(f"Fortran (matrix_ops.dot): {time_fortran:.6f} segundos")

def compare_results(matrix_c_numpy, matrix_c_fortran, tolerance=None):
    """Compara los resultados de NumPy y Fortran para verificar su correctitud."""
    print_progress_start("Comparando resultados")

    if tolerance is None:
        tolerance = CONFIG["TOLERANCE_DATA"]

    all_close = np.allclose(matrix_c_numpy, matrix_c_fortran, atol=tolerance)

    print_progress_end(success=all_close)
    print_section_header("COMPARACIÓN DE RESULTADOS")

    if all_close:
        print("Resultados de NumPy y Fortran coincidentes (dentro de tolerancia).")
    else:
        max_diff = np.max(np.abs(matrix_c_numpy - matrix_c_fortran))
        print(f"{SYMBOLS['WARNING']} ¡Atención! Resultados de NumPy y Fortran NO coincidentes.")
        print(f"Diferencia máxima: {max_diff:.6e}")

def compare_times(time_numpy, time_fortran, tolerance=None):
    """Compara los tiempos de ejecución de NumPy y Fortran."""
    if tolerance is None:
        tolerance = CONFIG["TOLERANCE_TIME"]

    ratio = time_numpy / time_fortran

    if abs(ratio - 1.0) <= tolerance:
        print("\nLos tiempos de ejecución de NumPy y Fortran fueron similares.")
    elif ratio > 1.0:
        print(f"\nFortran fue {ratio:.2f} veces más rápido que NumPy.")
    else:
        print(f"\nNumPy fue {1/ratio:.2f} veces más rápido que Fortran.")
