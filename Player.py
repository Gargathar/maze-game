import wasabi2d as w2d
import time
# Create a new scene
scene = w2d.Scene(width=800, height=600, background=(0.9, 0.9, 1.0), title="My Scene")
animate = w2d.animate 


class Player:
    
    def __init__(self):
        
        # Create a new square sprite for the Player
        self.sprite = scene.layers[1].add_rect(
            width=50,
            height=50,
            pos=(400, 300),
            color=(1, 0, 0),  # Red color
        )

        # Set flags for key presses
        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False
        self.space_pressed = False

        self.attacking = 0  
        self.direction = 0

    # Define movement functions
    def move_up(self):
        self.sprite.y -= 10
        self.direction = 90

    def move_down(self):
        self.sprite.y += 10
        self.direction = 270

    def move_left(self):
        self.sprite.x -= 10
        self.direction = 0

    def move_right(self):
        self.sprite.x += 10
        self.direction = 180



    # Remove the sword after the attack
    def attack(self):
        self.Sword = scene.layers[0].add_rect(
        width=10,
        height=50,
        pos=(400, 300),
        color=(0, 0, 0),
        # Black color for the sword
        )

    def done_swing(self):
        self.attacking = 0
        self.Sword.delete()
        if self.direction == 0:  # Player is facing left
            self.Sword.pos = (self.sprite.pos - (25, 0))
            animate(self.Sword, tween='linear', duration=0.3, angle=-3, on_finished=self.done_swing)
            
        elif self.direction == 90:  # Player is facing up
            self.Sword.pos = (self.sprite.pos + (0, 25))
            animate(self.Sword, tween='linear', duration=0.3, angle=3, on_finished=self.done_swing)
            
        elif self.direction == 180:  # Player is facing right
            self.Sword.pos = (self.sprite.pos + (25, 0))
            animate(self.Sword, tween='linear', duration=0.3, angle=3, on_finished=self.done_swing) 
            
        elif self.direction == 270:  # Player is facing down
            self.Sword.pos = (self.sprite.pos - (0, 25))
            animate(self.Sword, tween='linear', duration=0.3, angle=-3, on_finished=self.done_swing)
            
        # Position the sword at the sprite's position
        # for i in range(6):
        #     Sword.angle += (6)
        #     time.sleep(0.1)
        # time.sleep(5)
        # Remove the sword after the attack
        self.attacking = 0  # Reset attacking state


player = Player()
# Bind movement functions to arrow keys
@w2d.event
def on_key_down(key):
    if player.attacking == 1:
        pass
    elif player.attacking == 0:
        if key == w2d.keys.UP:
            player.up_pressed = True
        elif key == w2d.keys.DOWN:
            player.down_pressed = True
        elif key == w2d.keys.LEFT:
            player.left_pressed = True
        elif key == w2d.keys.RIGHT:
            player.right_pressed = True
        elif key == w2d.keys.SPACE:
            player.attack()
    else:
        print(player.attacking)



@w2d.event
def on_key_up(key):
    if player.attacking == 1:
        pass
    elif player.attacking == 0:
        if key == w2d.keys.UP:
            player.up_pressed = False
        elif key == w2d.keys.DOWN:
            player.down_pressed = False
        elif key == w2d.keys.LEFT:
            player.left_pressed = False
        elif key == w2d.keys.RIGHT:
            player.right_pressed = False
    else:
        print(player.attacking)

def update():
    if player.up_pressed:
        player.move_up()
    if player.down_pressed:
        player.move_down()
    if player.left_pressed:
        player.move_left()
    if player.right_pressed:
        player.move_right()
    w2d.clock.schedule(update, 1/60)



# Run the scene

update()
w2d.run()
