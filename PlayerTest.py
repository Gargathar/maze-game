import turtle

# Create a new turtle screen and set its background color
screen=turtle.Screen()
turtle.Screen().bgcolor("Gray")
turtle.Screen().title("Turtle Movement Example")
turtle.Screen().setup(width=800, height=600)

# Create a new turtle object

turtle.shape("square")
turtle.speed(1)
turtle.color("red")
turtle.penup()  # Lift the pen to avoid drawing lines
# Function to move the square up
def move_up():
    turtle.setheading(90)
    turtle.forward(50)

# Function to move the square down
def move_down():
    turtle.setheading(270)
    turtle.forward(50)

# Function to move the square left
def move_left():
    turtle.setheading(180)
    turtle.forward(50)

# Function to move the square right
def move_right():
    turtle.setheading(0)
    turtle.forward(50)

# Bind the arrow keys to the movement functions
screen.listen()  # Start listening for key events
screen.onkey(move_up, "Up")
screen.onkey(move_down, "Down")
screen.onkey(move_left, "Left")
screen.onkey(move_right, "Right")

turtle.done()  # Finish the turtle graphics
