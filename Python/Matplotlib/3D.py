import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style

# --- data for scatter ---
rng = np.random.default_rng(seed=1)
x = rng.random(100)
y = rng.random(100)
z = rng.random(100)

# --- data for surface ---
x1 = np.arange(-5, 5, 0.1)
y1 = np.arange(-5, 5, 0.1)
X1, Y1 = np.meshgrid(x1, y1)
Z1 = np.sin(X1) * np.cos(Y1)

# --- create figure with two 3D subplots side-by-side ---
fig = plt.figure(figsize=(14, 6))

ax1 = fig.add_subplot(1, 2, 1, projection='3d')  # left: scatter
sc = ax1.scatter(x, y, z, c=z, cmap='viridis', s=35, depthshade=True)
ax1.set_title("3D Scatter")
ax1.set_xlabel("X")
ax1.set_ylabel("Y")
ax1.set_zlabel("Z")
fig.colorbar(sc, ax=ax1, shrink=0.6, pad=0.1, label='z value')

ax2 = fig.add_subplot(1, 2, 2, projection='3d')  # right: surface
surf = ax2.plot_surface(X1, Y1, Z1, cmap='viridis', alpha=0.9, linewidth=0, antialiased=True)
ax2.set_title("3D Surface")
ax2.set_xlabel("X")
ax2.set_ylabel("Y")
ax2.set_zlabel("Z")
fig.colorbar(surf, ax=ax2, shrink=0.6, pad=0.1, label='Z value')

# Attempt to make axes proportions readable (works on Matplotlib 3.3+)
for ax in (ax1, ax2):
    try:
        ax.set_box_aspect((1, 1, 0.6))  # tweak the z-scale a little for visibility
    except Exception:
        pass

fig.tight_layout()
plt.show()
