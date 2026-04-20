import matplotlib.pyplot as plt
import numpy as np


def warp(x, y, objmass, x0, y0):
    G = 4 * np.pi**2        # AU^3 / (M_sun * yr^2)
    r = np.sqrt((x-x0)**2 + (y-y0)**2 + 0.01**2)  # softening
    return (-G * objmass) / r

gridSize = 100
x, y = np.linspace(-5, 5, gridSize), np.linspace(-5, 5, gridSize)  # AU
XX, YY = np.meshgrid(x, y)

phi = warp(XX, YY, .01, 0, 0)  # 1 solar mass



fig = plt.figure(figsize=(20, 16))
ax = fig.add_subplot(111, projection='3d')
surface = ax.plot_surface(XX, YY, phi, cmap='hot', edgecolor='none')
plt.colorbar(surface, label='Φ (AU² yr⁻²)')
ax.set_zlim(phi.min(), phi.max())
ax.set_xlabel('Spatial Coordinate x, AU')
ax.set_ylabel('Spatial Coordinate y, AU')
ax.set_zlabel('Gravitational Potential Φ, normalized')
plt.title('Gravitational Potential of a Spherical Mass in 3D')
ax.view_init(elev=30, azim=135)
plt.show()
