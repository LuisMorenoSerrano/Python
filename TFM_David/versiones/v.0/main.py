import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.lines import Line2D
from matplotlib import gridspec
import matplotlib.dates as mdates
from mpl_toolkits.axes_grid1 import AxesGrid
import matplotlib
from matplotlib.ticker import MaxNLocator
from matplotlib.lines import Line2D
import matplotlib.animation as animation
import os
import subprocess
from tqdm import tqdm
import time

# Matplotlib config
# LaTeX sizes
pt=1/72 # inch/pt

elsevierSingleColumn = 222
elsevierSingleHalfColumn = 397.0
elsevierDoubleColumn = 468

def heightFig(width, aspectRatio = 4/3):
    return width/aspectRatio

elsevierOneColumnWidth=345.0 
elsevierTwoColumnWidth=222.0 

oneColumnFig=elsevierSingleColumn*pt, heightFig(elsevierSingleColumn*pt, aspectRatio=7/5)
doubleColumnFig=elsevierDoubleColumn*pt, heightFig(elsevierSingleColumn*pt, aspectRatio=7/5)
triFigure = elsevierOneColumnWidth*pt, heightFig(elsevierSingleColumn*pt, aspectRatio=7/5)

twoParallelFig = 539/2.5*pt, heightFig(539/2.5*pt)

width_pt = 472.03123
width_inch = width_pt / 72.0
height_inch = width_inch * 0.6

size = [width_inch, height_inch]

# When exporting files
transparent=True
ext='pdf'
# matplotlib.use('pgf')
matplotlib.rcParams.update({
    'figure.autolayout': True,
    'pgf.texsystem': 'pdflatex',
    'text.usetex': True,
    'pgf.rcfonts': False,
    'savefig.format': ext,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.05,
})

# Plot content
lineWidth=1.5
markerSize=3
matplotlib.rcParams.update({
    'axes.labelsize': 'small', # default 'medium'
    'figure.titlesize': 'medium',    # default 'large'
    'font.family': 'serif',
    'font.size': 13, # default 10
    'legend.fontsize': 'small', # default 'medium',
    'legend.frameon': False,
    'lines.markersize': markerSize,
    'lines.markerfacecolor': 'none',
    'lines.linewidth': lineWidth,
    'xtick.labelsize': 'small', # default 'medium'
    'xtick.direction': 'in',
    'xtick.bottom': True,
    'xtick.top': True,
    'xtick.minor.visible': True,
    'ytick.labelsize': 'small', # default 'medium'
    'ytick.direction': 'in',
    'ytick.left': True,
    'ytick.right': True,
})

# --- PARÁMETROS ---
a2 = 0.1
tau = 0.005
a = -1
b = 1
N = 20
timesteps = 200

# --- EJECUTAR FORTRAN ---
os.makedirs("Datos", exist_ok=True)
os.makedirs("Figuras", exist_ok=True)
print("Ejecutando Fortran...")
start_fortran = time.perf_counter()
subprocess.run(["./solver", str(a2), str(tau), str(a), str(b), str(N), str(timesteps)])
end_fortran = time.perf_counter()
print(f"⏱️ Tiempo Fortran: {end_fortran - start_fortran:.3f} segundos")

# --- CARGAR RESULTADO ---
print("Cargando datos...")
start_load = time.perf_counter()
u_sol = np.loadtxt("Datos/u_sol.txt")
x = np.loadtxt("Datos/x.txt")
end_load = time.perf_counter()
print(f"⏱️ Tiempo carga de datos: {end_load - start_load:.3f} segundos")

# --- PLOTS ---
start_plot = time.perf_counter()
plt.figure(figsize=(size[0] * 1.3, size[1]))
timesteps_to_plot = np.unique(np.logspace(0, np.log10(timesteps), num=15, dtype=int)) - 1
colors = sns.color_palette("Reds_d", n_colors=len(timesteps_to_plot))[::-1]
for t, color in zip(timesteps_to_plot, colors):
    sns.lineplot(x=x, y=u_sol[t], color=color)
plt.xlabel("x", fontsize=14)
plt.ylabel("u(x, t)", fontsize=14)
n = len(colors)
legend_elements = [
    Line2D([0], [0], color=colors[0], lw=2, label=r"$t_0 = 0$"),
    Line2D([0], [0], color=colors[n//5], lw=2),
    Line2D([0], [0], color=colors[2*n//5], lw=2),
    Line2D([0], [0], color=colors[3*n//5], lw=2),
    Line2D([0], [0], color=colors[4*n//5], lw=2),
    Line2D([0], [0], color=colors[-1], lw=2, label=fr"$t_f = {tau * timesteps:.2f}$")
]
plt.legend(title= fr"$\textbf{{u}}$", handles=legend_elements, loc="upper right", bbox_to_anchor=(1.2, 0.65), labelspacing=0.2, handlelength=2, handletextpad=0.5, borderpad=0.3, fontsize=10)
plt.text(1.1, 0.94, fr"$\underline{{\textbf{{Parámetros}}}}$" "\n" fr"$NN = {2*N + 1}$" "\n" fr"$a_2 = {a2}$" "\n" fr"$\tau = {tau}$", 
    transform=plt.gca().transAxes, fontsize=12, va="top", ha="center")
plt.grid(color='gray', linestyle='--', linewidth=0.5)
plt.savefig("Figuras/opendomain_cte_evolucion.pdf")

plt.figure(figsize=(size[0] * 1.3, size[1]))
T, X = np.meshgrid(np.arange(timesteps) * tau, x)
contour = plt.contourf(X, T, u_sol.T, cmap="Reds", levels=50)
cbar = plt.colorbar(contour)
cbar.ax.tick_params(labelsize=10)
cbar.set_label("u", fontsize=12, rotation=0, labelpad=20)
plt.xlabel("x", fontsize=14)
plt.ylabel("t", fontsize=14)
contour_lines = plt.contour(X, T, u_sol.T, colors='black', linewidths=0.5)
plt.clabel(contour_lines, inline=True, fontsize=8, fmt='%1.2f')
plt.savefig("Figuras/opendomain_cte_contour.pdf")

end_plot = time.perf_counter()

total = end_plot - start_fortran
print(f"\n✅ Tiempo total del proceso: {total:.3f} segundos")

# --- ANIMACIÓN ---
# start_anim = time.perf_counter()
# frames_to_use = range(len(u_sol))
# fig, ax = plt.subplots(figsize=(width_inch, height_inch), facecolor='white') 
# line, = ax.plot(x, u_sol[0], label="Evolución de u(x, t)", lw=2, color='indianred')
# time_text = ax.text(0.05, 0.95, '', transform=ax.transAxes, fontsize=12, va='top')
# ax.set_xlabel("x", fontsize=14)
# ax.set_ylabel("u(x, t)", fontsize=14)
# ax.set_ylim(0, 0.15)  
# ax.grid(color='gray', linestyle='--', linewidth=0.5)
# progress_bar = tqdm(total=len(u_sol), desc="🎞️ Generando animación", unit="frame")
# def update(frame):
#     line.set_ydata(u_sol[frame])
#     time_text.set_text(f"t = {frame * tau:.2f}")
#     time_text.set_bbox(dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'))
#     progress_bar.update(1)
#     return [line, time_text] 
# ani = animation.FuncAnimation(
#     fig, update, frames=frames_to_use, blit=True
# )
# print("⏳ Procesando frames...")
# ani.save("Figuras/ani.mp4", writer="ffmpeg", fps=20)
# progress_bar.close()
# end_anim = time.perf_counter()
# print(f"⏱️ Tiempo generación de la animación: {end_anim - start_anim:.3f} segundos")
# plt.show()
# total = end_anim - start_fortran
# print(f"\n✅ Tiempo total del proceso: {total:.3f} segundos")