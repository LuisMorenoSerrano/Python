"""Funciones para mostrar información sobre matrices."""

from utils import format_number, print_section_header, get_contiguous_type

def matrix_info(matrix, name):
    """Muestra información detallada sobre una matriz NumPy."""
    size_bytes = matrix.nbytes
    size_mb = size_bytes / (1024 * 1024)
    elements = matrix.size
    shape = matrix.shape
    dtype = matrix.dtype
    element_size = matrix.itemsize

    title = f"INFORMACIÓN MATRIZ: {name}"
    print_section_header(title)

    print("  - Dimensiones...: ", end="")
    print(f"{format_number(shape[0])} x {format_number(shape[1])}")
    print(f"  - Elementos.....: {format_number(elements)}")
    print(f"  - Tipo Dato.....: {dtype} ({element_size} bytes/elemento)")
    print("  - Tamaño Memoria: ", end="")
    print(f"{size_mb:.2f} MB ({format_number(size_bytes)} bytes)")
    print("  - Tipo contiguo.: ", end="")
    print(f"{get_contiguous_type(matrix)}")
    print(
        f"  - Otros flags...: "
        f"OWNDATA={matrix.flags.owndata}, "
        f"WRITEABLE={matrix.flags.writeable}, "
        f"ALIGNED={matrix.flags.aligned}"
    )

def show_total_memory(matrices):
    """Muestra el uso total de memoria de un conjunto de matrices."""
    total_mb = 0
    max_name_length = max(len(name) for _, name in matrices)

    print_section_header("USO DE MEMORIA")

    for matrix, name in matrices:
        size_mb = matrix.nbytes / (1024 * 1024)
        total_mb += size_mb
        print(f"{name:.<{max_name_length}}: {size_mb:>8.2f} MB")

    print(f"{'Total':.<{max_name_length}}: {total_mb:>8.2f} MB")
