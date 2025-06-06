import numpy as np
import matplotlib.pyplot as plt
import os

# --- Constants ---
# Fundamental constants (using explicit Planck values where defined for the core framework)
k_B = 1.380649e-23  # Boltzmann Constant (J/K)

# Definitive Planck-scale constants for the core F_QC framework (Option 1)
I_0_PLANCK = 1.956e9         # Intrinsic Information Unit (J) - Set to Planck Energy (E_Pl)
T_VAC_PLANCK = 1.416808e32   # Vacuum Fluctuation Energy Scale (K) - Set to Planck Temperature (T_Pl)

# Coupling constants for F_QC
alpha_dark = 0.4    # Combined Dark Matter/Energy Coupling for F_QC
phi = (1 + np.sqrt(5)) / 2  # Golden Ratio (approx 1.6180339887)
# NEW: Combined phi * pi factor
PHI_PI = phi * np.pi # Approximately 5.083203692

# --- Refined Quantum Coherence Function (F_QC) v2.0 ---
def F_QC(D_ent, T_vac_current, rho_Dark, rho_total):
    """
    Calculates the Refined Quantum Coherence Function F_QC (v2.0).
    Explicitly uses the combined Golden Ratio * Pi (PHI_PI).
    The I_0_PLANCK and k_B are global constants.
    T_vac_current is the *effective* vacuum temperature for a given scenario.
    """
    t_vac_safe = np.maximum(T_vac_current, 1e-30) # Avoid division by zero or very small T_vac
    rho_total_safe = np.maximum(rho_total, 1e-30) # Avoid division by zero or very small rho_total

    # Term 1: Entanglement and Vacuum Energy, now with PHI_PI directly
    # Note: The ratio (I_0_PLANCK / (k_B * T_VAC_PLANCK)) is approx 1,
    # but the structure explicitly shows the constants for clarity.
    term1 = 1 + PHI_PI * (D_ent * I_0_PLANCK) / (k_B * t_vac_safe)
    
    # Term 2: Combined Dark Matter/Energy contribution
    term2 = 1 + alpha_dark * (rho_Dark / rho_total_safe)

    return term1 * term2

# --- Conceptual Link for Plotting Curved Lines ---
# To make F_QC vary with Length Scale and produce curved lines,
# we introduce a conceptual dependence for D_ent on the scale.
D_ENT_SCALE_EXPONENT = 0.005 # Adjust this to change the steepness of the curve
ref_scale = 1.0 # 1 meter as a reference point (arbitrary for conceptual scaling)

def get_effective_D_ent(D_ent_base, current_scale, ref_scale):
    """
    Returns an effective D_ent that varies conceptually with length scale.
    This helps produce curved lines in the plot.
    """
    scale_ratio = np.maximum(current_scale / ref_scale, 1e-100)
    return D_ent_base * (scale_ratio**D_ENT_SCALE_EXPONENT)

# --- Simulation Parameters for F_QC Plot ---
# Length scales (m) from Planck to macroscopic
scales = np.logspace(-35, 10, 100) # From 1e-35 m (Planck) to 1e10 m (macroscopic)

# Reference densities for the background cosmic environment (held constant for this plot)
rho_Dark_fixed = 0.9e-26                  # Combined Dark energy and Dark matter density (kg/m^3)
rho_M_fixed = 0.1e-26                     # Ordinary matter density (kg/m^3)
rho_total_fixed = rho_M_fixed + rho_Dark_fixed # Total density (kg/m^3)

# Scenarios for different applications
# T_vac values here represent the *effective* vacuum conditions for the application,
# which can deviate from T_VAC_PLANCK (Option 2 consideration).
scenarios = [
    # Scenario 1: Time Travel/Wormhole (High D_ent, T_vac near Planck for theoretical consistency)
    {'D_ent_base': 10.0, 'T_vac_scenario': T_VAC_PLANCK, 'label': r'Time Travel/Wormhole (T_{vac} \approx T_{Pl})'},
    # Scenario 2: Clean Energy (Moderate D_ent, very low T_vac for conceptual energy extraction)
    {'D_ent_base': 5.0, 'T_vac_scenario': 1e-15, 'label': r'Clean Energy (T_{vac} manipulated)'}, # Conceptual low T_vac
    # Scenario 3: Teleportation (Very High D_ent, T_vac closer to Planck for fundamental coherence)
    {'D_ent_base': 15.0, 'T_vac_scenario': T_VAC_PLANCK * 0.1, 'label': r'Teleportation (T_{vac} slightly lower)'} # A slight deviation for effect
]

# --- Plotting ---
plt.figure(figsize=(10, 6))
output_dir = os.path.join(os.path.dirname(__file__), '../figures')
os.makedirs(output_dir, exist_ok=True) # Ensure output directory exists

colors = ['#1f77b4', '#ff7f0e', '#2ca02c'] # Blue, Orange, Green

print("Calculating F_QC for application scenarios (v2.0, Planck-anchored)...")
for i, scenario in enumerate(scenarios):
    F_QC_values = []
    for scale in scales:
        effective_D_ent = get_effective_D_ent(scenario['D_ent_base'], scale, ref_scale)

        # Calculate F_QC using its defined inputs, passing scenario-specific T_vac
        fqc_val = F_QC(effective_D_ent, scenario['T_vac_scenario'],
                       rho_Dark_fixed, rho_total_fixed)
        F_QC_values.append(fqc_val)

    plt.plot(scales, F_QC_values, label=scenario['label'], color=colors[i])

plt.xscale('log') # Logarithmic scale for the x-axis (Length Scale)
plt.xlabel('Length Scale (m)')
plt.ylabel(r'Quantum Coherence Function ($\mathcal{F}_{QC}$)')
plt.title(r'Refined $\mathcal{F}_{QC}$ (v2.0) with Golden Ratio ($\phi \cdot \pi$) Scaling')
plt.grid(True)
plt.legend(title='Application Scenario')
plt.tight_layout()

# Save the plot
plot_filename = os.path.join(output_dir, 'fibonacci_F_QC_applications_v2.png')
plt.savefig(plot_filename)
plt.close()

print(f"Refined F_QC applications plot (v2.0) saved to: {plot_filename}")
print("fibonacci_F_QC_applications_sim.py (v2.0) complete.")


