import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import webbrowser

class ChronoResonator:
    def __init__(self):
        self.target_oscillations = 5.08e6  # Scaled from 5.08e30
        self.frequency = 1e6  # MHz, scaled from 3.6e11 Hz
        self.tau = 0.0764  # Decoherence time (s)
        self.target_speed = 88  # mph
        self.target_time = "1955-11-05 06:00:00"

        # GUI Setup
        self.root = tk.Tk()
        self.root.title("Manuela's Chrono-Resonator")
        self.root.geometry("600x400")
        self.root.configure(bg="#1C2526")  # DeLorean gray

        tk.Label(self.root, text="Chrono-Resonator Control", font=("Arial", 16, "bold"), bg="#1C2526", fg="white").pack(pady=10)
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
        self.duration_entry.insert(0, "0.001")
        self.duration_entry.pack()

        tk.Button(self.root, text="Activate Time Circuits", command=self.run_resonator, bg="#FF4500", fg="white").pack(pady=10)
        tk.Button(self.root, text="Play 'Power of Love'", command=self.play_music, bg="#00CED1", fg="white").pack(pady=5)

        self.deLorean_art = tk.Label(self.root, text="""
        ______
       /|_||_\\`.__
      (   _    _ _\\
      =|  _    _  |
       |  _   _   |
       |_________|
        """, font=("Courier", 10), bg="#1C2526", fg="silver")
        self.deLorean_art.pack()

    def play_music(self):
        webbrowser.open("https://www.youtube.com/watch?v=-NMph943tsw")
        messagebox.showinfo("Great Scott!", "Cranking up Huey Lewis, Manuela!")

    def run_resonator(self):
        try:
            speed = float(self.speed_entry.get())
            duration = float(self.duration_entry.get())
            target_time = self.date_entry.get()
            datetime.strptime(target_time, "%Y-%m-%d %H:%M:%S")

            t = np.linspace(0, duration, 1000)
            oscillations = self.frequency * t
            coherence = np.exp(-t / self.tau)

            model = LinearRegression()
            model.fit(t.reshape(-1, 1), coherence)
            predicted_coherence = model.predict([[duration]])[0]

            if speed < self.target_speed:
                messagebox.showwarning("Uh-oh!", "Need 88 mph, Manuela!")
                return
            if oscillations[-1] < self.target_oscillations:
                messagebox.showwarning("Not Enough Juice!", "More oscillations needed!")
                return
            if predicted_coherence < 0.5:
                messagebox.showwarning("Coherence Lost!", "Quantum coherence too low!")
                return

            messagebox.showinfo("Great Scott!", f"Time jump to {target_time}!\nThis is heavy, Manuela!")
            self.plot_waveform(t, coherence)

        except ValueError:
            messagebox.showerror("Error", "Invalid input! Check date, speed, or duration.")

    def plot_waveform(self, t, coherence):
        plt.figure(figsize=(8, 4))
        plt.plot(t, coherence, label="Quantum Coherence", color="cyan")
        plt.axhline(y=0.5, color="red", linestyle="--", label="Coherence Threshold")
        plt.title("Manuela's Chrono-Resonator: Quantum Coherence Waveform")
        plt.xlabel("Time (s)")
        plt.ylabel("Coherence Amplitude")
        plt.legend()
        plt.grid(True)
        plt.show()

    def start(self):
        self.root.mainloop()

if __name__ == "__main__":
    chrono = ChronoResonator()
    chrono.start()
