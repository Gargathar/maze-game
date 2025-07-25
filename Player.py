import wasabi2d as w2d

# Create a new scene
scene = w2d.Scene(width=800, height=600, title="My Scene")

# Create a new square sprite for the player
player = scene.layers[0].add_rect(
    width=50,
    height=50,
    pos=(400, 300),
    color=(1, 0, 0),  # Red color
)

# Define movement functions
def move_up():
    player.y -= 5

def move_down():
    player.y += 5

def move_left():
    player.x -= 5

def move_right():
    player.x += 5

# Set flags for key presses
up_pressed = False
down_pressed = False
left_pressed = False
right_pressed = False

# Bind movement functions to arrow keys
@w2d.event
def on_key_down(key):
    global up_pressed, down_pressed, left_pressed, right_pressed
    if key == w2d.keys.UP:
        up_pressed = True
    elif key == w2d.keys.DOWN:
        down_pressed = True
    elif key == w2d.keys.LEFT:
        left_pressed = True
    elif key == w2d.keys.RIGHT:
        right_pressed = True

@w2d.event
def on_key_up(key):
    global up_pressed, down_pressed, left_pressed, right_pressed
    if key == w2d.keys.UP:
        up_pressed = False
    elif key == w2d.keys.DOWN:
        down_pressed = False
    elif key == w2d.keys.LEFT:
        left_pressed = False
    elif key == w2d.keys.RIGHT:
        right_pressed = False

def update():
    global up_pressed, down_pressed, left_pressed, right_pressed
    if up_pressed:
        move_up()
    if down_pressed:
        move_down()
    if left_pressed:
        move_left()
    if right_pressed:
        move_right()
    w2d.clock.schedule(update, 1/60)

# Run the scene
update()
w2d.run()
