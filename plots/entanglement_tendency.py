import numpy as np
import matplotlib.pyplot as plt

def plot_entanglement_tendency(num_points=1000):
    prop1 = np.random.rand(num_points) * 10
    prop2 = np.random.rand(num_points) * 10

    phi = (1 + np.sqrt(5)) / 2

    ratio = np.where(prop2 != 0, prop1 / prop2, np.inf)

    proximity_to_phi = 1 / (1 + np.abs(ratio - phi))
    proximity_to_inv_phi = 1 / (1 + np.abs(ratio - 1/phi))

    coherence_score = np.maximum(proximity_to_phi, proximity_to_inv_phi)

    plt.figure(figsize=(9, 7))
    scatter = plt.scatter(prop1, prop2, c=coherence_score, cmap='plasma', s=50, alpha=0.7)
    plt.colorbar(scatter, label='Conceptual Entanglement/Coherence Tendency (closer to $\phi$ resonance)')
    plt.xlabel('Conceptual Property 1 (e.g., Quantum State A)')
    plt.ylabel('Conceptual Property 2 (e.g., Quantum State B)')
    plt.title('Conceptual Entanglement Tendency in Phase Space (Phi-Resonance)')
    plt.grid(True, linestyle=':', alpha=0.6)

    x_line = np.linspace(0, 10, 100)
    plt.plot(x_line, x_line / phi, 'r--', label=f'Ratio = 1/$\phi$ ({1/phi:.2f})')
    plt.plot(x_line, x_line * phi, 'g--', label=f'Ratio = $\phi$ ({phi:.2f})')
    plt.legend()
    plt.show()

plot_entanglement_tendency(num_points=5000)
