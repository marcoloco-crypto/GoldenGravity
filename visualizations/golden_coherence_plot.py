import matplotlib.pyplot as plt
import numpy as np
import os

# Ensure output directory exists
output_dir = os.path.join(os.path.dirname(__file__), '../figures')
os.makedirs(output_dir, exist_ok=True)

# Definitive combined Golden Ratio and Pi factor
PHI_PI = 5.083203692

# Entanglement Density range for plotting
# Assuming D_ent is dimensionless and can vary between 0 and 0.1 for typical plots
D_ent = np.linspace(0, 0.1, 100)

# Calculate the coherence term: (1 + PHI_PI * D_ent)
# This represents the first term of the F_QC function (without the dark matter/energy part)
F_QC_entanglement_term = 1 + PHI_PI * D_ent

# --- Plotting ---
plt.figure(figsize=(10, 6))
plt.plot(D_ent, F_QC_entanglement_term, label=r'$1 + (\phi \cdot \pi) \cdot \mathcal{D}_{\text{ent}}$', color='gold')
plt.xlabel(r'Entanglement Density ($\mathcal{D}_{\text{ent}}$)')
plt.ylabel('Coherence Term Contribution')
plt.title(r'Golden Gravity: Quantum Coherence Scaling by $(\phi \cdot \pi)$')
plt.legend()
plt.grid(True)
plt.tight_layout()

# Save the plot
plot_filename = os.path.join(output_dir, 'golden_coherence.png')
plt.savefig(plot_filename)
plt.close() # Close the plot to free memory

print(f"Golden Coherence plot saved to: {plot_filename}")
print("visualizations/golden_coherence_plot.py complete.")
