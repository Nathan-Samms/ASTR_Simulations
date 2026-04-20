import matplotlib.pyplot as plt
import numpy as np

#Gravitational Constant (6.6743*10^-11 m^3kg^-1s^-2)
G = 4 * np.pi**2
objmass = 1 #In solar masses

tgt = np.array([0,0])
eps = 0.01

X, Y = np.linspace(-1, 1, 500), np.linspace(-1, 1, 500)  # In AU
XX, YY = np.meshgrid(X, Y)
phi = (-G * objmass) / np.sqrt((XX-tgt[0])**2 + (YY-tgt[1])**2 + eps**2)

plt.figure(figsize=(6, 6))
plt.pcolormesh(X, Y, phi, cmap='hot', shading='auto')
plt.colorbar(label='Φ (AU² yr⁻²)')
plt.xlabel('x (AU)')
plt.ylabel('y (AU)')
plt.title(f'Gravitational Potential — M = {objmass} M☉')
plt.show()