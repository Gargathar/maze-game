import sys
sys.dont_write_bytecode = True
# This is a holy warding spell, one that is required for my computer for some stupid reason
# Please place it at the top of each new file, such that I may remain protected


import wasabi2d as w2d
import time
import math

from chunk_generation import Chunk, Cell
from maze_as_a_whole import Maze

# Create a new scene
scene = w2d.Scene(width=800, height=600, background=(0, 0, 0), title="My Scene")
animate = w2d.animate 

TILE_LEN = 50

class Player:
	
	def __init__(self):

		self.maze = Maze()
		self.map_position = [self.maze.MAP_LEN//2, self.maze.MAP_LEN//2] # [Y, X], NOT THE OTHER WAY AROUND!!!!!

		self.rendered_room_stuff:list[set[Cell]] = []
		
		# Create a new square sprite for the Player
		self.sprite = scene.layers[1].add_rect(
			width=TILE_LEN,
			height=TILE_LEN,
			pos=(50, 50),
			color=(1, 0, 0),  # Red color
		)

		# Set flags for key presses
		self.up_pressed:bool = False
		self.down_pressed:bool = False
		self.left_pressed:bool = False
		self.right_pressed:bool = False
		self.space_pressed:bool = False

		self.attacking = 0  

		self.direction = 0
		self.last_ver_move_up:bool = True
		self.last_hor_move_right:bool = True

		self.last_orb_shot_time = 0
		self.current_orb_type_index = 0
		self.orb_types = ["blast", "explosion"]



	def render_chunk(self, map_y, map_x): 
		"""
		Here so that there's only one scene to render, despite multiple layers
		
		Single hunk rendering starts at (0,0), then builds right and down
		multi-chunk rendering starts some offset (seen below), then does the same
		"""
		chunk:Chunk = self.maze.map[map_y][map_x]
		pix_start_y = self.maze.center_chunk.CHUNKLEN * TILE_LEN * (map_y-self.maze.center[0])
		pix_start_x = self.maze.center_chunk.CHUNKLEN * TILE_LEN * (map_y-self.maze.center[1])

		self.rendered_room_stuff.append(set())
		tile_set = self.rendered_room_stuff[-1]

		for i in range(chunk.CHUNKLEN):
			for j in range(chunk.CHUNKLEN):
				if chunk.grid[i][j].wall == True:
					tile = scene.layers[0].add_rect(
					width=TILE_LEN,
					height=TILE_LEN,
					pos=(pix_start_x + (TILE_LEN*j), pix_start_y + (TILE_LEN*i)),
					color=(1, 1, 1),  # White
					)
					tile_set.add(tile)
	

	def find_current_tile(self):
		print(self.sprite.x / 50)
		print(self.sprite.y / 50)
		tile_x = int(round(self.sprite.x / 50))
		tile_y = int(round(self.sprite.y / 50))
	
		print(f"called | {self.sprite.x} -> {tile_x} | {self.sprite.y} -> {tile_y} |")
		
		return [tile_x, tile_y]


	
	# Define movement functions
	def move_up(self):

		if self.sprite.y % TILE_LEN == 0:
			tile_coords:list[int] = self.find_current_tile()
			chunk:Chunk = self.maze.map[self.map_position[0]][self.map_position[1]]
			chunk.print_chunk()
			if chunk.grid[tile_coords[1]-1][tile_coords[0]].wall:
				return

		# Add trail at current position before moving
		trail = scene.layers[-2].add_rect(
			width=10,
			height=10,
			pos=(self.sprite.x, self.sprite.y),
			color=(1, 0, 0, 0.3),  # Red with transparency
		)
		
		new_y = self.sprite.y - 10
		if not self.check_collision(self.sprite.x, new_y):
			self.sprite.y = new_y
			self.direction = 90

		scene.camera.pos = player.sprite.pos
		self.last_ver_move_up = True

	def move_down(self):

		if self.sprite.y % TILE_LEN == 0:
			tile_coords:list[int] = self.find_current_tile()
			chunk:Chunk = self.maze.map[self.map_position[0]][self.map_position[1]]
			chunk.print_chunk()
			if chunk.grid[tile_coords[1]+1][tile_coords[0]].wall:
				return

		# Add trail at current position before moving
		trail = scene.layers[-2].add_rect(
			width=10,
			height=10,
			pos=(self.sprite.x, self.sprite.y),
			color=(1, 0, 0, 0.3),  # Red with transparency
		)
		
		new_y = self.sprite.y + 10
		if not self.check_collision(self.sprite.x, new_y):
			self.sprite.y = new_y
			self.direction = 270
		

		scene.camera.pos = player.sprite.pos
		self.last_ver_move_up = False

	def move_left(self):

		if self.sprite.x % TILE_LEN == 0:
			tile_coords:list[int] = self.find_current_tile()
			chunk:Chunk = self.maze.map[self.map_position[0]][self.map_position[1]]
			chunk.print_chunk()
			if chunk.grid[tile_coords[1]][tile_coords[0]-1].wall:
				return
			
		# Add trail at current position before moving
		trail = scene.layers[-2].add_rect(
			width=10,
			height=10,
			pos=(self.sprite.x, self.sprite.y),
			color=(1, 0, 0, 0.3),  # Red with transparency
		)
		
		new_x = self.sprite.x - 10
		if not self.check_collision(new_x, self.sprite.y):
			self.sprite.x = new_x
			self.direction = 180

		scene.camera.pos = player.sprite.pos
		self.last_hor_move_right = False

	def move_right(self):

		if self.sprite.x % TILE_LEN == 0:
			tile_coords:list[int] = self.find_current_tile()
			chunk:Chunk = self.maze.map[self.map_position[0]][self.map_position[1]]
			chunk.print_chunk()
			if chunk.grid[tile_coords[1]][tile_coords[0]+1].wall:
				return
			
		# Add trail at current position before moving
		trail = scene.layers[-2].add_rect(
			width=10,
			height=10,
			pos=(self.sprite.x, self.sprite.y),
			color=(1, 0, 0, 0.3),  # Red with transparency
		)
		
		new_x = self.sprite.x + 10
		if not self.check_collision(new_x, self.sprite.y):
			self.sprite.x = new_x
			self.direction = 0
		

		scene.camera.pos = player.sprite.pos
		self.last_hor_move_right = True



	# Remove the sword after the attack
	def attack(self):
		self.Sword = scene.layers[-1].add_sprite( # should probably re-write in terms of TILE_LEN
		scale = 1.5,
		pos=(400, 300),
		image="sword.png",  # Set the rotation based on the player's direction
		# Black color for the sword
		)

		def on_animation_finished():
			self.Sword.delete()
			self.attacking = 0
			# Reset movement flags to stop continuous movement after attack
			self.up_pressed = False
			self.down_pressed = False
			self.left_pressed = False
			self.right_pressed = False
		
		self.attacking = 1

		# Determine the tile in front of the player based on direction
		tile_coords = self.find_current_tile()
		chunk = self.maze.map[self.map_position[0]][self.map_position[1]]

		print(f"Attack: tile_coords={tile_coords}, direction={self.direction}")

		front_wall = False
		if self.direction == 180:  # facing left
			print(f"Checking left tile wall: {chunk.grid[tile_coords[1]][tile_coords[0]+1].wall}")
			if chunk.grid[tile_coords[1]][tile_coords[0]+1].wall:
				front_wall = True
		elif self.direction == 90:  # facing up
			print(f"Checking up tile wall: {chunk.grid[tile_coords[1]-1][tile_coords[0]].wall}")
			if chunk.grid[tile_coords[1]-1][tile_coords[0]].wall:
				front_wall = True
		elif self.direction == 0:  # facing right
			print(f"Checking right tile wall: {chunk.grid[tile_coords[1]][tile_coords[0]-1].wall}")
			if chunk.grid[tile_coords[1]][tile_coords[0]-1].wall:
				front_wall = True
		elif self.direction == 270:  # facing down
			print(f"Checking down tile wall: {chunk.grid[tile_coords[1]+1][tile_coords[0]].wall}")
			if chunk.grid[tile_coords[1]+1][tile_coords[0]].wall:
				front_wall = True

		if front_wall:
			# Swing sword on opposite side
			if self.direction == 180:  # facing left, swing right
				self.Sword.pos = (self.sprite.pos - (25, 0))
				animate(self.Sword, tween='linear', duration=0.2, angle=-3, on_finished=on_animation_finished)
			elif self.direction == 90:  # facing up, swing down
				self.Sword.pos = (self.sprite.pos + (0, 25))
				animate(self.Sword, tween='linear', duration=0.2, angle=-3, on_finished=on_animation_finished)
			elif self.direction == 0:  # facing right, swing left
				self.Sword.pos = (self.sprite.pos + (25, 0))
				animate(self.Sword, tween='linear', duration=0.2, angle=3, on_finished=on_animation_finished)
			elif self.direction == 270:  # facing down, swing up
				self.Sword.pos = (self.sprite.pos - (0, 25))
				animate(self.Sword, tween='linear', duration=0.2, angle=3, on_finished=on_animation_finished)
		else:
			# Swing sword normally
			if self.direction == 180:  # Player is facing left
				self.Sword.pos = (self.sprite.pos  (25, 0))
				animate(self.Sword, tween='linear', duration=0.2, angle=-3, on_finished=on_animation_finished)
				
			elif self.direction == 90:  # Player is facing up
				self.Sword.pos = (self.sprite.pos - (0, 25))
				animate(self.Sword, tween='linear', duration=0.2, angle=3, on_finished=on_animation_finished)
				
			elif self.direction == 0:  # Player is facing right
				self.Sword.pos = (self.sprite.pos - (25, 0))
				animate(self.Sword, tween='linear', duration=0.2, angle=3, on_finished=on_animation_finished) 
				
			elif self.direction == 270:  # Player is facing down
				self.Sword.pos = (self.sprite.pos + (0, 25))
				animate(self.Sword, tween='linear', duration=0.2, angle=-3, on_finished=on_animation_finished)

	def check_collision(self, new_x, new_y):
		"""
		Checks whether the player's next move will result in a collision with a wall.

		Args:
			new_x (int): The new x-coordinate of the player.
			new_y (int): The new y-coordinate of the player.

		Returns:
			bool: True if there is a collision, False otherwise.
		"""
		# Calculate the tile coordinates of the player's next move
		tile_x = int((new_x + TILE_LEN/ 2) // TILE_LEN)
		tile_y = int((new_y + TILE_LEN/ 2) // TILE_LEN)
		
		# Get the chunk that the player is currently in
		chunk = self.maze.map[self.map_position[0]][self.map_position[1]]
		
		# Get the cell that the player is trying to move into
		cell = chunk.grid[tile_y][tile_x]
		
		# Check if the cell is a wall
		if cell.wall:
			return True
		else:
			return False

class Orb:
	def __init__(self, pos, direction, orb_type="blast"):
		self.direction = direction
		self.speed = 15
		self.orb_type = orb_type
		self.sprite = scene.layers[-1].add_circle(
			radius=10,
			pos=pos,
			color=(1, 0.5, 0, 1) if orb_type == "explosion" else (0.5, 0, 0.5, 1),  # Orange for explosion, purple otherwise
		)
		self.alive = True
		self.opacity = 1.0
		self.exploding = False

	def update(self):
		if not self.alive:
			return

		# Calculate new position based on direction
		if self.direction == 0:  # right
			new_x = self.sprite.x + self.speed
			new_y = self.sprite.y
		elif self.direction == 90:  # up
			new_x = self.sprite.x
			new_y = self.sprite.y - self.speed
		elif self.direction == 180:  # left
			new_x = self.sprite.x - self.speed
			new_y = self.sprite.y
		elif self.direction == 270:  # down
			new_x = self.sprite.x
			new_y = self.sprite.y + self.speed
		else:
			new_x = self.sprite.x
			new_y = self.sprite.y

		# Check collision with walls
		tile_x = int((new_x + TILE_LEN / 2) // TILE_LEN)
		tile_y = int((new_y + TILE_LEN / 2) // TILE_LEN)
		chunk = player.maze.map[player.map_position[0]][player.map_position[1]]

		if chunk.grid[tile_y][tile_x].wall:
			if self.orb_type == "blast":
				# Start fading out
				self.alive = False
				animate(self.sprite, tween='linear', duration=0.3, color=(0.5, 0, 0.5, 0), on_finished=self.delete)
			elif self.orb_type == "explosion" and not self.exploding:
				self.exploding = True
				self.speed = 0
				animate(self.sprite, tween='linear', duration=1, radius=100, color=(0.5, 0, 0.5, 0), on_finished=self.delete)
		else:
			self.sprite.x = new_x
			self.sprite.y = new_y

	def delete(self):
		self.sprite.delete()
		self.alive = False


player = Player()
player.orbs = []

def orb_update():
	offset_x = 0
	offset_y = 0
	if player.direction == 0:  # right
		offset_x = TILE_LEN // 2
	elif player.direction == 90:  # up
		offset_y = -TILE_LEN // 2
	elif player.direction == 180:  # left
		offset_x = -TILE_LEN // 2
	elif player.direction == 270:  # down
		offset_y = TILE_LEN // 2

	# Calculate the starting position of the orb based on player position and direction
	start_pos = (player.sprite.x + offset_x, player.sprite.y + offset_y)
	orb_type = player.orb_types[player.current_orb_type_index]
	new_orb = Orb(start_pos, player.direction, orb_type)
	player.orbs.append(new_orb)


# Bind movement functions to arrow keys
@w2d.event
def on_key_down(key):
	if player.attacking == 1:
		pass
	elif player.attacking == 0:
		if key == w2d.keys.W or key == w2d.keys.UP:
			player.up_pressed = True
		elif key == w2d.keys.S or key == w2d.keys.DOWN:
			player.down_pressed = True
		elif key == w2d.keys.A or key == w2d.keys.LEFT:
			player.left_pressed = True
		elif key == w2d.keys.D or key == w2d.keys.RIGHT:
			player.right_pressed = True
		elif key == w2d.keys.SPACE:
			player.attack()
		elif key == w2d.keys.X:
			import time
			current_time = time.time()
			cooldown = 0.3
			if player.orb_types[player.current_orb_type_index] == "explosion":
				cooldown = 1.0
			if current_time - player.last_orb_shot_time >= cooldown:
				orb_update()
				player.last_orb_shot_time = current_time
		elif key == w2d.keys.E:
			player.current_orb_type_index = (player.current_orb_type_index + 1) % len(player.orb_types)
			print(f"Switched to orb type: {player.orb_types[player.current_orb_type_index]}")



@w2d.event
def on_key_up(key):
	if player.attacking == 1:
		pass

	elif player.attacking == 0:
		if key == w2d.keys.W or key == w2d.keys.UP:
			player.up_pressed = False
		elif key == w2d.keys.S or key == w2d.keys.DOWN:
			player.down_pressed = False
		elif key == w2d.keys.A or key == w2d.keys.LEFT:
			player.left_pressed = False
		elif key == w2d.keys.D or key == w2d.keys.RIGHT:
			player.right_pressed = False

		

		if player.sprite.x % TILE_LEN != 0:
			for _ in range(4):
				scene.camera.pos = player.sprite.pos
				if player.last_hor_move_right == True:
					player.move_right()
					#time.sleep(1/60)
				else:
					player.move_left()
					#time.sleep(1/60)

				if player.sprite.x % TILE_LEN == 0:
					break
				scene.camera.pos = player.sprite.pos
		
		if player.sprite.y % TILE_LEN != 0:
			for _ in range(4):
				scene.camera.pos = player.sprite.pos
				if player.last_ver_move_up == True:
					player.move_up()
					#time.sleep(1/60)
				else:
					player.move_down()
					#time.sleep(1/60)

				if player.sprite.y % TILE_LEN == 0:
					break
				scene.camera.pos = player.sprite.pos


	

	else:
		print(player.attacking)
	

def update():
	scene.camera.pos = player.sprite.pos
	if player.attacking == 1:
		pass
	elif player.attacking == 0:
		if player.up_pressed:
			player.move_up()
		elif player.down_pressed:
			player.move_down()
		elif player.left_pressed:
			player.move_left()
		elif player.right_pressed:
			player.move_right()

		# Update orbs and remove dead ones
		for orb in player.orbs[:]:
			orb.update()
			if not orb.alive:
				player.orbs.remove(orb)
	else:
		pass
	w2d.clock.schedule(update, 1/60)



# Run the scene

update()
player.render_chunk(15,15)
w2d.run()
