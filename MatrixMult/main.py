"""
Programa principal que compara el rendimiento de la multiplicación de matrices
utilizando NumPy y una subrutina Fortran compilada con `f2py`.
"""

import argparse
from config import CONFIG
from utils import format_number, print_section_header
from matrix_operations import create_matrices, evaluate_performance
from matrix_info import matrix_info, show_total_memory
from result_analysis import print_execution_times, compare_results, compare_times

def parse_arguments():
    """Procesa argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(
        description="Comparación de multiplicación de matrices entre NumPy y Fortran"
    )

    parser.add_argument(
        "-n",
        "--size",
        type=int,
        default=CONFIG["DEFAULT_DIMENSION"],
        help=f'Dimensión de las matrices cuadradas (por defecto: {CONFIG["DEFAULT_DIMENSION"]})',
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Muestra información detallada de las matrices",
    )

    parser.add_argument(
        "-c",
        "--compare",
        action="store_true",
        default=CONFIG["COMPARE_RESULTS"],
        help="Compara los resultados de NumPy y Fortran para verificar su correctitud",
    )

    return parser.parse_args()

def main():
    """Función principal que coordina la ejecución del programa."""
    # Procesar argumentos de línea de comandos
    args = parse_arguments()
    n = args.size
    verbose = args.verbose
    compare = args.compare

    # Mensaje de inicio
    n_formatted = format_number(n)
    print_section_header("OPERACIÓN", new_line=False)
    print(f"Multiplicación de matrices {n_formatted} x {n_formatted}")

    # Generar matrices aleatorias
    matrix_a, matrix_b, matrix_c_numpy, matrix_c_fortran = create_matrices(n)

    # Realizar cálculos
    tiempo_numpy, tiempo_fortran = evaluate_performance(
        matrix_a, matrix_b, matrix_c_numpy, matrix_c_fortran, n
    )

    # Comparar resultados solo si se solicita explícitamente
    if compare:
        compare_results(matrix_c_numpy, matrix_c_fortran)

    # Mostrar información de las matrices si está en modo verbose
    if verbose:
        matrix_info(matrix_a, "A")
        matrix_info(matrix_b, "B")
        matrix_info(matrix_c_numpy, "C (NumPy)")
        matrix_info(matrix_c_fortran, "C (Fortran)")

        # Mostrar uso total de memoria
        matrices = [
            (matrix_a, "Matriz A"),
            (matrix_b, "Matriz B"),
            (matrix_c_numpy, "Matriz C (NumPy)"),
            (matrix_c_fortran, "Matriz C (Fortran)"),
        ]
        show_total_memory(matrices)

    # Mostrar resultados de tiempo y comparar
    print_execution_times(tiempo_numpy, tiempo_fortran)
    compare_times(tiempo_numpy, tiempo_fortran)

if __name__ == "__main__":
    main()
