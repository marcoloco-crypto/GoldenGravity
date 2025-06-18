import numpy as np
import matplotlib.pyplot as plt
import os

# --- Constants ---
phi = (1 + np.sqrt(5)) / 2  # Golden Ratio
PHI_PI = phi * np.pi        # Golden Ratio amplified by Pi (approx 5.083203692)

# --- Conceptual Gravitational Modulation Function ---
def calculate_gravitational_modulation(entanglement_density):
    """
    Calculates a conceptual 'gravitational modulation factor'.
    This factor represents how spacetime's properties (like local gravity)
    might be influenced or 'modulated' by entanglement density, amplified
    by the fundamental PHI_PI constant from Golden Gravity.

    A higher entanglement_density leads to a stronger modulation.
    The '1 +' ensures a baseline and 'PHI_PI' is the core amplification.
    """
    # This directly uses the (1 + PHI_PI * D_ent) form, similar to a part of F_QC
    modulation_factor = 1 + PHI_PI * entanglement_density
    return modulation_factor

# --- Simulation Parameters ---
# Range of entanglement density to explore (dimensionless, e.g., normalized)
# From very low to a conceptual 'high' entanglement state.
entanglement_densities = np.linspace(0, 0.2, 100) # Range from 0 to 0.2, 100 points

# --- Calculate Modulation Factors ---
modulation_factors = [calculate_gravitational_modulation(d_ent) for d_ent in entanglement_densities]

# --- Plotting Results ---
plt.figure(figsize=(10, 6))

# Ensure output directory exists and is correct
output_dir = os.path.join(os.path.dirname(__file__), '../figures')
os.makedirs(output_dir, exist_ok=True)

plt.plot(entanglement_densities, modulation_factors, color='teal', linewidth=2)
plt.xlabel(r'Entanglement Density ($\mathcal{D}_{\text{ent}}$)')
plt.ylabel('Gravitational Modulation Factor')
plt.title(r'Conceptual Gravitational Modulation by Entanglement ($\phi \cdot \pi$ influence)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.axhline(y=1.0, color='gray', linestyle=':', label='Baseline (no modulation)')
plt.legend()
plt.tight_layout()

# Save the plot to the correct figures directory
plot_filename = os.path.join(output_dir, 'gravitational_modulator.png')
plt.savefig(plot_filename)
plt.close() # Close the plot to free memory

print(f"Conceptual Gravitational Modulator plot saved to: {plot_filename}")
print("gravitational_modulator_sim.py rewritten and complete.")
