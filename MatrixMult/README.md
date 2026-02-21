# MatrixMult

Comparación de rendimiento entre multiplicación de matrices usando NumPy y Fortran (BLAS).

## Descripción

Este proyecto (prueba de concepto) compara el rendimiento de multiplicación de matrices usando dos implementaciones:

1. **NumPy**: Usando la función `numpy.dot()` con matrices optimizadas
2. **Fortran+BLAS**: Usando una subrutina Fortran que invoca a `dgemm` de BLAS/LAPACK

El objetivo es evaluar las diferencias de rendimiento entre ambos enfoques para matrices grandes, verificando además la precisión de los resultados.

## Estructura del proyecto

```bash
MatrixMult/
├── config.py             # Configuración global
├── main.py               # Programa principal
├── matrix_info.py        # Funciones para mostrar información de matrices
├── matrix_mod.f90        # Implementación Fortran con BLAS
├── matrix_operations.py  # Operaciones con matrices
├── result_analysis.py    # Análisis de resultados
└── utils.py              # Funciones de utilidad
```

## Requisitos

### Entorno de desarrollo recomendado

Para trabajar con este proyecto, se recomienda un entorno completo que incluya Python (`>=v3.12`) y los paquetes:

```bash
numpy>=2.2.5
matplotlib>=3.10.1
meson>=1.7.2
ninja>=1.11.1.4
pandas>=2.2.3
seaborn>=0.13.2
```

### Bibliotecas del sistema

- **BLAS/LAPACK**: Bibliotecas de álgebra lineal optimizadas
- **gfortran**: Compilador Fortran para compilar el módulo Fortran

En sistemas basados en Ubuntu, puedes instalar las dependencias con:

```bash
sudo apt-get install python3-numpy gfortran libblas-dev liblapack-dev
```

O para usar una implementación optimizada:

```bash
sudo apt-get install python3-numpy gfortran libopenblas-dev
```

## Recomendaciones para VS Code

Si utilizas Visual Studio Code para el desarrollo, se recomienda instalar la extensión **Modern Fortran** para obtener:

1. Resaltado de sintaxis para código Fortran
2. Autocompletado y navegación de código
3. Diagnósticos y análisis de código
4. Integración con herramientas como fortls

Puedes instalar la extensión desde `Quick Open` (Ctrl+P) y el siguiente comando:

```bash
ext install fortran-lang.linter-gfortran
```

Para mejorar aún más la experiencia de desarrollo, instala las siguientes herramientas complementarias:

```bash
pip install fortls findent
```

## Compilación

Para compilar el módulo Fortran, ejecuta:

```bash
f2py -m matrix_ops -c matrix_mod.f90 --f90flags="-O3 -march=native" -lopenblas
```

## Uso

Para ejecutar la comparación con el tamaño de matriz predeterminado:

```bash
python main.py
```

### Argumentos

- `-n, --size`: Dimensión de las matrices cuadradas (por defecto: 500)
- `-v, --verbose`: Muestra información detallada de las matrices
- `-c, --compare`: Compara los resultados de NumPy y Fortran para verificar su correctitud

Ejemplos:

```bash
# Usar matrices 1000x1000
python main.py -n 1000

# Mostrar información detallada
python main.py -v

# Verificar también la precisión de los resultados
python main.py -c

# Combinación de argumentos
python main.py -n 2000 -v -c
```

## Detalles técnicos

La implementación de Fortran utiliza la rutina `dgemm` de BLAS para la multiplicación de matrices,
que está altamente optimizada para el hardware subyacente. Por otro lado, NumPy también utiliza
implementaciones optimizadas internamente.

El código está diseñado para:

- Crear matrices en los formatos adecuados para cada implementación (orden C para NumPy, orden F para Fortran)
- Preasignar matrices de resultado para evitar asignaciones de memoria durante los cálculos
- Medir con precisión el tiempo de ejecución
- Proporcionar información detallada sobre las matrices y el uso de memoria
- Comparar resultados para verificar la precisión numérica

## Rendimiento

El rendimiento relativo entre NumPy y Fortran puede variar significativamente dependiendo de:

- El tamaño de las matrices
- La implementación de BLAS utilizada
- La arquitectura del CPU
- La cantidad de memoria disponible

En general, para matrices muy grandes, la implementación con Fortran+BLAS tiende a ser competitiva o superar a NumPy, especialmente cuando se usa una implementación optimizada como OpenBLAS o Intel MKL.

## Licencia

Este proyecto se distribuye bajo la licencia MIT.
