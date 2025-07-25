import wasabi2d as w2d
import time
# Create a new scene
scene = w2d.Scene(width=800, height=600, background=(0.9, 0.9, 1.0), title="My Scene")
animate = w2d.animate 
# Create a new square sprite for the player
player = scene.layers[1].add_rect(
    width=50,
    height=50,
    pos=(400, 300),
    color=(1, 0, 0),  # Red color
)


attacking = 0  
direction = 0
# Define movement functions
def move_up():
    player.y -= 10
    direction = 90

def move_down():
    player.y += 10
    direction = 270

def move_left():
    player.x -= 10
    direction = 0

def move_right():
    player.x += 10
    direction = 180
  # Remove the sword after the attack
def attack():
    Sword = scene.layers[0].add_rect(
    width=10,
    height=50,
    pos=(400, 300),
    color=(0, 0, 0),
      # Black color for the sword
    
)

    def done_swing():
        attacking = 0
        Sword.delete()
    if direction == 0:  # Player is facing left
        Sword.pos = (player.pos - (25, 0))
        animate(Sword, tween='linear', duration=0.3, angle=-3, on_finished=done_swing)
        
    elif direction == 90:  # Player is facing up
        Sword.pos = (player.pos + (0, 25))
        animate(Sword, tween='linear', duration=0.3, angle=3, on_finished=done_swing )
        
    elif direction == 180:  # Player is facing right
        Sword.pos = (player.pos + (25, 0))
        animate(Sword, tween='linear', duration=0.3, angle=3, on_finished=done_swing ) 
        
    elif direction == 270:  # Player is facing down
        Sword.pos = (player.pos - (0, 25))
        animate(Sword, tween='linear', duration=0.3, angle=-3, on_finished=done_swing )
        
      # Position the sword at the player's position
    # for i in range(6):
    #     Sword.angle += (6)
    #     time.sleep(0.1)
    # time.sleep(5)
    # Remove the sword after the attack
    attacking = 0  # Reset attacking state
    

# Set flags for key presses
up_pressed = False
down_pressed = False
left_pressed = False
right_pressed = False
space_pressed = False
# Bind movement functions to arrow keys
@w2d.event
def on_key_down(key):
    global up_pressed, down_pressed, left_pressed, right_pressed , space_pressed
    if attacking == 1:
        pass
    elif attacking == 0:
        if key == w2d.keys.UP:
            up_pressed = True
        elif key == w2d.keys.DOWN:
            down_pressed = True
        elif key == w2d.keys.LEFT:
            left_pressed = True
        elif key == w2d.keys.RIGHT:
            right_pressed = True
        elif key == w2d.keys.SPACE:
            attack()
    else:
        print(attacking)



@w2d.event
def on_key_up(key):
    global up_pressed, down_pressed, left_pressed, right_pressed, space_pressed
    if attacking == 1:
        pass
    elif attacking == 0:
        if key == w2d.keys.UP:
            up_pressed = False
        elif key == w2d.keys.DOWN:
            down_pressed = False
        elif key == w2d.keys.LEFT:
            left_pressed = False
        elif key == w2d.keys.RIGHT:
            right_pressed = False
    else:
        print(attacking)

def update():
    global up_pressed, down_pressed, left_pressed, right_pressed, space_pressed
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
