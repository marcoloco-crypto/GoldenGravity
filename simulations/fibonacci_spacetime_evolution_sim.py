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
PHI_PI = phi * np.pi # Approximately 5.083203692

I_0_PLANCK = 1.956e9         # Intrinsic Information Unit (J) - Set to Planck Energy (E_Pl)
T_VAC_PLANCK = 1.416808e32   # Vacuum Fluctuation Energy Scale (K) - Set to Planck Temperature (T_Pl)


# --- Quantum Coherence Function (F_QC) v2.0 - Internal Definition ---
def F_QC(D_ent, T_vac_current, rho_Dark, rho_total):
    t_vac_safe = np.maximum(T_vac_current, 1e-30)
    rho_total_safe = np.maximum(rho_total, 1e-30)
    term1 = 1 + PHI_PI * (D_ent * I_0_PLANCK) / (k_B * t_vac_safe)
    term2 = 1 + alpha_dark * (rho_Dark / rho_total_safe)
    return term1 * term2

# --- Simulation Parameters ---
Lx = 100            # Spatial dimension (meters)
Nx = 200            # Number of spatial points (Fibonacci-scaled)
Lt = 50             # Temporal dimension (arbitrary units for steps)
Nt = 20000          # DRASTICALLY INCREASED for stability (e.g., 20000 or more)

# Create Fibonacci-scaled spatial grid
fib_sequence = [1, 1]
while len(fib_sequence) < Nx:
    fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])

fib_normalized = np.array(fib_sequence[:Nx]) / np.sum(fib_sequence[:Nx])
x_fib = np.cumsum(fib_normalized) * Lx 

# Time step
dt = Lt / Nt

# Initial conditions for S field (start with a small perturbation)
S_field = np.zeros((Nt, Nx))
# Drastically reduced initial perturbation further
S_field[0, Nx // 2] = 1e-8 # Even smaller initial value

# --- Scenario Specific Parameters (for Field Equation inputs) ---
RHO_M_BACKGROUND = 1e-27            # kg/m^3, avg matter density
E_EM_BACKGROUND = 1e-20             # J/m^3, avg EM energy density (further reduced)
RHO_DARK_BACKGROUND = 0.9e-26       # kg/m^3, avg combined dark matter/energy density
RHO_TOTAL_BACKGROUND = RHO_M_BACKGROUND + RHO_DARK_BACKGROUND + (E_EM_BACKGROUND / c**2) # kg/m^3

D_ENT_BACKGROUND = 1e-18            # Conceptual entanglement density (further reduced)

# Define a localized source term (e.g., a "star" or "quantum anomaly")
source_location_idx = Nx // 4
# Drastically reduced source strengths further
source_strength_mass = 1e-35       # Localized mass density (kg/m^3)
source_strength_em = 1e-20          # Localized EM energy density (J/m^3)
source_strength_dark = 1e-40       # Localized combined dark density (kg/m^3)
source_D_ent = 1e-18                # Localized higher entanglement density

SOURCE_T_VAC_MANIPULATED = T_VAC_PLANCK * 1e-20

source_profile = np.exp(-((np.arange(Nx) - source_location_idx)**2) / (2 * 10**2)) # Width of 10 grid points

# --- Field Equation Evolution (1+1D using Finite Differences) ---
print("Simulating S field evolution (v2.0, Planck-anchored, phi*pi)...")

S_field_prev = S_field[0, :].copy()
S_field_curr = S_field[0, :].copy()
S_field_next = np.zeros(Nx)

S_history = np.zeros((Nt, Nx))
S_history[0, :] = S_field_curr

MIN_DX = 1e-20 # Slightly increased clamp to prevent division by near-zero effectively.
MAX_S_FIELD_VALUE = 1e-2 # Clamp S_field to prevent overflow (arbitrary upper bound)
MIN_S_FIELD_VALUE = -1e-2 # Clamp S_field to prevent underflow

for t in range(1, Nt):
    S_field_next[0] = S_field_curr[0]
    S_field_next[Nx-1] = S_field_curr[Nx-1]

    for i in range(1, Nx - 1):
        current_rho_M = RHO_M_BACKGROUND + source_strength_mass * source_profile[i]
        current_E_EM = E_EM_BACKGROUND + source_strength_em * source_profile[i]
        current_rho_Dark = RHO_DARK_BACKGROUND + source_strength_dark * source_profile[i]
        
        current_rho_total = current_rho_M + (current_E_EM / c**2) + current_rho_Dark

        current_D_ent = D_ENT_BACKGROUND + source_D_ent * source_profile[i]
        
        current_T_vac_for_FQC = T_VAC_PLANCK
        if source_profile[i] > 0.1:
            current_T_vac_for_FQC = SOURCE_T_VAC_MANIPULATED

        current_F_QC = F_QC(current_D_ent, current_T_vac_for_FQC, current_rho_Dark, current_rho_total)

        source_term_val = (G_0 * G_Newton / c**2) * \
                          (current_rho_M + (current_E_EM / c**2) + current_rho_Dark) * \
                          current_F_QC

        dx_left = x_fib[i] - x_fib[i-1]
        dx_right = x_fib[i+1] - x_fib[i]
        
        # Clamp dx_left and dx_right to a minimum value to prevent division by zero/near-zero
        dx_left_clamped = np.maximum(dx_left, MIN_DX)
        dx_right_clamped = np.maximum(dx_right, MIN_DX)
        
        # Second spatial derivative (d^2S/dx^2) for non-uniform grid
        laplacian_S_term1 = S_field_curr[i+1] / (dx_right_clamped * (dx_left_clamped + dx_right_clamped))
        laplacian_S_term2 = S_field_curr[i] / (dx_left_clamped * dx_right_clamped)
        laplacian_S_term3 = S_field_curr[i-1] / (dx_left_clamped * (dx_left_clamped + dx_right_clamped))
        
        laplacian_S = 2 * (laplacian_S_term1 - laplacian_S_term2 + laplacian_S_term3)

        # Rearrange the field equation for S_field_next (explicit method)
        S_field_next[i] = 2 * S_field_curr[i] - S_field_prev[i] + \
                          (dt**2) * (c**2) * (source_term_val + laplacian_S)
        
        # Clamp S_field values to prevent them from growing too large or too small
        S_field_next[i] = np.clip(S_field_next[i], MIN_S_FIELD_VALUE, MAX_S_FIELD_VALUE)


    S_field_prev = S_field_curr.copy()
    S_field_curr = S_field_next.copy()
    S_history[t, :] = S_field_curr

    if t % (Nt // 10) == 0:
        print(f"Time Step: {t}/{Nt}, S_field min: {S_field_curr.min():.4e}, max: {S_field_curr.max():.4e}, mean: {S_field_curr.mean():.4e}")


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
