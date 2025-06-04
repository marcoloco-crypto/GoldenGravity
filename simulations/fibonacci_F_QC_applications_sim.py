import numpy as np
import matplotlib.pyplot as plt
import os

# --- Constants ---
k_B = 1.380649e-23  # Boltzmann Constant (J/K)
I_0 = 1e-34         # Intrinsic Information Unit (J)

# Coupling constants for F_QC
beta = 0.1          # Quantum Coherence Coupling
alpha_DE = 0.5      # Dark Energy Coupling
alpha_DM = 0.3      # Dark Matter Coupling
gamma_exotic = 0.2  # Exotic Matter Coupling
eta = 0.1           # Teleportation Coupling
phi = (1 + np.sqrt(5)) / 2  # Golden Ratio (approx 1.618)

# --- Refined Quantum Coherence Function (F_QC) ---
def F_QC(D_ent, T_vac, rho_DE, rho_DM, rho_total, rho_exotic=0, Q_tele=0):
    """
    Calculates the Refined Quantum Coherence Function F_QC.
    Includes Golden Ratio (phi) in D_ent term and all 5 comprehensive terms.
    Handles NumPy arrays for all inputs.
    """
    t_vac_safe = np.maximum(T_vac, 1e-30) # Avoid division by zero or very small T_vac
    rho_total_safe = np.maximum(rho_total, 1e-30) # Avoid division by zero or very small rho_total

    term1 = 1 + beta * (phi * D_ent * I_0) / (k_B * t_vac_safe)
    term2 = 1 + alpha_DE * (rho_DE / rho_total_safe)
    term3 = 1 + alpha_DM * (rho_DM / rho_total_safe)
    term4 = 1 - gamma_exotic * rho_exotic # This crucial exotic matter term is included.
    term5 = 1 + eta * Q_tele

    return term1 * term2 * term3 * term4 * term5

# --- Conceptual Link for Plotting Curved Lines ---
# To make F_QC vary with Length Scale and produce curved lines,
# we introduce a conceptual dependence for D_ent on the scale.
# This makes D_ent "effective" for plotting purposes, even if D_ent_base is a constant.
D_ENT_SCALE_EXPONENT = 0.005 # Adjust this to change the steepness of the curve
# Use a reference scale roughly in the middle of your logspace scales for normalization
ref_scale = 1.0 # 1 meter as a reference point (arbitrary for conceptual scaling)

def get_effective_D_ent(D_ent_base, current_scale, ref_scale):
    """
    Returns an effective D_ent that varies conceptually with length scale.
    This helps produce curved lines in the plot.
    """
    # Ensure scale_ratio is always positive and not too small for numerical stability
    scale_ratio = np.maximum(current_scale / ref_scale, 1e-100)
    return D_ent_base * (scale_ratio**D_ENT_SCALE_EXPONENT)

# --- Simulation Parameters for F_QC Plot ---
# Length scales (m) from Planck to macroscopic
scales = np.logspace(-35, 10, 100) # From 1e-35 m (Planck) to 1e10 m (macroscopic)

# Reference densities for the background cosmic environment (held constant for this plot)
rho_DE_fixed = 0.7e-26                    # Dark energy density (kg/m^3)
rho_DM_fixed = 0.2e-26                    # Dark matter density (kg/m^3)
rho_M_fixed = 0.1e-26                     # Ordinary matter density (kg/m^3)
rho_total_fixed = rho_M_fixed + rho_DE_fixed + rho_DM_fixed # Total density (kg/m^3)

# Scenarios for different applications, now reflecting D_ent and other parameters
scenarios = [
    # Scenario 1: Time Travel/Wormhole (High D_ent, higher exotic matter)
    {'D_ent_base': 10.0, 'T_vac': 1e-10, 'rho_exotic': 0.1e-26, 'Q_tele': 0.5, 'label': 'Time Travel/Wormhole'},
    # Scenario 2: Clean Energy (Moderate D_ent, no exotic matter, no teleportation)
    {'D_ent_base': 5.0, 'T_vac': 1e-12, 'rho_exotic': 0.0, 'Q_tele': 0.0, 'label': 'Clean Energy'},
    # Scenario 3: Teleportation (Higher D_ent, some exotic matter, high teleportation efficiency)
    {'D_ent_base': 15.0, 'T_vac': 1e-10, 'rho_exotic': 0.05e-26, 'Q_tele': 1.0, 'label': 'Teleportation'}
]

# --- Plotting ---
plt.figure(figsize=(10, 6))
output_dir = os.path.join(os.path.dirname(__file__), '../figures')
os.makedirs(output_dir, exist_ok=True) # Ensure output directory exists

# Colors matching your JSON example
colors = ['#1f77b4', '#ff7f0e', '#2ca02c'] # Blue, Orange, Green

print("Calculating F_QC for application scenarios...")
for i, scenario in enumerate(scenarios):
    F_QC_values = []
    for scale in scales:
        # Calculate effective D_ent based on base D_ent and current scale
        effective_D_ent = get_effective_D_ent(scenario['D_ent_base'], scale, ref_scale)

        # Calculate F_QC using the effective D_ent and scenario-specific parameters
        fqc_val = F_QC(effective_D_ent, scenario['T_vac'],
                       rho_DE_fixed, rho_DM_fixed, rho_total_fixed,
                       scenario['rho_exotic'], scenario['Q_tele'])
        F_QC_values.append(fqc_val)

    plt.plot(scales, F_QC_values, label=scenario['label'], color=colors[i])

plt.xscale('log') # Logarithmic scale for the x-axis (Length Scale)
plt.xlabel('Length Scale (m)')
plt.ylabel(r'Quantum Coherence Function ($\mathcal{F}_{QC}$)')
plt.title(r'Refined $\mathcal{F}_{QC}$ with Golden Ratio Scaling for Applications')
plt.grid(True)
plt.legend(title='Application Scenario')
plt.tight_layout()

# Save the plot
plot_filename = os.path.join(output_dir, 'fibonacci_F_QC_applications.png')
plt.savefig(plot_filename)
plt.close()

print(f"Refined F_QC applications plot saved to: {plot_filename}")
print("fibonacci_F_QC_applications_sim.py complete.")

