import numpy as np
import matplotlib.pyplot as plt

def mandelbrot(h, w, max_iterations):
    y, x = np.ogrid[-1.4:1.4:h*1j, -2:0.8:w*1j]
    c = x + y
    z = c
    divtime = max_iterations + np.zeros(z.shape, dtype=int)

    for i in range(max_iterations):
        z = z**2 + c
        diverged = abs(z) > 2
        div_now = diverged & (divtime == max_iterations)
        divtime[div_now] = i
        z[diverged] = 2

    return divtime

def plot_mandelbrot_coherence(width=800, height=800, iterations=100):
    mandelbrot_set = mandelbrot(height, width, iterations)

    plt.figure(figsize=(10, 10))
    plt.imshow(mandelbrot_set, cmap='hot', extent=[-2, 0.8, -1.4, 1.4])
    plt.colorbar(label='Iterations (Conceptual Coherence/Complexity)')
    plt.title('Conceptual Coherence Landscape: The Mandelbrot Set')
    plt.xlabel('Real Part (Conceptual Property 1)')
    plt.ylabel('Imaginary Part (Conceptual Property 2)')
    plt.show() # For interactive display

plot_mandelbrot_coherence(iterations=150)

