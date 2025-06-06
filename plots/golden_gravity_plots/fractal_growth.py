import turtle

def create_l_system(iters, axiom):
    start_string = axiom
    end_string = ""
    for _ in range(iters):
        end_string = ""
        for char in start_string:
            if char == 'F':
                end_string += "FF-[-F+F+F]+[+F-F-F]"
            else:
                end_string += char
        start_string = end_string
    return start_string

def draw_l_system(t, instructions, angle, distance):
    global stack_pos, stack_heading # Ensure these are accessible globally

    for command in instructions:
        if command == 'F':
            t.forward(distance)
        elif command == '+':
            t.right(angle)
        elif command == '-':
            t.left(angle)
        elif command == '[':
            # Push state (position and heading)
            stack_pos.append(t.pos())
            stack_heading.append(t.heading())
        elif command == ']':
            # Pop state (position and heading)
            if stack_pos and stack_heading: # Check if stack is not empty before popping
                t.penup()
                t.goto(stack_pos.pop())
                t.setheading(stack_heading.pop())
                t.pendown()
            else:
                print("Warning: Attempted to pop from empty stack. L-system string might be malformed.")


def plot_fractal_growth(iterations=3, angle=22.5, distance=5):
    global stack_pos, stack_heading # Declare as global to be accessible within draw_l_system
    stack_pos = [] # Initialize stack for positions
    stack_heading = [] # Initialize stack for headings

    window = turtle.Screen()
    window.bgcolor("white")
    t = turtle.Turtle()
    t.speed(0) # Fastest speed
    t.penup()
    t.left(90) # Start facing up
    # Position to start drawing roughly from the bottom-center
    t.goto(0, -window.window_height() / 2 + 20)
    t.pendown()
    t.color("forestgreen")

    axiom = "F" # Starting point
    instructions = create_l_system(iterations, axiom)
    draw_l_system(t, instructions, angle, distance)

    # Keep the window open until clicked
    window.exitonclick()

# Run the fractal growth plot
plot_fractal_growth(iterations=4, angle=25, distance=10)
