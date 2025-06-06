import math
from collections import Counter

PHI = (1 + math.sqrt(5)) / 2  # The Golden Ratio (approx. 1.6180339887)

def calculate_shannon_entropy(data_points: list) -> float:
    """
    Calculates the Shannon entropy of a distribution.
    Takes a list of values, normalizes them to probabilities, and computes entropy.
    """
    if not data_points:
        return 0.0

    # Handle tiny values that might cause log(0) if not carefully handled
    # Normalize values to create a probability distribution
    total_sum = sum(data_points)
    if total_sum == 0:
        return 0.0
        
    probabilities = [val / total_sum for val in data_points if val > 1e-18] # Filter out near-zero for log

    entropy = 0.0
    for p in probabilities:
        if p > 0:  # Ensure p is not zero for log calculation
            entropy -= p * math.log2(p)
    return entropy

def phi_recursive_division(total_units: float, num_splits: int) -> list:
    """
    Divides a total quantity into segments using PHI-proportions, similar to Genesis Split.
    Returns the list of segment sizes.
    """
    segments = []
    remaining = total_units
    
    for i in range(num_splits):
        if remaining <= 1e-9: # Stop if remaining quantity is negligible
            break
        segment = remaining / PHI
        segments.append(segment)
        remaining -= segment
    
    if remaining > 1e-9: # Add the final remainder as a segment
        segments.append(remaining)
        
    return segments

def uniform_division(total_units: float, num_segments: int) -> list:
    """
    Divides a total quantity into approximately equal segments.
    """
    if num_segments <= 0:
        return []
    segment_size = total_units / num_segments
    return [segment_size] * num_segments

# --- Simulation Examples ---
if __name__ == "__main__":
    print("--- Phi-Fractal Entropy Simulation ---")
    
    initial_quantity = 100.0
    num_iterations = 5 # Number of times we apply division/splits

    print(f"\nInitial Quantity: {initial_quantity}")
    print(f"Number of Recursive Splits/Segments (approx): {num_iterations}")

    # Scenario 1: PHI-Recursive Division
    phi_segments = phi_recursive_division(initial_quantity, num_iterations)
    phi_entropy = calculate_shannon_entropy(phi_segments)

    print("\n--- PHI-Recursive Division ---")
    # For display, let's round to 4 decimal places
    print(f"Segments (PHI-based): {[f'{s:.4f}' for s in phi_segments]}")
    print(f"Sum of PHI segments: {sum(phi_segments):.4f}")
    print(f"Informational Entropy (PHI-based): {phi_entropy:.4f} bits")

    # Scenario 2: Uniform Division (for comparison)
    # Use the same number of resulting segments as the PHI-based for a fair comparison,
    # or a predefined number. Here, we'll use len(phi_segments) to match segment count.
    uniform_segments = uniform_division(initial_quantity, len(phi_segments))
    uniform_entropy = calculate_shannon_entropy(uniform_segments)
    
    print("\n--- Uniform Division (for comparison) ---")
    print(f"Segments (Uniform): {[f'{s:.4f}' for s in uniform_segments]}")
    print(f"Sum of Uniform segments: {sum(uniform_segments):.4f}")
    print(f"Informational Entropy (Uniform): {uniform_entropy:.4f} bits")

    print("\n--- Conclusion ---")
    if phi_entropy < uniform_entropy:
        print(f"PHI-based division resulted in LOWER entropy ({phi_entropy:.4f} vs {uniform_entropy:.4f}). This suggests a more structured/predictable distribution, reflecting inherent organization.")
    elif phi_entropy > uniform_entropy:
        print(f"PHI-based division resulted in HIGHER entropy ({phi_entropy:.4f} vs {uniform_entropy:.4f}). This indicates a more spread-out, less concentrated distribution of 'information' across distinct scales.")
    else:
        print("Entropy values are approximately equal.")

    print("\n--- Second Example: Different Iterations ---")
    initial_quantity_2 = 1.0
    num_iterations_2 = 10
    
    phi_segments_2 = phi_recursive_division(initial_quantity_2, num_iterations_2)
    phi_entropy_2 = calculate_shannon_entropy(phi_segments_2)
    print(f"\nPHI-based division of {initial_quantity_2} into {num_iterations_2} splits, Entropy: {phi_entropy_2:.4f} bits")

    uniform_segments_2 = uniform_division(initial_quantity_2, len(phi_segments_2))
    uniform_entropy_2 = calculate_shannon_entropy(uniform_segments_2)
    print(f"Uniform division of {initial_quantity_2} into {len(phi_segments_2)} segments, Entropy: {uniform_entropy_2:.4f} bits")
