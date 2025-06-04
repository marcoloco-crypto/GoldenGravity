import numpy as np
import matplotlib.pyplot as plt

print("Starting 1+1D Spacetime Field Evolution (Fibonacci Grid) Simulation...")
# Constants (SI units)
G_0 = 6.67430e-11  # Gravitational constant (m^3 kg^-1 s^-2)
c = 2.99792458e8   # Speed of light (m s^-1)
k_B = 1.380649e-23 # Boltzmann constant (J K^-1)
phi = (1 + np.sqrt(5)) / 2  # Golden ratio
L = 1e-10          # Spatial domain (meters, Planck scale)
T = 5000           # Time steps
N = 100            # Spatial points
T_vac = 2.7        # Vacuum temperature (K)
I_0 = 1e4          # Reference intensity (J m^-2) for F_QC scaling
rho_exotic = 1e5   # Exotic matter density (kg m^-3) for CTCs

# Fibonacci-scaled grid for fractal-like spacetime
fib = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
fib = np.array(fib[:min(len(fib), N)]) / sum(fib[:min(len(fib), N)]) * L
x = np.cumsum(fib)
dx = np.diff(x).mean()
dt = 0.5 * dx / c  # Stable time step (Courant condition)

# Initialize S_field (dimensionless gravitational potential)
S_field = np.zeros((T, len(x)))
S_field_old = np.zeros(len(x))
x0, t0 = len(x) // 2, 0
S_field[t0, x0] = 1e-5  # Initial ripple for wave propagation
S_field_old[x0] = 1e-5

# Evolution with wave equation for CTC formation
for t in range(1, T):
    S_field_new = np.zeros(len(x))
    for i in range(1, len(x)-1):
        d2S_dx2 = (S_field[t-1, i+1] - 2*S_field[t-1, i] + S_field[t-1, i-1]) / dx**2
        source = phi * G_0 * rho_exotic / c**4  # Exotic matter drives CTC curvature
        S_field_new[i] = 2 * S_field[t-1, i] - S_field_old[i] + dt**2 * (c**2 * d2S_dx2 + source)
    # Periodic boundaries for time loop stability
    S_field_new[0] = S_field_new[-2]
    S_field_new[-1] = S_field_new[1]
    S_field_old = S_field[t-1].copy()
    S_field[t] = S_field_new
    if t % 250 == 0:
        print(f"Time Step: {t}/{T}")
        print(f"  S_field min: {S_field[t].min():.4e}, max: {S_field[t].max():.4e}, mean: {S_field[t].mean():.4e}")

# Plot spacetime ripples
plt.figure(figsize=(10, 6))
plt.imshow(S_field, aspect='auto', cmap='viridis', origin='lower')
plt.colorbar(label='Spacetime Field (dimensionless)')
plt.title('Fibonacci Spacetime Evolution for CTCs')
plt.xlabel('Spatial Grid (meters)')
plt.ylabel('Time Step (seconds)')
plt.savefig('../plots/fibonacci_spacetime_evolution.png')
plt.close()
print("Fibonacci Spacetime evolution plot saved to: ../plots/fibonacci_spacetime_evolution.png")
print("fibonacci_spacetime_evolution_sim.py complete.")

# Calculate F_QC (dimensionless, quantum coherence for time travel)
F_QC = phi * S_field[-1, x0] / (k_B * T_vac / I_0)
print(f"Calculated F_QC for simulation (at source center, last step): {F_QC:.4e}")
source_term = S_field[-1, x0] / phi
print(f"Calculated source term (at source center, last step): {source_term:.4e}")
