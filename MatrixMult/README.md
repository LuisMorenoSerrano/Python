# MatrixMult

Performance comparison between matrix multiplication using NumPy and Fortran (BLAS).

## Description

This project (proof of concept) compares the performance of matrix multiplication using two implementations:

1. **NumPy**: Using the `numpy.dot()` function with optimized arrays
2. **Fortran+BLAS**: Using a Fortran subroutine that invokes `dgemm` from BLAS/LAPACK

The goal is to evaluate the performance differences between both approaches for large matrices, while also verifying the accuracy of the results.

## Project structure

```bash
MatrixMult/
├── config.py             # Global configuration
├── main.py               # Main program
├── matrix_info.py        # Functions to display matrix information
├── matrix_mod.f90        # Fortran implementation with BLAS
├── matrix_operations.py  # Matrix operations
├── result_analysis.py    # Result analysis
└── utils.py              # Utility functions
```

## Requirements

### Recommended development environment

To work with this project, a complete environment including Python (`>=v3.12`) and the following packages is recommended:

```bash
numpy>=2.2.5
matplotlib>=3.10.1
meson>=1.7.2
ninja>=1.11.1.4
pandas>=2.2.3
seaborn>=0.13.2
```

### System libraries

- **BLAS/LAPACK**: Optimized linear algebra libraries
- **gfortran**: Fortran compiler to compile the Fortran module

On Ubuntu-based systems, you can install dependencies with:

```bash
sudo apt-get install python3-numpy gfortran libblas-dev liblapack-dev
```

Or to use an optimized implementation:

```bash
sudo apt-get install python3-numpy gfortran libopenblas-dev
```

## VS Code recommendations

If you use Visual Studio Code for development, it is recommended to install the **Modern Fortran** extension to get:

1. Syntax highlighting for Fortran code
2. Code autocompletion and navigation
3. Code diagnostics and analysis
4. Integration with tools like fortls

You can install the extension from `Quick Open` (Ctrl+P) with the following command:

```bash
ext install fortran-lang.linter-gfortran
```

To further improve the development experience, install the following complementary tools:

```bash
pip install fortls findent
```

## Compilation

To compile the Fortran module, run:

```bash
f2py -m matrix_ops -c matrix_mod.f90 --f90flags="-O3 -march=native" -lopenblas
```

## Usage

To run the comparison with the default matrix size:

```bash
python main.py
```

### Arguments

- `-n, --size`: Dimension of the square matrices (default: 500)
- `-v, --verbose`: Display detailed matrix information
- `-c, --compare`: Compare NumPy and Fortran results to verify correctness

Examples:

```bash
# Use 1000x1000 matrices
python main.py -n 1000

# Display detailed information
python main.py -v

# Also verify result accuracy
python main.py -c

# Combination of arguments
python main.py -n 2000 -v -c
```

## Technical details

The Fortran implementation uses the `dgemm` routine from BLAS for matrix multiplication,
which is highly optimized for the underlying hardware. On the other hand, NumPy also uses
internally optimized implementations.

The code is designed to:

- Create matrices in the appropriate formats for each implementation (C-order for NumPy, F-order for Fortran)
- Pre-allocate result matrices to avoid memory allocations during computations
- Accurately measure execution time
- Provide detailed information about matrices and memory usage
- Compare results to verify numerical accuracy

## Performance

The relative performance between NumPy and Fortran can vary significantly depending on:

- Matrix size
- BLAS implementation used
- CPU architecture
- Amount of available memory

In general, for very large matrices, the Fortran+BLAS implementation tends to be competitive or outperform NumPy, especially when using an optimized implementation like OpenBLAS or Intel MKL.

## License

This project is distributed under the MIT license.
