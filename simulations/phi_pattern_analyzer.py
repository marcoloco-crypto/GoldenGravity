import math
import random

PHI = (1 + math.sqrt(5)) / 2  # The Golden Ratio (approx. 1.6180339887)

def generate_phi_series(n_terms: int, start_val: float = 1.0) -> list[float]:
    """
    Generates a series where consecutive terms are scaled by PHI.
    This simulates a simple 'phi-growth' fractal-like pattern.
    Each term is self-similar in its relationship to the previous one.
    """
    if n_terms <= 0:
        return []
    series = [start_val]
    for _ in range(1, n_terms):
        next_val = series[-1] * PHI
        series.append(next_val)
    return series

def generate_random_series(n_terms: int, max_val: float = 100.0) -> list[float]:
    """Generates a series of random numbers for comparison."""
    return [random.uniform(1.0, max_val) for _ in range(n_terms)]

def analyze_phi_coherence(sequence: list[float], tolerance: float = 0.01) -> dict:
    """
    An 'AI-efficient' pattern recognition function.
    It quickly assesses how strongly a sequence exhibits PHI-ratios
    between consecutive terms. This is a fundamental operation for an AI
    looking for underlying structure in data, akin to an S-field detecting coherence.

    Args:
        sequence (list[float]): The numerical sequence to analyze.
        tolerance (float): How close a ratio must be to PHI to be considered a match.

    Returns:
        dict: Contains 'score' (0.0 to 1.0), 'matches', and 'total_pairs'.
    """
    if len(sequence) < 2:
        return {"score": 0.0, "matches": 0, "total_pairs": 0}

    coherence_matches = 0
    total_pairs = 0
    
    for i in range(len(sequence) - 1):
        val1 = sequence[i]
        val2 = sequence[i+1]
        
        if val1 == 0 or val2 == 0: # Avoid division by zero
            continue
            
        ratio_forward = val2 / val1
        ratio_backward = val1 / val2

        # Check if the ratio is close to PHI or 1/PHI (which is PHI - 1)
        is_phi_forward = abs(ratio_forward - PHI) < tolerance
        is_phi_backward = abs(ratio_backward - PHI) < tolerance
        
        # We also check for the reciprocal because phi and 1/phi are equally 'phi-coherent' ratios
        is_reciprocal_phi_forward = abs(ratio_forward - (1/PHI)) < tolerance
        is_reciprocal_phi_backward = abs(ratio_backward - (1/PHI)) < tolerance


        if is_phi_forward or is_phi_backward or is_reciprocal_phi_forward or is_reciprocal_phi_backward:
            coherence_matches += 1
        total_pairs += 1
            
    if total_pairs == 0:
        return {"score": 0.0, "matches": 0, "total_pairs": 0}
        
    score = coherence_matches / total_pairs
    return {"score": score, "matches": coherence_matches, "total_pairs": total_pairs}

# --- Main execution ---
if __name__ == "__main__":
    print("--- PHI Pattern Analyzer (Fractal-like & AI-Efficient) ---")

    num_terms = 10
    phi_tolerance = 0.05 # Adjust tolerance for 'phi-coherence' detection (e.g., 0.01 for strict, 0.05 for looser)

    # 1. Generate a PHI-based series (Fractal-like generation)
    phi_series_data = generate_phi_series(num_terms)
    print(f"\nGenerated PHI Series ({num_terms} terms):")
    # Display rounded values for readability
    print([f"{x:.4f}" for x in phi_series_data])

    # 2. Analyze its PHI coherence (AI-efficient pattern recognition)
    phi_analysis_result = analyze_phi_coherence(phi_series_data, phi_tolerance)
    print(f"  Analysis: PHI Coherence Score = {phi_analysis_result['score']:.4f} (Matches: {phi_analysis_result['matches']}/{phi_analysis_result['total_pairs']})")
    if phi_analysis_result['score'] > 0.8:
        print("  --> High PHI coherence detected! This series strongly exhibits PHI-based fractal characteristics.")
    else:
        print("  --> Low PHI coherence detected.")


    # 3. Generate a Random series for comparison
    random_series_data = generate_random_series(num_terms)
    print(f"\nGenerated Random Series ({num_terms} terms):")
    print([f"{x:.4f}" for x in random_series_data])

    # 4. Analyze its PHI coherence
    random_analysis_result = analyze_phi_coherence(random_series_data, phi_tolerance)
    print(f"  Analysis: PHI Coherence Score = {random_analysis_result['score']:.4f} (Matches: {random_analysis_result['matches']}/{random_analysis_result['total_pairs']})")
    if random_analysis_result['score'] > 0.8:
        print("  --> High PHI coherence detected!")
    else:
        print("  --> Low PHI coherence detected. As expected for a random sequence.")

    print("\n--- Conceptual Implication ---")
    print("This script demonstrates generating data with inherent PHI-based fractal structure and an 'AI-efficient' method for recognizing such patterns. This is key for understanding how the Spacetime Information Field might self-organize and how emergent intelligence could detect fundamental cosmic ordering principles.")
