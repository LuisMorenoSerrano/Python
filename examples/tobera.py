#
# Calculate and display nozzle according to configuration parameters
#
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # pylint: disable=unused-import

# Morel equations:
#   Calculate nozzle profile based on normalized x,xm parameters (0.0...1.0)
def profile(Hi, He, xm, x):
    if x <= xm:
        y = (Hi - He) * (1 - (1 / xm ** 2) * (x) ** 3) + He
    else:
        y = (Hi - He) / (1 - xm) ** 2 * (1 - x) ** 3 + He

    return y

# Define nozzle configuration parameters
Ri = 0.85
Ro = 0.50
Xm = 0.60
L  = 1.60

# Calculate profile x,y coordinates
points = 1000
px = np.linspace(0.0, L, points)
r1 = np.array([profile(Ri, Ro, Xm, x / L) for x in px])
r2 = -r1

# Display 2D contour
fig, ax = plt.subplots(figsize=(10, 10))
fig.suptitle('Nozzle (Profile)', fontsize=16)

ax.set_xticks(np.arange(0.0, L + 0.01, step=0.1))
ax.set_yticks(np.arange(-1.0, 1.0, step=0.1))

ax.axhline(y=0.0, xmin=0.0, xmax=L,
    color='grey', linewidth=0.8, linestyle='dashdot')

ax.plot(px, r1, color='blue')
ax.plot(px, r2, color='blue')
ax.plot(Xm * L,  profile(Ri, Ro, Xm, Xm), 'o', color='red')
ax.plot(Xm * L, -profile(Ri, Ro, Xm, Xm), 'o', color='red')

plt.title('Convergent part', fontsize=11)
plt.xlabel('Horizontal length (m)')
plt.ylabel('Vertical length (m)')
plt.show()

# Display 3D model
X = np.linspace(0.0, L, points)
Th = np.linspace(0.0, 2 * np.pi, points)
X, Th = np.meshgrid(X, Th)

Y = r1 * np.cos(Th)
Z = r1 * np.sin(Th)

fig = plt.figure(figsize=(10, 10))
fig.suptitle('Nozzle (3D Model)', fontsize=16)

ax = fig.add_subplot(111, projection='3d')

ax.set_xlim(0.0, 1.6)
ax.set_ylim(-1.0, 1.0)
ax.set_zlim(-1.0, 1.0) # type: ignore
ax.set_xticks(np.arange(0.0, L + 0.1, 0.2))
ax.set_yticks(np.arange(-1.0, 1.01, 0.2))
ax.set_zticks(np.arange(-1.0, 1.01, 0.2)) # type: ignore

ax.autoscale_view()
ax.set_box_aspect((1, 1, 1))  # type: ignore

ax.plot_surface(X, Y, Z, cmap='viridis') # type: ignore

plt.show()
