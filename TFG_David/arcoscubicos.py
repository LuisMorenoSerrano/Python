#
# Calculate nozzle first part based on cubic arcs
#
import numpy as np
import matplotlib.pyplot as plt

# Morel equations:
#   Calculate nozzle profile depending on normalized x,xm parameters (0.0...1.0)
def profile(Hi, He, xm, x):
    if x <= xm:
        y = (Hi - He) * (1 - (1 / xm ** 2) * (x) ** 3) + He
    else:
        y = (Hi - He) / (1 - xm) ** 2 * (1 - x) ** 3 + He

    return y

# Definition of nozzle configuration parameters
Ri = 0.85
Ro = 0.50
Xm = 0.60
L  = 1.60

plotting = True

# Calculate profile x,y coordinates
puntos = 1000
px = np.linspace(0.0, L, puntos)
r1 = [profile(Ri, Ro, Xm, x / L) for x in px]
r2 = [-1 * x for x in r1]

# Show graphics (if applicable)
if plotting:
    # Show 2D-Contour
    fig, ax = plt.subplots(figsize=(10, 10))

    ax.set_title('Tobera (Perfil)')
    ax.set_xticks(np.arange(0.0, L + 0.01, step=0.1))
    ax.set_yticks(np.arange(-1.0, 1.0, step=0.1))

    ax.axhline(y=0.0, xmin=0.0, xmax=L,
        color='grey', linewidth=0.8, linestyle='dashdot')

    ax.plot(px, r1, color='blue')
    ax.plot(px, r2, color='blue')
    ax.plot(Xm * L,  profile(Ri, Ro, Xm, Xm), 'o', color='red')
    ax.plot(Xm * L, -profile(Ri, Ro, Xm, Xm), 'o', color='red')

    plt.xlabel('Horizontal length (m)')
    plt.ylabel('Vertical length (m)')
    plt.title('Convergent part')
    plt.show()

    # Show 3D-Model
    X  = np.linspace(0.0, L, puntos)
    Th = np.linspace(0.0, 2 * np.pi, puntos)
    X, Th = np.meshgrid(X, Th)

    Y = r1 * np.cos(Th)
    Z = r1 * np.sin(Th)

    fig = plt.figure(figsize=(10, 10))
    ax  = fig.add_subplot(projection='3d')

    ax.set_title('Nozzle (3D-Model)')
    ax.set_xlim(0.0, 1.6)
    ax.set_ylim(-1.0, 1.0)
    ax.set_zlim(-1.0, 1.0)
    ax.set_xticks(np.arange(0.0, L + 0.1, 0.2))
    ax.set_yticks(np.arange(-1.0, 1.01, 0.2))
    ax.set_zticks(np.arange(-1.0, 1.01, 0.2))

    ax.autoscale_view()
    ax.set_aspect('equal')

    ax.plot_surface(X, Y, Z, vmin=Z.min() * 2)

    plt.show()
