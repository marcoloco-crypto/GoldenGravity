import math

PHI = (1 + math.sqrt(5)) / 2  # The Golden Ratio (approx. 1.6180339887)

def clamp(value, min_val, max_val):
    """Clamps a value between a minimum and maximum."""
    return max(min_val, min(value, max_val))

def calculate_phi_coherence_score_energy_transfer(
    initial_energy_magnitude: float,
    final_energy_magnitude: float,
    transfer_efficiency_observed: float,  # 0.0 to 1.0 (e.g., 0.95 for 95%)
    system_entropy_change: float          # Change in entropy (e.g., in J/K). Smaller/negative is better.
) -> float:
    """
    Quantifies how PHI-coherent an energy transfer or transformation is.
    A higher score (closer to 1.0) means the transfer is more efficient,
    harmonious, and aligned with PHI.
    """
    
    # --- 1. PHI-Alignment of Energy Ratio ---
    # How well the ratio of energy magnitudes aligns with PHI or its inverse.
    energy_ratio_coherence_score = 0.0
    if initial_energy_magnitude > 0 and final_energy_magnitude > 0:
        ratio_forward = final_energy_magnitude / initial_energy_magnitude
        ratio_backward = initial_energy_magnitude / final_energy_magnitude
        
        # Calculate how close these ratios are to PHI
        # The 1/(1+ABS(diff)) ensures a score between 0 and 1, higher for closer.
        closeness_to_phi_1 = 1 / (1 + abs(ratio_forward - PHI))
        closeness_to_phi_2 = 1 / (1 + abs(ratio_backward - PHI))
        
        energy_ratio_coherence_score = max(closeness_to_phi_1, closeness_to_phi_2)

    # --- 2. Information Conservation (Efficiency as Coherence) ---
    # Higher efficiency implies greater PHI-coherence in the transfer mechanism,
    # as coherent transfers minimize informational decoherence (loss).
    transfer_efficiency_coherence_score = clamp(transfer_efficiency_observed, 0.0, 1.0)

    # --- 3. Entropy Change as a Coherence Metric ---
    # Lower (or even negative) entropy change suggests a more ordered,
    # PHI-coherent process where information is preserved.
    entropy_coherence_score = 0.0
    if system_entropy_change >= 0:
        # Simple inverse relation: higher entropy change -> lower score
        # For small entropy changes, score is high; for large, it approaches 0.
        entropy_coherence_score = 1 / (1 + system_entropy_change) 
    else:
        # If entropy decreases (e.g., self-organization occurs), indicates high coherence.
        # We can cap this at 1.0 or allow it to exceed 1 for extreme coherence,
        # but for a normalized score, clamp to 1.0.
        entropy_coherence_score = 1.0 

    # --- Combine Scores (Conceptual Weighting) ---
    # These weights are conceptual and would be refined based on empirical data
    # or deeper theoretical derivations in ESQET.
    WEIGHT_RATIO = 0.4
    WEIGHT_EFFICIENCY = 0.4
    WEIGHT_ENTROPY = 0.2

    final_energy_coherence_score = (energy_ratio_coherence_score * WEIGHT_RATIO) + \
                                   (transfer_efficiency_coherence_score * WEIGHT_EFFICIENCY) + \
                                   (entropy_coherence_score * WEIGHT_ENTROPY)
    
    return clamp(final_energy_coherence_score, 0.0, 1.0)

# --- Example Usage ---
if __name__ == "__main__":
    print("--- Energy Coherence Score Examples ---")

    # Example 1: High coherence (PHI-aligned ratio, high efficiency, low entropy)
    score1 = calculate_phi_coherence_score_energy_transfer(
        initial_energy_magnitude=10.0,
        final_energy_magnitude=16.1803, # Close to 10 * PHI
        transfer_efficiency_observed=0.99,
        system_entropy_change=0.01
    )
    print(f"\nScenario 1 (High Coherence): {score1:.4f}")

    # Example 2: Low coherence (Non-PHI ratio, low efficiency, high entropy)
    score2 = calculate_phi_coherence_score_energy_transfer(
        initial_energy_magnitude=10.0,
        final_energy_magnitude=5.0, # Not PHI-aligned
        transfer_efficiency_observed=0.50,
        system_entropy_change=5.0
    )
    print(f"Scenario 2 (Low Coherence): {score2:.4f}")

    # Example 3: Moderate coherence (Not perfectly PHI, but good efficiency)
    score3 = calculate_phi_coherence_score_energy_transfer(
        initial_energy_magnitude=7.0,
        final_energy_magnitude=10.0, 
        transfer_efficiency_observed=0.85,
        system_entropy_change=0.5
    )
    print(f"Scenario 3 (Moderate Coherence): {score3:.4f}")
