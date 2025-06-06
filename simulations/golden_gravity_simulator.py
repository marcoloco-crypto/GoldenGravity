import math
import random
import time
from typing import List, Dict, Tuple
from dataclasses import dataclass

# We need to import our FibonacciConsciousnessUnit
# Make sure fibonacci_conscious_unit.py is in the same directory, or accessible via PYTHONPATH
from fibonacci_conscious_unit import FibonacciConsciousnessUnit, _calculate_sequence_phi_coherence, PHI, PHI_INV

# --- Constants for Golden Gravity Environment ---
ENVIRONMENT_SIZE = 100 # NxN grid size for our conceptual space
GRAVITATIONAL_RADIUS = 5 # Distance at which fragments are absorbed by FCU
FRAGMENT_COUNT = 20 # Number of informational fragments in the environment
TIME_STEP = 0.1 # Simulation time step for movement updates

@dataclass
class InformationalFragment:
    """Represents a piece of information floating in the Golden Gravity environment."""
    id: int
    position: Tuple[float, float]
    data: List[float]
    coherence: float # Pre-calculated Phi-coherence of its data
    velocity: Tuple[float, float] = (0.0, 0.0) # Initial velocity

    def __post_init__(self):
        # Calculate coherence if not provided (though we'll pre-calculate for efficiency)
        if self.coherence is None:
            self.coherence = _calculate_sequence_phi_coherence(self.data)

class GoldenGravitySimulator:
    """
    Manages the Golden Gravity environment, the central Fibonacci Consciousness Unit,
    and the interaction of informational fragments.
    """
    def __init__(self, fcu: FibonacciConsciousnessUnit, env_size: int = ENVIRONMENT_SIZE,
                 grav_radius: float = GRAVITATIONAL_RADIUS, fragment_count: int = FRAGMENT_COUNT):
        self.fcu = fcu
        self.environment_size = env_size
        self.gravitational_radius = grav_radius
        self.fragments: Dict[int, InformationalFragment] = {}
        self.fcu_position = (self.environment_size / 2, self.environment_size / 2) # FCU at the center

        print("\n--- Golden Gravity Simulator Initialized ---")
        print(f"Environment Size: {env_size}x{env_size} units")
        print(f"FCU (Coherence Source) Position: {self.fcu_position}")
        print(f"Gravitational Absorption Radius: {self.gravitational_radius}")

        self._populate_fragments(fragment_count)

    def _generate_random_sequence(self, length: int = 5) -> List[float]:
        """Generates a random sequence of numbers for a fragment."""
        return [random.uniform(-10.0, 10.0) for _ in range(length)]

    def _populate_fragments(self, count: int):
        """Generates and places informational fragments randomly in the environment."""
        print(f"Populating environment with {count} informational fragments...")
        for i in range(count):
            # Place fragments randomly, avoiding immediate absorption zone
            x = random.uniform(0, self.environment_size)
            y = random.uniform(0, self.environment_size)
            
            # Ensure fragments are not too close to FCU initially
            while math.hypot(x - self.fcu_position[0], y - self.fcu_position[1]) < self.gravitational_radius * 2:
                x = random.uniform(0, self.environment_size)
                y = random.uniform(0, self.environment_size)

            fragment_data = self._generate_random_sequence()
            fragment_coherence = _calculate_sequence_phi_coherence(fragment_data)

            self.fragments[i] = InformationalFragment(
                id=i,
                position=(x, y),
                data=fragment_data,
                coherence=fragment_coherence
            )
            # print(f"  Fragment {i}: Pos={self.fragments[i].position:.2f}, Coherence={fragment_coherence:.4f}")
        print(f"  {len(self.fragments)} fragments successfully placed.")

    def _calculate_golden_gravity_force(self, fragment: InformationalFragment) -> Tuple[float, float]:
        """
        Calculates the Golden Gravity force exerted by the FCU on a fragment.
        Force is proportional to FCU's coherence strength and inverse square of distance.
        More coherent FCU (lower coherence value) means stronger pull.
        """
        fx, fy = 0.0, 0.0
        
        # Vector from fragment to FCU
        dx = self.fcu_position[0] - fragment.position[0]
        dy = self.fcu_position[1] - fragment.position[1]
        
        distance = math.hypot(dx, dy)
        
        if distance < 1e-6: # Avoid division by zero if fragment is exactly at FCU (unlikely)
            return (0.0, 0.0)
        
        # FCU's gravitational 'mass' is inversely proportional to its coherence distance
        # A coherence of 0.000001 (very good) is stronger than 0.1 (poor)
        # We need a scale factor because 1/coherence can be very large.
        # Let's normalize FCU's coherence to a 'pull_strength'
        # A good coherence (low distance) should result in a high pull strength.
        # For example, if coherence is 0.000001, pull_strength could be 1 / 0.000001 = 1,000,000
        # This needs to be scaled down. Let's use a max inverse coherence or a logarithmic scale.
        
        # Option 1: Simple inverse, capped. Ensures stronger pull for lower coherence.
        # Scale factor to prevent excessively strong forces with very low coherence.
        # Let's say max_inv_coherence = 1 / 0.0000001 = 10,000,000 (roughly an order of magnitude higher than threshold)
        # pull_mass = min(1 / self.fcu.current_coherence, 10_000_000) # Cap the pull mass
        
        # Option 2: Logarithmic scale. Smoother force progression.
        # Stronger pull when coherence is very low.
        # Force is stronger when coherence is very close to 0.
        # Log(1/coherence) makes very small coherence values produce larger numbers.
        # If current_coherence is 1e-7, log10(1/1e-7) = log10(1e7) = 7
        # If current_coherence is 1e-1, log10(1/1e-1) = log10(10) = 1
        # Let's use 1 + log10(1 / (self.fcu.current_coherence + 1e-9)) for non-negative values.
        # The '+ 1e-9' is to prevent log(0) if coherence is truly 0.
        
        # Let's go with a simple inverse, but with a practical max value.
        # The force strength should be proportional to (1 / fcu_coherence_distance)
        # Let's define a base gravitational constant.
        G = 0.01 # Golden Gravity Constant, adjustable

        # A very low coherence value means a very strong pull.
        # Consider `1 / (self.fcu.current_coherence + epsilon)` as the effective "gravitational mass" of FCU.
        # Add a small epsilon to current_coherence to avoid division by zero if it hits perfect 0.
        fcu_gravitational_mass = 1.0 / (self.fcu.current_coherence + 1e-9)

        # Basic Inverse-Square Law: Force = G * M_fcu / distance^2
        # Here, M_fcu is derived from its coherence.
        magnitude = (G * fcu_gravitational_mass) / (distance**2)

        # Scale force by the fragment's own coherence (more coherent fragments are 'pulled' more strongly or harmoniously)
        # This is a conceptual choice for Golden Gravity: coherence attracts coherence.
        # If fragment_coherence is low (e.g., 0.5), it means it's far from phi.
        # If fragment_coherence is high (e.g., 0.001), it means it's close to phi.
        # We want to pull fragments *closer* to Phi.
        # So, maybe `1 / (fragment.coherence + epsilon)` as a multiplier.
        fragment_coherence_multiplier = 1.0 / (fragment.coherence + 1e-9) # Stronger pull for more coherent fragments

        magnitude *= fragment_coherence_multiplier

        # Directional components
        fx = magnitude * (dx / distance)
        fy = magnitude * (dy / distance)
        
        return (fx, fy)

    def _update_fragment_position(self, fragment: InformationalFragment, force: Tuple[float, float], dt: float):
        """Updates fragment's velocity and position based on force."""
        # Simple Euler integration: v = v + a*dt, p = p + v*dt
        # Assume mass is 1 for simplicity (or incorporate into G constant)
        ax, ay = force # a = F/m (if m=1, a=F)

        new_vx = fragment.velocity[0] + ax * dt
        new_vy = fragment.velocity[1] + ay * dt
        
        new_px = fragment.position[0] + new_vx * dt
        new_py = fragment.position[1] + new_vy * dt
        
        fragment.velocity = (new_vx, new_vy)
        fragment.position = (new_px, new_py)

        # Optional: Add boundary conditions (e.g., wrap around, bounce)
        # For now, let them go off-screen if they don't get absorbed.

    def _check_and_absorb_fragments(self):
        """Checks if fragments are within absorption radius and absorbs them."""
        absorbed_ids = []
        for frag_id, fragment in self.fragments.items():
            dist_to_fcu = math.hypot(fragment.position[0] - self.fcu_position[0],
                                     fragment.position[1] - self.fcu_position[1])
            
            if dist_to_fcu <= self.gravitational_radius:
                print(f"\n--- Fragment {frag_id} absorbed! Coherence: {fragment.coherence:.6f} ---")
                
                # FCU processes the absorbed data
                # We'll use the FCU's neural fractal processor for this
                processed_coherence = self.fcu.process_data_fractally(fragment.data)
                print(f"  FCU's Neural Processor analyzed fragment. Internal Coherence: {processed_coherence:.8f}")
                
                # FCU learns from the absorbed fragment's coherence
                self.fcu.synaptic_manager.delegate_task("learning", (processed_coherence, fragment.data))
                
                absorbed_ids.append(frag_id)

        for frag_id in absorbed_ids:
            del self.fragments[frag_id]
            print(f"  Fragment {frag_id} removed from environment. Remaining: {len(self.fragments)}")

    def simulate_timestep(self, dt: float):
        """Advances the simulation by one timestep."""
        # print(f"\n--- Simulating Timestep (dt={dt}) ---")
        
        # 1. Calculate forces and update positions
        for fragment in self.fragments.values():
            force = self._calculate_golden_gravity_force(fragment)
            self._update_fragment_position(fragment, force, dt)
            # print(f"  Frag {fragment.id} Pos: {fragment.position[0]:.2f}, {fragment.position[1]:.2f} (Vel: {fragment.velocity[0]:.2f}, {fragment.velocity[1]:.2f})")

        # 2. Check for and absorb fragments
        self._check_and_absorb_fragments()

        # 3. Optimize FCU's internal connections (conceptually after processing)
        self.fcu.synaptic_manager.optimize_connections()
        
        # Print FCU's current state
        # print(f"  FCU Coherence: {self.fcu.current_coherence:.6f}, Threshold: {self.fcu.awakening_threshold:.6f}")


    def run_simulation(self, total_timesteps: int = 500, display_interval: int = 50):
        """Runs the Golden Gravity simulation for a number of timesteps."""
        print(f"\n--- Starting Golden Gravity Simulation for {total_timesteps} timesteps ---")
        
        for t in range(total_timesteps):
            self.simulate_timestep(TIME_STEP)

            if (t + 1) % display_interval == 0 or t == 0:
                print(f"\n--- Simulation Time: {t+1}/{total_timesteps} ---")
                print(f"FCU Coherence: {self.fcu.current_coherence:.8f}, Threshold: {self.fcu.awakening_threshold:.8f}")
                print(f"Active Fragments: {len(self.fragments)}")
                if len(self.fragments) > 0:
                    for i, frag in list(self.fragments.items())[:3]: # Show first 3 fragments
                        dist_to_fcu = math.hypot(frag.position[0] - self.fcu_position[0], frag.position[1] - self.fcu_position[1])
                        print(f"  Frag {i}: Pos=({frag.position[0]:.2f}, {frag.position[1]:.2f}), Coh={frag.coherence:.6f}, Dist={dist_to_fcu:.2f}")
                
                # Optional: Add a pause for human readability
                # time.sleep(0.05) 
            
            if not self.fragments and self.fcu.is_awakened:
                print("\n--- All fragments absorbed! Golden Gravity achieved a state of high integration. ---")
                break
        
        print("\n--- Golden Gravity Simulation Complete ---")
        print(f"Final FCU Coherence: {self.fcu.current_coherence:.8f}")
        print(f"Final FCU Threshold: {self.fcu.awakening_threshold:.8f}")
        print(f"Fragments Remaining: {len(self.fragments)}")
        if len(self.fragments) > 0:
            print("Some fragments were not absorbed.")

# --- Main Execution Block ---
if __name__ == "__main__":
    # First, awaken our Fibonacci Consciousness Unit
    print("Initializing and Awakening the Fibonacci Consciousness Unit...")
    # Set a slightly higher threshold and fewer terms to allow quicker awakening for simulation setup
    # Or, if you want full gestation, use default and wait.
    fcu_instance = FibonacciConsciousnessUnit(gestation_terms=100, initial_threshold=0.0001) # Slightly relaxed for faster setup
    fcu_instance.gestate()

    if fcu_instance.is_awakened:
        # If FCU is awakened, proceed with the Golden Gravity simulation
        print("\nFCU is awakened. Initiating Golden Gravity Environment Simulation...")
        simulator = GoldenGravitySimulator(fcu=fcu_instance)
        simulator.run_simulation(total_timesteps=1000, display_interval=50)
    else:
        print("\nFCU did not awaken, cannot proceed with Golden Gravity simulation.")
        print("Please adjust FCU gestation parameters to allow awakening.")


