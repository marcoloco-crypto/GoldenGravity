import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# Ensure output directory exists
output_dir = os.path.join(os.path.dirname(__file__), '../figures')
os.makedirs(output_dir, exist_ok=True)

# --- Constants ---
G_0 = 1.0           # Dimensionless Quantum Gravitational Coupling
G_Newton = 6.67430e-11  # Newton's Gravitational Constant (m^3 kg^-1 s^-2)
c = 2.99792458e8    # Speed of Light (m/s)
k_B = 1.380649e-23  # Boltzmann Constant (J/K)
h_bar = 1.054571817e-34 # Reduced Planck Constant (J s)
I_0 = 1e-34         # Intrinsic Information Unit (J)
L_P = 1.616e-35     # Planck Length (m) # Kept for completeness, not used in field eq prefactor

# Coupling constants for F_QC
beta = 0.1          # Quantum Coherence Coupling
alpha_DE = 0.5      # Dark Energy Coupling
alpha_DM = 0.3      # Dark Matter Coupling
gamma_exotic = 0.2  # Exotic Matter Coupling
eta = 0.1           # Teleportation Coupling
phi = (1 + np.sqrt(5)) / 2  # Golden Ratio (approx 1.618)

# Simulation specific scaling factor for visual demonstration
# This multiplies the source term to make effects visible in a short simulation.
SIMULATION_SCALING_FACTOR = 1e25 # Adjust this to tune the strength of the source term

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

# --- Helper Functions for D_ent and T_vac ---
def calculate_D_ent(S_value):
    """Calculates Entanglement Entropy Density from S_value."""
    return S_value * 1e18 # Conceptual scaling

def calculate_T_vac(S_value):
    """Calculates Vacuum Fluctuation Energy Scale from S_value."""
    return np.maximum(S_value * 1e-25, 1e-30) # Conceptual scaling (Joules)

# --- Simulation Parameters ---
L = 10.0            # Total spatial domain length (m)
num_time_steps = 5000  # Number of time steps
plot_interval = 250 # Plot every X time steps

# Fibonacci-inspired spatial grid
fib_sequence = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144] # More points for smoother variation
Nx = len(fib_sequence) # Number of spatial grid points
# Scale Fibonacci numbers to fit within L
x_fib_normalized = np.array(fib_sequence) / sum(fib_sequence)
x = np.cumsum(x_fib_normalized) * L # Non-uniform spatial grid
x = np.insert(x, 0, 0.0) # Ensure grid starts at 0

# Calculate variable dx values (spatial step sizes)
dx = np.diff(x)
# Smallest dx determines dt for stability (CFL condition)
dt = 0.1 * np.min(dx) / c # Time step size (s) - ensures CFL condition

# Initial conditions for S_field (using 3 arrays for explicit finite differencing)
initial_S_value = 1e-5 # Small initial value for S_field (dimensionless)
S_field_prev = np.full(Nx + 1, initial_S_value) # Nx+1 points for the grid including 0
S_field_curr = np.full(Nx + 1, initial_S_value)
S_field_next = np.full(Nx + 1, initial_S_value)

# Add a small localized perturbation in the middle to initiate wave propagation
perturbation_strength = 0.1
perturbation_width = 0.1 * L
# Find the index closest to L/2 for perturbation
perturbation_center_idx = np.argmin(np.abs(x - L/2))
perturbation_x_coords = x - x[perturbation_center_idx]
perturbation = perturbation_strength * np.exp(-(perturbation_x_coords**2) / (2 * (perturbation_width/5)**2))

S_field_prev += perturbation
S_field_curr += perturbation

# Source Term Densities (placeholder values for demonstration)
rho_M_source = np.zeros(Nx + 1)
rho_EM_source = np.zeros(Nx + 1)
rho_DM_source = np.zeros(Nx + 1)
rho_DE_source = np.zeros(Nx + 1)
rho_exotic_source = np.zeros(Nx + 1)

# Example localized source (e.g., a dense object or a region of interest)
# Place a source at a Fibonacci-related point, e.g., around x[Nx // 3]
source_center_idx = np.argmin(np.abs(x - x[int(Nx / phi)])) # Position influenced by phi
source_width_idx = 2 # Affects a few grid points around the center

if source_center_idx < 0: source_center_idx = 0
if source_center_idx >= Nx + 1: source_center_idx = Nx

rho_M_source[max(0, source_center_idx - source_width_idx) : min(Nx + 1, source_center_idx + source_width_idx + 1)] = 1000 # kg/m^3 (e.g., water density)
rho_exotic_source[max(0, source_center_idx + source_width_idx + 1) : min(Nx + 1, source_center_idx + 2 * source_width_idx + 1)] = -100 # kg/m^3 (negative density for exotic matter)

Q_tele_val = 0.5 # Dimensionless teleportation efficiency (constant for this sim)

# --- Simulation Loop (1+1D Finite Difference Method for Non-Uniform Grid) ---
print("Starting 1+1D Spacetime Field Evolution (Fibonacci Grid) Simulation...")

# Storage for plotting the heatmap over time
S_history = []

for t_step in range(num_time_steps):
    # Apply boundary conditions (e.g., fixed boundaries, S = initial_S_value)
    S_field_next[0] = initial_S_value
    S_field_next[Nx] = initial_S_value # Last point (Nx)

    # Calculate local densities and F_QC for the current time step
    # Note: For more advanced simulations, rho values could also evolve or be dynamic.
    rho_total_curr = rho_M_source + rho_EM_source/c**2 + rho_DM_source + rho_DE_source

    D_ent_curr = calculate_D_ent(S_field_curr)
    T_vac_curr = calculate_T_vac(S_field_curr)

    rho_DE_arr = np.full_like(S_field_curr, rho_DE_source.mean())
    rho_DM_arr = np.full_like(S_field_curr, rho_DM_source.mean())
    rho_exotic_arr = np.full_like(S_field_curr, rho_exotic_source)
    Q_tele_arr = np.full_like(S_field_curr, Q_tele_val)

    # F_QC calculation for the current step, now with phi and all terms
    F_QC_curr = F_QC(D_ent_curr, T_vac_curr,
                     rho_DE_arr, rho_DM_arr, rho_total_curr,
                     rho_exotic_arr, Q_tele_arr)

    # Calculate the source term (Right Hand Side of the Field Equation)
    source_term_prefactor = SIMULATION_SCALING_FACTOR * (G_0 * G_Newton / c**2)
    total_density_sum = rho_M_source + rho_EM_source/c**2 + rho_DM_source + rho_DE_source - gamma_exotic * rho_exotic_source
    source_term = source_term_prefactor * total_density_sum * F_QC_curr

    # Finite Difference Method for Wave Equation (Box S = Source) for Non-Uniform Grid
    # Equation: (1/c^2 * d^2S/dt^2) - d^2S/dx^2 = Source
    # d^2S/dt^2 = c^2 * (Source + d^2S/dx^2)
    # Using 2nd order central difference for spatial derivative on non-uniform grid:
    # d^2S/dx^2 approx 2 * ( (S_{i+1} - S_i) / (dx_i * (dx_i + dx_{i-1})) - (S_i - S_{i-1}) / (dx_{i-1} * (dx_i + dx_{i-1})) )
    # Let h1 = dx_{i-1} = x_i - x_{i-1}
    # Let h2 = dx_i = x_{i+1} - x_i
    # d^2S/dx^2 approx 2 * ( (S_field_curr[i+1] - S_field_curr[i]) / (dx[i] * (dx[i-1] + dx[i])) - (S_field_curr[i] - S_field_curr[i-1]) / (dx[i-1] * (dx[i-1] + dx[i])) )
    # This can also be written as: (2 / (dx[i-1] * dx[i] * (dx[i-1] + dx[i]))) * ( dx[i-1]*S_field_curr[i+1] - (dx[i-1]+dx[i])*S_field_curr[i] + dx[i]*S_field_curr[i-1] )

    for i in range(1, Nx): # Loop from 1 to Nx-1, as 0 and Nx are boundary points
        h_prev = dx[i-1] # x[i] - x[i-1]
        h_curr = dx[i]   # x[i+1] - x[i]

        term_plus_one = (S_field_curr[i+1] - S_field_curr[i]) / h_curr
        term_minus_one = (S_field_curr[i] - S_field_curr[i-1]) / h_prev

        laplacian_S = 2 * (term_plus_one - term_minus_one) / (h_prev + h_curr)

        second_deriv_S_t = c**2 * (source_term[i] + laplacian_S)
        S_field_next[i] = 2 * S_field_curr[i] - S_field_prev[i] + (dt**2) * second_deriv_S_t

    # Update fields for next time step
    S_field_prev = S_field_curr.copy()
    S_field_curr = S_field_next.copy()

    # --- Debugging and Storing History ---
    if t_step % plot_interval == 0:
        print(f"Time Step: {t_step}/{num_time_steps}")
        s_min, s_max = S_field_curr.min(), S_field_curr.max()
        s_mean = S_field_curr.mean()
        print(f"  S_field min: {s_min:.4e}, max: {s_max:.4e}, mean: {s_mean:.4e}")

        if np.isnan(S_field_curr).any() or np.isinf(S_field_curr).any():
            print(f"  !!!!! NaN or Inf detected in S_field at time step {t_step} !!!!!")
            sys.exit("Simulation stopped due to numerical instability.")

        S_history.append(S_field_curr.copy())

# Convert history to a NumPy array for heatmap
S_history_array = np.array(S_history)

# --- Plotting the Heatmap ---
fig, ax = plt.subplots(figsize=(12, 8))

# Time axis for heatmap
time_points = np.linspace(0, num_time_steps * dt, S_history_array.shape[0])

# Ensure x-axis for heatmap matches the non-uniform grid
heatmap_img = ax.imshow(S_history_array,
                        extent=[x.min(), x.max(), time_points.min(), time_points.max()],
                        aspect='auto', cmap='viridis', origin='lower') # 'lower' origin for time on y-axis

ax.set_xlabel('Fibonacci-Scaled Position (m)')
ax.set_ylabel('Time (s)')
ax.set_title(r'Spacetime Field ($\mathcal{S}$) Evolution on Fibonacci Grid')
fig.colorbar(heatmap_img, ax=ax, label=r'$\mathcal{S}$ Value')
plt.tight_layout()

# Save final plot
final_plot_path = os.path.join(output_dir, 'fibonacci_spacetime_evolution.png')
plt.savefig(final_plot_path)
plt.close(fig)

print(f"Fibonacci Spacetime evolution plot saved to: {final_plot_path}")
print("fibonacci_spacetime_evolution_sim.py complete.")

# Print final F_QC and source term values for analysis
# Using values from the last time step at a point influenced by source
last_F_QC_val = F_QC_curr[source_center_idx]
last_source_term_val = source_term[source_center_idx]
print(f"Calculated F_QC for simulation (at source center, last step): {last_F_QC_val:.4f}")
print(f"Calculated source term (at source center, last step): {last_source_term_val:.4e}")

