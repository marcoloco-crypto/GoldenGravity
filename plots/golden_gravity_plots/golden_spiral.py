import matplotlib.pyplot as plt
import numpy as np

def plot_fibonacci_spiral(n_terms=10):
    """
    Plots the Fibonacci spiral and guiding rectangles based on n_terms of the Fibonacci sequence.
    """
    fib_sequence = [0, 1]
    while len(fib_sequence) < n_terms:
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])

    fig, ax = plt.subplots(1, figsize=(8, 8))
    ax.set_aspect('equal')
    ax.set_title(f"Golden Spiral & Rectangles (up to {n_terms} terms)")
    ax.axis('off') # Hide axes for cleaner look

    x, y = 0, 0 # Current corner for drawing square
    dx, dy = 1, 0 # Direction vector for adding next square (right, up, left, down)

    # Plot the squares and calculate spiral points
    spiral_points_x = []
    spiral_points_y = []

    for i in range(1, n_terms): # Start from fib_sequence[1] = 1
        side = fib_sequence[i]

        # Draw the square
        # Adjust position based on direction to ensure correct placement
        if dx == 1 and dy == 0: # Moving right
            rect_x, rect_y = x, y
        elif dx == 0 and dy == 1: # Moving up
            rect_x, rect_y = x - side, y
        elif dx == -1 and dy == 0: # Moving left
            rect_x, rect_y = x - side, y - side
        elif dx == 0 and dy == -1: # Moving down
            rect_x, rect_y = x, y - side

        ax.add_patch(plt.Rectangle((rect_x, rect_y), side, side,
                                   edgecolor='gray', facecolor='lightgray', alpha=0.5))

        # Calculate arc points for the spiral. This method directly calculates points on the spiral.
        if i >= 1: # For sides of 1 or more
            center_x, center_y = 0, 0
            start_angle = 0
            end_angle = 0

            # Determine center and angles for the current square's arc segment
            if dx == 1 and dy == 0: # Moved right (square to the right)
                center_x, center_y = x, y + side # Center of arc is top-left of *new* square
                start_angle, end_angle = 270, 360 # From bottom-left of arc's bounding box
            elif dx == 0 and dy == 1: # Moved up (square above)
                center_x, center_y = x, y # Center of arc is bottom-right of *new* square
                start_angle, end_angle = 180, 270 # From bottom-right
            elif dx == -1 and dy == 0: # Moved left (square to the left)
                center_x, center_y = x + side, y # Center of arc is top-right of *new* square
                start_angle, end_angle = 90, 180 # From top-right
            elif dx == 0 and dy == -1: # Moved down (square below)
                center_x, center_y = x + side, y + side # Center of arc is bottom-left of *new* square
                start_angle, end_angle = 0, 90 # From top-left
            
            # Generate points for this arc segment
            theta = np.linspace(np.radians(start_angle), np.radians(end_angle), 50)
            r = side # Radius is the side length
            current_arc_x = center_x + r * np.cos(theta)
            current_arc_y = center_y + r * np.sin(theta)
            
            # Add to overall spiral points
            spiral_points_x.extend(current_arc_x)
            spiral_points_y.extend(current_arc_y)

        # Update position and direction for the next square
        if dx == 1 and dy == 0: # Moved right, next square is up
            x += side
            dx, dy = 0, 1
        elif dx == 0 and dy == 1: # Moved up, next square is left
            y += side
            dx, dy = -1, 0
        elif dx == -1 and dy == 0: # Moved left, next square is down
            x -= side
            dx, dy = 0, -1
        elif dx == 0 and dy == -1: # Moved down, next square is right
            y -= side
            dx, dy = 1, 0
            
    # Plot the full spiral curve
    ax.plot(spiral_points_x, spiral_points_y, color='red', linewidth=2)

    # Adjust limits to fit all squares and spiral
    ax.autoscale_view()
    plt.show() # For interactive display

# Run the plot for a few terms
plot_fibonacci_spiral(n_terms=9)
