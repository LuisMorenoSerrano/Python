import os
import re
import sys
import time

import matplotlib
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm


def setup_matplotlib_config():
    """Configurar matplotlib para gráficos de calidad publicable"""
    # Dimensiones para figuras
    width_pt = 472.03123
    width_inch = width_pt / 72.0
    height_inch = width_inch * 0.6

    # Configuración global de matplotlib
    matplotlib.rcParams.update(
        {
            "figure.autolayout": True,
            "pgf.texsystem": "pdflatex",
            "text.usetex": True,
            "pgf.rcfonts": False,
            "savefig.format": "pdf",
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.05,
            "axes.labelsize": "small",
            "figure.titlesize": "medium",
            "font.family": "serif",
            "font.size": 13,
            "legend.fontsize": "small",
            "legend.frameon": False,
            "lines.markersize": 3,
            "lines.markerfacecolor": "none",
            "lines.linewidth": 1.5,
            "xtick.labelsize": "small",
            "xtick.direction": "in",
            "xtick.bottom": True,
            "xtick.top": True,
            "xtick.minor.visible": True,
            "ytick.labelsize": "small",
            "ytick.direction": "in",
            "ytick.left": True,
            "ytick.right": True,
        }
    )

    return width_inch, height_inch


def extract_tau_from_sim(sim_path):
    """Extraer el parámetro tau del archivo sim.txt"""
    try:
        with open(sim_path, "r") as f:
            contenido = f.read()

        match_tau = re.search(r"tau\s*=\s*([0-9.eE+-]+)", contenido)
        if not match_tau:
            raise ValueError("No se encontró 'tau' en sim.txt")

        tau = float(match_tau.group(1))
        print(f"🔍 Parámetro extraído: tau = {tau}")
        return tau
    except Exception as e:
        print(f"❌ Error al extraer tau: {e}")
        sys.exit(1)


def load_data(version_path):
    """Cargar los datos de coordenadas x y soluciones u"""
    ruta_x = os.path.join(version_path, "x.txt")

    # Verificar archivo de coordenadas
    if not os.path.isfile(ruta_x):
        print(f"❌ No se encontró el archivo de coordenadas x: {ruta_x}")
        sys.exit(1)

    # Cargar coordenadas x
    x = np.loadtxt(ruta_x)

    # Encontrar archivos de solución
    archivos_u = sorted(
        [
            f
            for f in os.listdir(version_path)
            if re.match(r"u.*\.txt$", f) and f != "x.txt"
        ]
    )

    if not archivos_u:
        print(f"❌ No se encontraron archivos tipo 'u*.txt' en {version_path}")
        sys.exit(1)

    # Cargar datos de solución
    print("📥 Cargando datos...")
    ruta_u = os.path.join(version_path, archivos_u[0])
    try:
        u_sol = np.loadtxt(ruta_u)
        print(f"✓ Datos cargados: {u_sol.shape}")

        # Asegurar dimensión correcta para animación
        if u_sol.ndim == 1:
            u_sol = np.expand_dims(u_sol, axis=0)

        return x, u_sol
    except Exception as e:
        print(f"❌ Error al cargar datos: {e}")
        sys.exit(1)


def create_animation(x, u_sol, tau, width_inch, height_inch):
    """Crear animación de la solución"""
    frames_to_use = range(len(u_sol))
    fig, ax = plt.subplots(figsize=(width_inch, height_inch), facecolor="white")

    # Configurar elementos gráficos
    (line,) = ax.plot(
        x, u_sol[0], label="Evolución de u(x, t)", lw=2, color="indianred"
    )
    time_text = ax.text(0.05, 0.95, "", transform=ax.transAxes, fontsize=12, va="top")

    # Configurar ejes y límites
    ax.set_xlabel("x", fontsize=14)
    ax.set_ylabel("u(x, t)", fontsize=14)
    ax.set_ylim(np.min(u_sol) * 0.95, np.max(u_sol) * 1.05)
    ax.grid(color="gray", linestyle="--", linewidth=0.5)

    # Barra de progreso y función de actualización
    progress_bar = tqdm(total=len(u_sol), desc="🎞️ Generando animación", unit="frame")

    def update(frame):
        line.set_ydata(u_sol[frame])
        time_text.set_text(f"t = {frame * tau:.2f}")
        time_text.set_bbox(
            dict(
                facecolor="white",
                alpha=0.7,
                edgecolor="black",
                boxstyle="round,pad=0.3",
            )
        )
        progress_bar.update(1)
        return [line, time_text]

    # Crear animación
    ani = animation.FuncAnimation(fig, update, frames=frames_to_use, blit=True)

    return ani, progress_bar, fig


def save_animation(ani, output_path, fps=60):
    """Guardar la animación al disco"""
    # Crear directorio de salida si no existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Codecs y parámetros optimizados para calidad/tamaño
    ani.save(
        output_path,
        writer="ffmpeg",
        fps=fps,
        extra_args=[
            "-vcodec",
            "libx264",
            "-preset",
            "fast",
            "-crf",
            "22",
            "-threads",
            "4",
            "-pix_fmt",
            "yuv420p",
        ],
    )  # Compatibilidad con más reproductores

    print(f"✅ Animación guardada en: {output_path}")


def main():
    # Verificar argumentos de la línea de comandos
    if len(sys.argv) < 3:
        print("❌ Uso: python animar.py <versión> <nombre_animación>")
        sys.exit(1)

    # Obtener argumentos
    version = sys.argv[1]
    nombre_anim = sys.argv[2]

    # Configurar matplotlib
    width_inch, height_inch = setup_matplotlib_config()

    # Rutas
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    ruta_version = os.path.join(base_dir, "versiones", version, "Datos")
    ruta_sim = os.path.join(ruta_version, "sim.txt")

    # Verificar existencia del archivo de simulación
    if not os.path.isfile(ruta_sim):
        print(f"❌ No se encontró el archivo sim.txt en {ruta_version}")
        sys.exit(1)

    # Extraer parámetros y cargar datos
    tau = extract_tau_from_sim(ruta_sim)
    x, u_sol = load_data(ruta_version)

    # Crear y guardar animación
    start_anim = time.perf_counter()

    ani, progress_bar, fig = create_animation(x, u_sol, tau, width_inch, height_inch)

    # Ruta de salida
    salida_dir = os.path.join(os.path.dirname(__file__), "salida")
    ruta_salida = os.path.join(salida_dir, nombre_anim)

    # Guardar animación
    save_animation(ani, ruta_salida)

    # Cerrar recursos
    progress_bar.close()
    plt.close(fig)

    # Mostrar tiempo de ejecución
    end_anim = time.perf_counter()
    print(
        f"\n⏱️ Tiempo generación de la animación: {end_anim - start_anim:.3f} segundos"
    )


if __name__ == "__main__":
    main()
