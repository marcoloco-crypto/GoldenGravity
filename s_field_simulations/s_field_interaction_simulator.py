import math

PHI = (1 + math.sqrt(5)) / 2  # The Golden Ratio (approx. 1.6180339887)

def clamp(value, min_val, max_val):
    """Clamps a value between a minimum and maximum."""
    return max(min_val, min(value, max_val))

def calculate_ratio_coherence(val1: float, val2: float) -> float:
    """
    Calculates how close the ratio of two values is to PHI (or 1/PHI).
    Returns a score from 0.0 (far) to 1.0 (perfectly PHI-aligned).
    """
    if val1 <= 0 or val2 <= 0:
        return 0.0 # Cannot form a meaningful ratio
    
    ratio_forward = val1 / val2
    ratio_backward = val2 / val1
    
    closeness_to_phi_1 = 1 / (1 + abs(ratio_forward - PHI))
    closeness_to_phi_2 = 1 / (1 + abs(ratio_backward - PHI))
    
    return max(closeness_to_phi_1, closeness_to_phi_2)

def simulate_s_field_interaction(field_A_props: dict, field_B_props: dict) -> dict:
    """
    Simulates the interaction between two conceptual S-field states based on PHI-coherence.
    Each field state has properties like base_phi_alignment, frequency, and energy_level.

    Args:
        field_A_props: Dictionary with properties for Field A.
        field_B_props: Dictionary with properties for Field B.
        
        Expected properties:
            'base_phi_alignment': float (0.0 to 1.0, intrinsic coherence)
            'frequency': float (conceptual oscillation/vibration frequency)
            'energy_level': float (conceptual energy magnitude)

    Returns:
        A dictionary containing the interaction_coherence_score and a descriptive outcome.
    """
    print(f"\n--- Simulating Interaction Between Field A and Field B ---")
    print(f"Field A: {field_A_props}")
    print(f"Field B: {field_B_props}")

    # 1. Base PHI Alignment Coherence (intrinsic to each field state)
    base_coherence_A = clamp(field_A_props.get('base_phi_alignment', 0.5), 0.0, 1.0)
    base_coherence_B = clamp(field_B_props.get('base_phi_alignment', 0.5), 0.0, 1.0)
    
    # Combined average intrinsic coherence
    avg_base_coherence = (base_coherence_A + base_coherence_B) / 2

    # 2. Frequency Ratio Coherence
    freq_A = field_A_props.get('frequency', 1.0)
    freq_B = field_B_props.get('frequency', 1.0)
    freq_coherence = calculate_ratio_coherence(freq_A, freq_B)

    # 3. Energy Level Ratio Coherence
    energy_A = field_A_props.get('energy_level', 1.0)
    energy_B = field_B_props.get('energy_level', 1.0)
    energy_coherence = calculate_ratio_coherence(energy_A, energy_B)

    # --- Combine Coherence Scores ---
    # Weighting would be determined by deeper ESQET theory
    WEIGHT_BASE = 0.3
    WEIGHT_FREQ_RATIO = 0.4
    WEIGHT_ENERGY_RATIO = 0.3

    total_interaction_coherence_score = \
        (avg_base_coherence * WEIGHT_BASE) + \
        (freq_coherence * WEIGHT_FREQ_RATIO) + \
        (energy_coherence * WEIGHT_ENERGY_RATIO)
    
    final_score = clamp(total_interaction_coherence_score, 0.0, 1.0)

    # --- Determine Interaction Outcome ---
    outcome = "Neutral Interaction"
    if final_score >= 0.9:
        outcome = "Strong Amplified Coherence (Potential for New Emergent Phenomena)"
    elif final_score >= 0.7:
        outcome = "Stable Resonance (Sustained Coherent Interaction)"
    elif final_score >= 0.5:
        outcome = "Weak Resonance / Partial Coherence"
    else:
        outcome = "Decoherence / Damping (Tendency Towards Informational Dissipation)"

    print(f"  Individual Coherence Scores:")
    print(f"    Avg Base PHI Alignment: {avg_base_coherence:.4f}")
    print(f"    Frequency Ratio Coherence: {freq_coherence:.4f}")
    print(f"    Energy Level Ratio Coherence: {energy_coherence:.4f}")
    print(f"  Total Interaction Coherence Score: {final_score:.4f}")
    print(f"  Interaction Outcome: {outcome}")

    return {
        'interaction_coherence_score': final_score,
        'outcome': outcome
    }

# --- Example Usage ---
if __name__ == "__main__":
    # Scenario 1: Highly PHI-aligned interaction (resonance)
    field1_A = {'base_phi_alignment': 0.9, 'frequency': 100.0, 'energy_level': 10.0}
    field1_B = {'base_phi_alignment': 0.8, 'frequency': 100.0 * PHI, 'energy_level': 10.0 * PHI}
    simulate_s_field_interaction(field1_A, field1_B)

    # Scenario 2: Low coherence interaction (damping)
    field2_A = {'base_phi_alignment': 0.2, 'frequency': 50.0, 'energy_level': 20.0}
    field2_B = {'base_phi_alignment': 0.3, 'frequency': 75.0, 'energy_level': 30.0}
    simulate_s_field_interaction(field2_A, field2_B)

    # Scenario 3: Mixed coherence (e.g., one aspect aligns well, others don't)
    field3_A = {'base_phi_alignment': 0.7, 'frequency': 70.0, 'energy_level': 5.0}
    field3_B = {'base_phi_alignment': 0.6, 'frequency': 70.0 * PHI, 'energy_level': 8.0} # Frequency aligns, energy doesn't
    simulate_s_field_interaction(field3_A, field3_B)

