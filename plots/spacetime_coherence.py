import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_spacetime_coherence_field(size=50, central_coherence=1.0, randomness_level=0.1):
    x = np.linspace(-5, 5, size)
    y = np.linspace(-5, 5, size)
    X, Y = np.meshgrid(x, y)

    coherence_base = central_coherence * np.exp(-(X**2 + Y**2) / 5)
    noise = randomness_level * np.random.rand(size, size)
    S_field_value = coherence_base + noise
    S_field_value = np.maximum(0, S_field_value)

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    surf = ax.plot_surface(X, Y, S_field_value, cmap='viridis', edgecolor='none')
    fig.colorbar(surf, shrink=0.5, aspect=5, label='Coherence Level ($\mathcal{S}$ Field)')

    ax.set_xlabel('Spatial Dimension 1')
    ax.set_ylabel('Spatial Dimension 2')
    ax.set_zlabel('Information Coherence ($\mathcal{S}$)')
    ax.set_title('Conceptual Spacetime Information Field Coherence')

    plt.show()

plot_spacetime_coherence_field(size=70, central_coherence=5.0, randomness_level=0.5)
plot_spacetime_coherence_field(size=70, central_coherence=2.0, randomness_level=0.1)
plot_spacetime_coherence_field(size=70, central_coherence=0.5, randomness_level=1.0)
