PHI_PI = 5.083203692

def compute_coherence_score(entanglement_density):
    """Calculate coherence score using phi * pi scaling."""
    return 1 + PHI_PI * entanglement_density

if __name__ == "__main__":
    print("--- Energy Coherence Score Examples ---")
    print(f"Scenario 1 (High Coherence): {compute_coherence_score(0.1):.4f}")  # 1.5083
    print(f"Scenario 2 (Low Coherence): {compute_coherence_score(0.01):.4f}")  # 1.0508
    print(f"Scenario 3 (Moderate Coherence): {compute_coherence_score(0.05):.4f}")  # 1.2542
