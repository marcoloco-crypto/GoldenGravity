import numpy as np
import matplotlib.pyplot as plt

print("Starting Gravitational Modulator Simulation...")
L, T = 100, 5000
dx, dt = 1.0, 0.01
phi = (1 + np.sqrt(5)) / 2
S_field = np.ones((T, L)) * 1e-5
x0, t0 = L // 2, 0
S_field[t0, x0] = 1e10
for t in range(1, T):
    for x in range(1, L-1):
        S_field[t, x] = S_field[t-1, x] + dt * (
            phi * (S_field[t-1, x+1] - 2*S_field[t-1, x] + S_field[t-1, x-1]) / dx**2
        )
    if t % 250 == 0:
        print(f"Time Step: {t}/{T}")
        print(f"  S_field min: {S_field[t].min():.4e}, max: {S_field[t].max():.4e}, mean: {S_field[t].mean():.4e}")
plt.figure(figsize=(10, 6))
plt.imshow(S_field, aspect='auto', cmap='viridis', origin='lower')
plt.colorbar(label='Spacetime Field (S)')
plt.title('Gravitational Modulator Evolution')
plt.xlabel('Spatial Grid (x)')
plt.ylabel('Time Step (t)')
plt.savefig('../plots/gravitational_modulator.png')
plt.close()
print("Gravitational modulator plot saved to: ../plots/gravitational_modulator.png")
print("gravitational_modulator_sim.py complete.")
