import numpy as np
import matplotlib.pyplot as plt
import os

# --- Constants ---
# Fundamental constants
c = 299792458       # Speed of light (m/s)
G_Newton = 6.674e-11 # Newton's gravitational constant (m^3 kg^-1 s^-2)
k_B = 1.380649e-23  # Boltzmann Constant (J/K)

# ESQET specific constants (using explicit Planck values for the core framework)
G_0 = 1.0           # Dimensionless gravitational coupling constant (ESQET)
alpha_dark = 0.4    # Combined Dark Matter/Energy Coupling for F_QC
phi = (1 + np.sqrt(5)) / 2  # Golden Ratio (approx 1.6180339887)
# NEW: Combined phi * pi factor
PHI_PI = phi * np.pi # Approximately 5.083203692

I_0_PLANCK = 1.956e9         # Intrinsic Information Unit (J) - Set to Planck Energy (E_Pl)
T_VAC_PLANCK = 1.416808e32   # Vacuum Fluctuation Energy Scale (K) - Set to Planck Temperature (T_Pl)


# --- Quantum Coherence Function (F_QC) v2.0 - Internal Definition ---
def F_QC(D_ent, T_vac_current, rho_Dark, rho_total):
    """
    Calculates the Refined Quantum Coherence Function F_QC (v2.0).
    Now explicitly uses the combined Golden Ratio * Pi (PHI_PI).
    The I_0_PLANCK and k_B are global constants.
    T_vac_current is the *effective* vacuum temperature for a given scenario.
    """
    t_vac_safe = np.maximum(T_vac_current, 1e-30)
    rho_total_safe = np.maximum(rho_total, 1e-30)

    # Term 1: Entanglement and Vacuum Energy, now with PHI_PI directly
    # Note: The ratio (I_0_PLANCK / (k_B * T_VAC_PLANCK)) is approx 1
    term1 = 1 + PHI_PI * (D_ent * I_0_PLANCK) / (k_B * t_vac_safe)
    term2 = 1 + alpha_dark * (rho_Dark / rho_total_safe)

    return term1 * term2

# --- Simulation Parameters ---
Lx = 100            # Spatial dimension (meters)
Nx = 200            # Number of spatial points (Fibonacci-scaled)
Lt = 50             # Temporal dimension (arbitrary units for steps)
Nt = 100            # Number of temporal steps

# Create Fibonacci-scaled spatial grid
fib_sequence = [1, 1]
while len(fib_sequence) < Nx:
    fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])

# Normalize Fibonacci sequence to create non-uniform spacing that sums to Lx
fib_normalized = np.array(fib_sequence[:Nx]) / np.sum(fib_sequence[:Nx])
x_fib = np.cumsum(fib_normalized) * Lx # Adjust to start roughly from 0

# Time step
dt = Lt / Nt

# Initial conditions for S field (start with a small perturbation)
S_field = np.zeros((Nt, Nx))
S_field[0, Nx // 2] = 1.0  # Initial perturbation at the center

# --- Scenario Specific Parameters (for Field Equation inputs) ---
# These parameters now define the *sources* for the S field evolution.
# F_QC inputs will be derived from these.
# Values are illustrative and conceptual.
RHO_M_BACKGROUND = 1e-27            # kg/m^3, avg matter density
E_EM_BACKGROUND = 1e-15             # J/m^3, avg EM energy density
RHO_DARK_BACKGROUND = 0.9e-26       # kg/m^3, avg combined dark matter/energy density
RHO_TOTAL_BACKGROUND = RHO_M_BACKGROUND + RHO_DARK_BACKGROUND + (E_EM_BACKGROUND / c**2) # kg/m^3

# For the core simulation, assume T_vac is at Planck scale for fundamental behavior
D_ENT_BACKGROUND = 1e-10            # Conceptual entanglement density

# Define a localized source term (e.g., a "star" or "quantum anomaly")
source_location_idx = Nx // 4
source_strength_mass = 1e-20       # Localized mass density (kg/m^3)
source_strength_em = 1e-5          # Localized EM energy density (J/m^3)
source_strength_dark = 1e-25       # Localized combined dark density (kg/m^3)
source_D_ent = 1e-5                # Localized higher entanglement density

# We use T_VAC_PLANCK here, or can conceptually lower it for engineered 'cold vacuum' scenarios if needed.
# For core simulation, stick to Planck T_vac unless specifically manipulating it.
SOURCE_T_VAC_MANIPULATED = T_VAC_PLANCK * 1e-20 # Example of a *manipulated* T_vac for a source region

# Source profile (Gaussian-like for smooth fall-off)
source_width_grid_points = 10 # in grid points
source_profile = np.exp(-((np.arange(Nx) - source_location_idx)**2) / (2 * source_width_grid_points**2))

# --- Field Equation Evolution (1+1D using Finite Differences) ---
print("Simulating S field evolution (v2.0, Planck-anchored, phi*pi)...")

# Initialize S_field for explicit finite difference
S_field_prev = np.zeros(Nx)
S_field_curr = S_field[0, :]
S_field_next = np.zeros(Nx)

# Store S_field history for plotting
S_history = np.zeros((Nt, Nx))
S_history[0, :] = S_field_curr

for t in range(1, Nt):
    for i in range(1, Nx - 1):
        # Calculate local densities and F_QC for each point in space and time
        current_rho_M = RHO_M_BACKGROUND + source_strength_mass * source_profile[i]
        current_E_EM = E_EM_BACKGROUND + source_strength_em * source_profile[i]
        current_rho_Dark = RHO_DARK_BACKGROUND + source_strength_dark * source_profile[i]
        
        current_rho_total = current_rho_M + (current_E_EM / c**2) + current_rho_Dark

        current_D_ent = D_ENT_BACKGROUND + source_D_ent * source_profile[i]
        
        # Here, T_vac is passed as a variable, which could be T_VAC_PLANCK for the core
        # or SOURCE_T_VAC_MANIPULATED in the source region if modeling specific engineering.
        current_T_vac_for_FQC = T_VAC_PLANCK # Default to Planck T_vac
        if source_profile[i] > 0.1: # If within the source region, use manipulated T_vac
            current_T_vac_for_FQC = SOURCE_T_VAC_MANIPULATED


        current_F_QC = F_QC(current_D_ent, current_T_vac_for_FQC, current_rho_Dark, current_rho_total)

        # Calculate the source term for the field equation
        source_term_val = (G_0 * G_Newton / c**2) * \
                          (current_rho_M + (current_E_EM / c**2) + current_rho_Dark) * \
                          current_F_QC

        # Finite difference approximation for D'Alembertian operator
        dx_left = x_fib[i] - x_fib[i-1]
        dx_right = x_fib[i+1] - x_fib[i]
        
        term_plus_one = S_field_curr[i+1] / (dx_right * (dx_left + dx_right))
        term_curr = S_field_curr[i] / (dx_left * dx_right)
        term_minus_one = S_field_curr[i-1] / (dx_left * (dx_left + dx_right))
        
        laplacian_S = 2 * (term_plus_one - term_curr + term_minus_one)

        S_field_next[i] = 2 * S_field_curr[i] - S_field_prev[i] + \
                          (dt**2) * (c**2) * (source_term_val + laplacian_S)

    # Boundary conditions: fixed at initial_S_value (assuming first and last points are fixed)
    S_field_next[0] = S_field_curr[0]
    S_field_next[Nx-1] = S_field_curr[Nx-1]

    # Update for next iteration
    S_field_prev = S_field_curr.copy()
    S_field_curr = S_field_next.copy()
    S_history[t, :] = S_field_curr

# --- Plotting ---
plt.figure(figsize=(12, 6))
output_dir = os.path.join(os.path.dirname(__file__), '../figures')
os.makedirs(output_dir, exist_ok=True)

plt.imshow(S_history, aspect='auto', origin='lower', extent=[x_fib[0], x_fib[-1], 0, Lt], cmap='viridis')
plt.colorbar(label=r'Spacetime Information Field ($\mathcal{S}$)')
plt.xlabel('Spatial Dimension (m) - Fibonacci Scaled')
plt.ylabel('Time Evolution (arbitrary units)')
plt.title(r'Spacetime Information Field ($\mathcal{S}$) Evolution (v2.0) ($\phi \cdot \pi$)')
plt.grid(False)

# Save the plot
plot_filename = os.path.join(output_dir, 'fibonacci_spacetime_evolution_v2.png')
plt.savefig(plot_filename)
plt.close()

print(f"S field evolution plot (v2.0) saved to: {plot_filename}")
print("fibonacci_spacetime_evolution_sim.py (v2.0) complete.")

