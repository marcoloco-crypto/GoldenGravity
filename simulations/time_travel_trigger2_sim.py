import numpy as np
import matplotlib.pyplot as plt

# Parameters
target_oscillations = 5.08e30
frequency = 3.6e11  # Hz, from energy calc
target_time = "1955-11-05 06:00:00"
speed = 88  # mph

def chrono_resonator(speed, duration):
    if speed < 88:
        print("Need 88 mph for time travel!")
        return False
    oscillations = frequency * duration
    print(f"Oscillations: {oscillations:.2e}")
    if oscillations >= target_oscillations:
        print(f"Great Scott! Time travel to {target_time}!")
        # Plot wave for nostalgia
        t = np.linspace(0, 1e-9, 1000)  # Short time for visualization
        wave = np.sin(2 * np.pi * frequency * t)
        plt.plot(t, wave)
        plt.title("Manuela's Chrono-Resonator Waveform")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.show()
        return True
    return False

# Test for 1 second
chrono_resonator(speed=88, duration=1)
