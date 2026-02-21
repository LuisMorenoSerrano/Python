"""Funciones de utilidad generales."""

import locale
from config import SYMBOLS

def format_number(number):
    """Formatea un número con separador de miles según la configuración regional."""
    return locale.format_string("%d", number, grouping=True)

def print_section_header(title, char="=", new_line=True):
    """Imprime un encabezado de sección con formato consistente."""
    print(f"{'\n' if new_line else ''}{title}")
    print(char * len(title))

def print_progress_start(message, width=22, new_line=False):
    """Inicia un mensaje de progreso sin completarlo."""
    print(f"{'\n' if new_line else ''}{message:<{width}}...", end="", flush=True)

def print_progress_end(success=True):
    """Completa un mensaje de progreso con el símbolo correspondiente."""
    symbol = SYMBOLS["SUCCESS"] if success else SYMBOLS["ERROR"]
    print(f" {symbol}")

def get_contiguous_type(matrix):
    """Devuelve una descripción del tipo contiguo de una matriz."""
    if matrix.flags.c_contiguous:
        return "C (por filas)"

    if matrix.flags.f_contiguous:
        return "Fortran (por columnas)"

    return "No contiguo"
