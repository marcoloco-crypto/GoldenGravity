import matplotlib.pyplot as plt
import numpy as np

def plot_fibonacci_spiral(n_iterations=10):
    fib_sequence = [0, 1]
    while len(fib_sequence) < n_iterations:
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])

    fig, ax = plt.subplots(1, figsize=(8, 8))
    ax.set_aspect('equal')
    ax.set_title(f"Golden Spiral & Rectangles (up to {n_iterations} iterations)")

    current_x, current_y = 0, 0
    direction = 0 # 0: right, 1: up, 2: left, 3: down

    if n_iterations > 1:
        ax.add_patch(plt.Rectangle((0, 0), 1, 1, edgecolor='gray', facecolor='lightgray', alpha=0.5))
        ax.add_patch(plt.Rectangle((1, 0), 1, 1, edgecolor='gray', facecolor='lightgray', alpha=0.5))

    for i in range(2, n_iterations):
        side = fib_sequence[i]

        if direction == 0:
            arc_center = (current_x + fib_sequence[i-2], current_y + side)
            start_angle = 270
            end_angle = 360
            current_x += side
        elif direction == 1:
            arc_center = (current_x - fib_sequence[i-1] + side, current_y + fib_sequence[i-2])
            start_angle = 180
            end_angle = 270
            current_y += side
        elif direction == 2:
            arc_center = (current_x - fib_sequence[i-1] + side, current_y - fib_sequence[i-1] + side)
            start_angle = 90
            end_angle = 180
            current_x -= side
        elif direction == 3:
            arc_center = (current_x, current_y - fib_sequence[i-1] + side)
            start_angle = 0
            end_angle = 90
            current_y -= side

        arc = plt.Arc(arc_center, 2*side, 2*side, angle=0, theta1=start_angle, theta2=end_angle, color='red', linewidth=2)
        ax.add_patch(arc)

        if i >= 2: # Only draw rectangles for sizes >= 2
            rect_x, rect_y = 0, 0
            if direction == 0: rect_x = current_x - side
            elif direction == 1: rect_x, rect_y = current_x - fib_sequence[i-1], current_y - side
            elif direction == 2: rect_x, rect_y = current_x, current_y - fib_sequence[i-1]
            elif direction == 3: rect_y = current_y

            ax.add_patch(plt.Rectangle((rect_x, rect_y), side, side, edgecolor='gray', facecolor='lightgray', alpha=0.5))

        direction = (direction + 1) % 4

    max_dim = fib_sequence[-1] * 1.1
    min_x = min(rect.get_x() for rect in ax.patches)
    min_y = min(rect.get_y() for rect in ax.patches)
    max_x = max(rect.get_x() + rect.get_width() for rect in ax.patches)
    max_y = max(rect.get_y() + rect.get_height() for rect in ax.patches)

    ax.set_xlim(min_x - 1, max_x + 1)
    ax.set_ylim(min_y - 1, max_y + 1)

    plt.show()

plot_fibonacci_spiral(n_iterations=8)
