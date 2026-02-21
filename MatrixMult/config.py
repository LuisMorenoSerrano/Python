"""Configuración global para las pruebas de multiplicación de matrices."""

import locale

# Configuración global
CONFIG = {
    "COMPARE_RESULTS": False,
    "DEFAULT_DIMENSION": 500,
    "LOCALE": "es_ES.UTF-8",
    "TOLERANCE_DATA": 1e-8,
    "TOLERANCE_TIME": 0.02,
}

# Símbolos para la interfaz de usuario
SYMBOLS = {
    "SUCCESS": "✅",
    "ERROR": "❌",
    "WARNING": "⚠️"
}

# Configurar localización
locale.setlocale(locale.LC_ALL, CONFIG["LOCALE"])
