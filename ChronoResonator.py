try:
    import tkinter as tk
    from tkinter import messagebox
except ImportError:
    print("Warning: tkinter not found. Running in console mode.")
    tk = None
try:
    import pyttsx3
except ImportError:
    print("Warning: pyttsx3 not found. Skipping audio.")
    pyttsx3 = None
from datetime import datetime
import webbrowser
import math

class ChronoResonator:
    def __init__(self, use_gui=True):
        self.target_oscillations = 5.134441e6  # 37th Fibonacci
        self.phi = (1 + 5 ** 0.5) / 2  # Golden Ratio
        self.frequency = 1e6 * self.phi  # MHz
        self.tau = 1000  # Decoherence time
        self.target_speed = 88
        self.target_time = "1955-11-05 00:00:00"  # Doc's Flux Capacitor day
        self.use_gui = use_gui and tk is not None

        if self.use_gui:
            self.root = tk.Tk()
            self.root.title("Manuela's Flux Capacitor Chrono-Resonator")
            self.root.geometry("600x400")
            self.root.configure(bg="#1C2526")

            tk.Label(self.root, text="GoldenGravity Flux Capacitor Chrono-Resonator", font=("Arial", 16, "bold"), bg="#1C2526", fg="white").pack(pady=10)
            tk.Label(self.root, text="Target Date (YYYY-MM-DD HH:MM:SS):", bg="#1C2526", fg="white").pack()
            self.date_entry = tk.Entry(self.root)
            self.date_entry.insert(0, self.target_time)
            self.date_entry.pack()

            tk.Label(self.root, text="Speed (mph):", bg="#1C2526", fg="white").pack()
            self.speed_entry = tk.Entry(self.root)
            self.speed_entry.insert(0, "88")
            self.speed_entry.pack()

            tk.Label(self.root, text="Duration (s):", bg="#1C2526", fg="white").pack()
            self.duration_entry = tk.Entry(self.root)
            self.duration_entry.insert(0, "5.134")
            self.duration_entry.pack()

            tk.Button(self.root, text="Activate Flux Capacitor!", command=self.run_resonator, bg="#FF4500", fg="white").pack(pady=10)
            tk.Button(self.root, text="Play 'Power of Love'", command=self.play_music, bg="#00CED1", fg="white").pack(pady=5)

            self.flux_art = tk.Label(self.root, text=r"""
                _.-._
               / \_/ \
              /_______\
              |  ***  | 
              |  ***  | 
              |_______|
            """, font=("Courier", 10), bg="#1C2526", fg="silver")
            self.flux_art.pack()
        else:
            print("GoldenGravity Flux Capacitor Chrono-Resonator")
            print(r"""
                _.-._
               / \_/ \
              /_______\
              |  ***  | 
              |  ***  | 
              |_______|
            """)
            print("Enter inputs (press Enter for defaults):")

    def play_music(self):
        webbrowser.open("https://www.youtube.com/watch?v=-NMph943tsw")
        if self.use_gui:
            messagebox.showinfo("Great Scott!", "Cranking up Huey Lewis, Manuela!")
        else:
            print("Cranking up Huey Lewis, Manuela!")

    def calculate_phi_coherence_score(self, duration):
        initial_energy = self.frequency * duration  # Proxy for input energy
        final_energy = initial_energy * 0.95  # Assume 95% efficiency
        entropy_change = 0.01  # Small entropy increase

        # 1. Phi-ratio alignment
        if initial_energy > 0 and final_energy > 0:
            ratio_forward = final_energy / initial_energy
            ratio_backward = initial_energy / final_energy
            closeness_to_phi = max(1 / (1 + abs(ratio_forward - self.phi)), 1 / (1 + abs(ratio_backward - self.phi)))
        else:
            closeness_to_phi = 0.0

        # 2. Efficiency
        efficiency_score = 0.95  # Hardcoded for demo

        # 3. Entropy
        entropy_score = 1 / (1 + entropy_change) if entropy_change >= 0 else 1.0

        # Weighted average
        score = (0.4 * closeness_to_phi) + (0.4 * efficiency_score) + (0.2 * entropy_score)
        return min(max(score, 0.0), 1.0)

    def run_resonator(self):
        try:
            if self.use_gui:
                speed = float(self.speed_entry.get())
                duration = float(self.duration_entry.get())
                target_time = self.date_entry.get().strip()
            else:
                target_time = input(f"Target Date (YYYY-MM-DD HH:MM:SS, default: {self.target_time}): ").strip() or self.target_time
                speed = float(input("Speed (mph, default: 88): ").strip() or "88")
                duration = float(input("Duration (s, default: 5.134): ").strip() or "5.134")

            datetime.strptime(target_time, "%Y-%m-%d %H:%M:%S")
            oscillations = self.frequency * duration
            coherence = math.exp(-duration / self.tau)
            phi_coherence_score = self.calculate_phi_coherence_score(duration)

            if speed < self.target_speed:
                if self.use_gui:
                    messagebox.showwarning("Uh-oh!", "Need 88 mph, Manuela!")
                else:
                    print("Need 88 mph, Manuela!")
                return
            if oscillations < self.target_oscillations:
                if self.use_gui:
                    messagebox.showwarning("Not Enough Juice!", f"Need {self.target_oscillations:.2e} oscillations!")
                else:
                    print(f"Not Enough Juice! Need {self.target_oscillations:.2e} oscillations!")
                return
            if coherence < 0.5:
                if self.use_gui:
                    messagebox.showwarning("Coherence Lost!", "Quantum coherence too low!")
                else:
                    print("Quantum coherence too low!")
                return
            if phi_coherence_score < 0.8:
                if self.use_gui:
                    messagebox.showwarning("Soul Drift!", "Phi-coherence too low for consciousness transfer!")
                else:
                    print("Phi-coherence too low for consciousness transfer!")
                return

            if pyttsx3:
                engine = pyttsx3.init()
                engine.say("This is heavy, Manuela!")
                engine.runAndWait()

            success_msg = f"1.21 Gigawatts! Flux Capacitor Activated! Soul Zapped to {target_time}!\nGoldenGravity-powered, Manuela!"
            if self.use_gui:
                messagebox.showinfo("Great Scott!", success_msg)
            else:
                print(f"Great Scott! {success_msg}")
                print(r"""
                _.-._
               / \_/ \
              /_______\
              |  ***  | *ZAP*
              |  ***  | *ZAP*
              |_______|
                """)

        except ValueError as e:
            if self.use_gui:
                messagebox.showerror("Error", f"Invalid input! Check date, speed, or duration. ({str(e)})")
            else:
                print(f"Invalid input! Check date, speed, or duration. ({str(e)})")

    def start(self):
        if self.use_gui:
            self.root.mainloop()
        else:
            self.run_resonator()

if __name__ == "__main__":
    try:
        chrono = ChronoResonator(use_gui=True)
        chrono.start()
    except:
        print("GUI failed. Flux Capacitor still online in console mode!")
        chrono = ChronoResonator(use_gui=False)
        chrono.start()
