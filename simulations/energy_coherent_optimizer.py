import numpy as np
import matplotlib.pyplot as plt
import os

# --- Constants ---
phi = (1 + np.sqrt(5)) / 2  # Golden Ratio (approx 1.6180339887)
# NEW: Combined phi * pi factor as the target for optimization
PHI_PI_TARGET = phi * np.pi # Approximately 5.083203692

# --- Energy Coherence Score Function ---
def calculate_energy_coherence_score(adjustable_parameter_X):
    """
    Calculates a conceptual Energy Coherence Score.
    The score is maximized when 'adjustable_parameter_X' approaches PHI_PI_TARGET.
    A higher score indicates better PHI_PI-alignment in energy configurations/transfers.
    
    Score = 1 / (1 + |X - PHI_PI_TARGET|)
    This gives a max score of 1.0 when X = PHI_PI_TARGET, and decreases as X moves away from PHI_PI_TARGET.
    """
    # Ensure no division by zero if X is exactly PHI_PI_TARGET, though unlikely with floats
    difference = abs(adjustable_parameter_X - PHI_PI_TARGET)
    score = 1.0 / (1.0 + difference)
    return score

# --- Optimization Simulation Parameters ---
num_iterations = 500         # Number of steps in the optimization process
# Initial X should be in a range spanning the target PHI_PI_TARGET
initial_X = np.random.uniform(PHI_PI_TARGET * 0.5, PHI_PI_TARGET * 1.5) 
learning_rate = 0.05         # How big are the steps taken to adjust X
noise_level = 0.01           # Small random noise to simulate real-world fluctuations

# --- Optimization Loop ---
print(f"Starting Energy Coherence Optimization. Target Phi*Pi: {PHI_PI_TARGET:.4f}")
print(f"Initial Adjustable Parameter (X): {initial_X:.4f}")

current_X = initial_X
score_history = []
X_history = []

for iteration in range(num_iterations):
    current_score = calculate_energy_coherence_score(current_X)
    score_history.append(current_score)
    X_history.append(current_X)

    # Determine direction for optimization (simple gradient ascent-like)
    test_X_up = current_X + learning_rate
    test_X_down = current_X - learning_rate

    score_up = calculate_energy_coherence_score(test_X_up)
    score_down = calculate_energy_coherence_score(test_X_down)

    # Add small random noise to simulate imperfect measurements or environmental factors
    current_score_with_noise = current_score + np.random.normal(0, noise_level)
    score_up_with_noise = score_up + np.random.normal(0, noise_level)
    score_down_with_noise = score_down + np.random.normal(0, noise_level)


    # Move X in the direction that yields a better score (using noisy scores for decision)
    if score_up_with_noise > current_score_with_noise and score_up_with_noise >= score_down_with_noise:
        current_X += learning_rate
    elif score_down_with_noise > current_score_with_noise and score_down_with_noise > score_up_with_noise:
        current_X -= learning_rate
    else:
        # If no immediate improvement, try a smaller step or random jump to avoid local minima
        learning_rate *= 0.995 # Gradually reduce step size
        current_X += np.random.uniform(-learning_rate * 0.1, learning_rate * 0.1) # Add a smaller random perturbation

    # Clip X to a reasonable range to prevent it from going wild
    current_X = np.clip(current_X, PHI_PI_TARGET * 0.1, PHI_PI_TARGET * 2.0) # Adjust clip range to new target

    if iteration % (num_iterations // 10) == 0:
        print(f"Iteration {iteration}: X = {current_X:.4f}, Score = {current_score_with_noise:.4f} (Noisy)")

print(f"Optimization complete. Final X = {current_X:.4f}, Final Score = {calculate_energy_coherence_score(current_X):.4f} (True)")

# --- Plotting Results ---
plt.figure(figsize=(10, 8)) # Adjusted figure size for two subplots
output_dir = os.path.join(os.path.dirname(__file__), '../figures')
os.makedirs(output_dir, exist_ok=True) # Ensure output directory exists

# Plotting the Energy Coherence Score over iterations
plt.subplot(2, 1, 1) # Two plots, 1 column, first plot
plt.plot(score_history, color='purple')
plt.axhline(y=1.0, color='gray', linestyle='--', label='Max Score (1.0)')
plt.xlabel('Iteration')
plt.ylabel('Energy Coherence Score')
plt.title(r'Energy Coherence Score Optimization towards $(\phi \cdot \pi)$')
plt.legend()
plt.grid(True)

# Plotting the adjustable parameter X over iterations
plt.subplot(2, 1, 2) # Two plots, 1 column, second plot
plt.plot(X_history, color='orange')
plt.axhline(y=PHI_PI_TARGET, color='red', linestyle='--', label=r'Target $(\phi \cdot \pi)$')
plt.xlabel('Iteration')
plt.ylabel('Adjustable Parameter X')
plt.title(r'Adjustable Parameter X approaching $(\phi \cdot \pi)$')
plt.legend()
plt.grid(True)

plt.tight_layout() # Adjust layout to prevent overlap

# Save the plot
plot_filename = os.path.join(output_dir, 'energy_coherence_optimization.png')
plt.savefig(plot_filename)
plt.close()

print(f"Energy Coherence Optimization plot saved to: {plot_filename}")
print("energy_coherent_optimizer.py complete.")
