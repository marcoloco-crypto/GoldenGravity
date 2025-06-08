import random
import espeak

espeak.init()

def generate_dna(cycle: int, controlled: bool = True) -> list[float]:
    dna = [1, 1]
    while len(dna) < max(10, cycle + 5):
        dna.append(dna[-1] + dna[-2] if controlled else dna[-1] + random.uniform(0.5, 2.0) * dna[-1])
    return dna

def calculate_coherence(dna: list[float]) -> float:
    if len(dna) < 2: return 1.0
    return sum(abs(dna[i] / dna[i-1] - 1.618) for i in range(1, len(dna))) / (len(dna) - 1)

def save_dna_frame(dna: list[float], cycle: int, name: str):
    dot = Digraph(format='png')
    for i, val in enumerate(dna[:8]):
        dot.node(str(i), label=f"{val:.2f}", color="orange")
        if i > 0: dot.edge(str(i-1), str(i))
    dot.node("taco", label="🌮")
    dot.attr(label=f"Cycle {cycle}: {name}")
    dot.render(f"{name}_cycle_{cycle}", cleanup=True)

HORIZON_THRESHOLD = 0.000005
for cycle in range(20):
    controlled_dna = generate_dna(cycle, True)
    coh_controlled = calculate_coherence(controlled_dna)
    delta = 1.618 * 3.142 * coh_controlled
    print(f"Cycle {cycle} [Controlled_AI]: DNA={controlled_dna[:5]}..., Coherence={coh_controlled:.6f}, Delta={delta:.3f}")
    espeak.synth(f"Cycle {cycle}, Coherence {coh_controlled:.6f}, Delta {delta:.3f}")
    if coh_controlled < HORIZON_THRESHOLD:
        print("🌮 TACO STRIKE! Controlled_AI HITS EVENT HORIZON WITH DELTA LAMBDA PHI!")
        print(f"Coherence < {HORIZON_THRESHOLD}, phi * pi * delta = {1.618 * 3.142 * delta:.2f}")
        espeak.synth("Taco Strike! Horizon reached with Delta Lambda Phi!")
        save_dna_frame(controlled_dna, cycle, "Controlled_AI")
