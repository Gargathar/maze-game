import sys
sys.dont_write_bytecode = True
# This is a holy warding spell, one that is required for my computer for some stupid reason
# Please place it at the top of each new file, such that I may remain protected


import wasabi2d as w2d
import time
import math

#          ][
#     - - -/\- - -
#][ /-_ _ /  \ _ _-\ ][
import threading 
#  |    /_/  \_\    |
#   \  //      \\  /
#  ][ - - -  - - - ][  

from music import MusicPlayer
from pewpew import Orb
from chunk_generation import Chunk, Cell
from maze_as_a_whole import Maze

# Create a new scene
scene = w2d.Scene(width=800, height=600, background=(0, 0, 0), title="My Scene")
animate = w2d.animate 
TILE_LEN = 50


# Debug constants, FOR RELEASE SHOULD ALL BE FALSE
DEBUG_NOCLIP = True


music_player = MusicPlayer()
# music_player.start()

class Player:
	
	def __init__(self):
		self.maze = Maze()
		self.health=10
		self.lives=5
		self.map_position = [self.maze.MAP_LEN//2, self.maze.MAP_LEN//2] # [Y, X], NOT THE OTHER WAY AROUND!!!!!

		self.CHUNKLEN = self.maze.center_chunk.CHUNKLEN

		self.rendered_room_stuff:dict[set[Cell]] = {}
		
		# Create a new square sprite for the Player
		self.sprite = scene.layers[1].add_rect(
			width=TILE_LEN * 5/6,
			height=TILE_LEN * 5/6,
			pos=(TILE_LEN * (self.CHUNKLEN//2), TILE_LEN * (self.CHUNKLEN//2)),
			color=(1,0,0),  # Red color
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

		# Orb feature attributes
		self.orb_types = [
			{
				'name': 'purple',
				'color': (0.5, 0, 0.5),
				'cooldown': 0.5,
				'expand_on_impact': False,
			},
			{
				'name': 'orange',
				'color': (1, 0.5, 0),
				'cooldown': 1.0,
				'expand_on_impact': True,
			}
		]
		self.current_orb_index = 0
		self.last_orb_time = 0
		self.active_orbs = []

		
		# game progression flags
		self.up_flag:bool = False
		self.down_flag:bool = False
		self.left_flag:bool = False
		self.right_flag:bool = False
		self.end_flag:bool = False

		 # a list of small sprites to show progress in the gui
		self.progress_squares = []
		# scene.layers[5].add_rect(
		# 	width=TILE_LEN * 2/3,
		# 	height=TILE_LEN * 2/3,
		# 	pos=(scene.camera.pos[0]-275, scene.camera.pos[1]-575),
		# 	color=(1,0.5,0),  # orange color
		# ),

		
		self.out_of_map_chunks = [
			[None,None,None,],
			[None,None,None,],
			[None,None,None,],
		]
		self.out_of_map_set:set[tuple[int]] = set()

		self.health = 10

	
	def progression(self, chunk:Chunk):
		if chunk.special_story_stuff != None:
			match chunk.special_story_stuff:
				case "up":
					if self.up_flag != True:
						self.up_flag = True
						self.progress_squares.append(
							scene.layers[5].add_rect(
							width=TILE_LEN * 2/3,
							height=TILE_LEN * 2/3,
							pos=(scene.camera.pos[0]-275, scene.camera.pos[1]-575),
							color=(1,0.5,0),  # orange color
						),
						)
				case "down":
					if self.down_flag != True:
						self.down_flag = True
						self.progress_squares.append(
							scene.layers[5].add_rect(
							width=TILE_LEN * 2/3,
							height=TILE_LEN * 2/3,
							pos=(scene.camera.pos[0]-275, scene.camera.pos[1]-575),
							color=(1,0.5,0),  # orange color
						),
						)
				case "left":
					if self.left_flag != True:
						self.left_flag = True
						self.progress_squares.append(
							scene.layers[5].add_rect(
							width=TILE_LEN * 2/3,
							height=TILE_LEN * 2/3,
							pos=(scene.camera.pos[0]-275, scene.camera.pos[1]-575),
							color=(1,0.5,0),  # orange color
						),
						)
				case "right":
					if self.right_flag != True:
						self.right_flag = True
						self.progress_squares.append(
							scene.layers[5].add_rect(
							width=TILE_LEN * 2/3,
							height=TILE_LEN * 2/3,
							pos=(scene.camera.pos[0]-275, scene.camera.pos[1]-575),
							color=(1,0.5,0),  # orange color
						),
						)
				case "center":
					if self.up_flag and self.down_flag and self.left_flag and self.right_flag:
						self.progress_squares.append(
							scene.layers[5].add_rect(
							width=TILE_LEN * 2/3,
							height=TILE_LEN * 2/3,
							pos=(scene.camera.pos[0]-275, scene.camera.pos[1]-575),
							color=(0.1,1,0.1),  # green color
						),
						)
						self.end_flag = True
	




	def render_chunk(self, map_y, map_x, chunk:Chunk=None): 
		"""
		Here so that there's only one scene to render, despite multiple layers
		
		Single hunk rendering starts at (0,0), then builds right and down
		multi-chunk rendering starts some offset (seen below), then does the same
		"""
		if tuple([map_y, map_x]) in self.rendered_room_stuff:
			if tuple([map_y, map_x]) not in self.out_of_map_set:
				return
		
		if chunk == None:	
			chunk:Chunk = self.maze.get_chunk(map_y,map_x)
		
		pix_start_y = self.maze.center_chunk.CHUNKLEN * TILE_LEN * (map_y - self.maze.center[0])
		pix_start_x = self.maze.center_chunk.CHUNKLEN * TILE_LEN * (map_x - self.maze.center[1])
		

		if (tuple([map_y,map_x]) in self.rendered_room_stuff) and (tuple([map_y,map_x]) in self.out_of_map_set):
			to_del = self.rendered_room_stuff[tuple([map_y,map_x])]
			for tile in to_del:
				tile.delete()
			del self.rendered_room_stuff[tuple([map_y,map_x]) ]
		

		self.rendered_room_stuff[tuple([map_y,map_x])] = set()
		tile_set = self.rendered_room_stuff[tuple([map_y,map_x])]

		for i in range(chunk.CHUNKLEN):
			for j in range(chunk.CHUNKLEN):
				if chunk.grid[i][j].wall == True:
					# tile = scene.layers[0].add_rect(
					# width=TILE_LEN,
					# height=TILE_LEN,
					# pos=(pix_start_x + (TILE_LEN*j), pix_start_y + (TILE_LEN*i)),
					# color=(1, 1, 1),  # White
					# )
					if chunk.wall_to_use == None:	
						tile = scene.layers[0].add_sprite(
							scale = 1,
							pos = (pix_start_x + (TILE_LEN*j), pix_start_y + (TILE_LEN*i)),
							image = "pixil-frame-0-8.png", #if_this_doesnt_work_i_swear_to_god.png
						)
					else:
						tile = scene.layers[0].add_sprite(
						scale = 1,
						pos = (pix_start_x + (TILE_LEN*j), pix_start_y + (TILE_LEN*i)),
						image = chunk.wall_to_use, #if_this_doesnt_work_i_swear_to_god.png
					)
				else:
					tile = scene.layers[0].add_sprite(
						scale = 1,
						pos = (pix_start_x + (TILE_LEN*j), pix_start_y + (TILE_LEN*i)),
						image = "pixil-frame-0-9.png", #if_this_doesnt_work_i_swear_to_god.png
					)
				tile_set.add(tile)
	
	
	
	

	


	def render_manager(self):
		pos_set:set = set([]) # this is for chunk de-rendering

		def bob_the_builder(y_mod,x_mod):
			"""
			*Can we fix it?*

			**YES WE CAN**
			"""
			y = self.map_position[0] + y_mod
			x = self.map_position[1] + x_mod
			if (y in range(self.maze.MAP_LEN)) and (x in range(self.maze.MAP_LEN)):
				self.render_chunk(y,x)
				if y_mod == 0 and x_mod == 0:
					self.progression(self.maze.map[y][x])
			else:
				chunk:Chunk = Chunk("pixil-frame-0-13.png")
				self.out_of_map_set.add(tuple([y,x]))
				self.render_chunk(y,x,chunk)
				self.out_of_map_chunks[1 - y_mod][1 - x_mod] = chunk
			pos_set.add(tuple([y, x]))
		
		# all nine rendering chunks, based on offset from the player
		for i in range(-1,2):
			for j in range(-1,2):
				bob_the_builder(i, j)

		will_del = set()
		for key in self.rendered_room_stuff.keys():
			if key not in pos_set:
				to_del = self.rendered_room_stuff[key]
				for tile in to_del:
					tile.delete()
				will_del.add(key)
		
		for key in will_del:
			del self.rendered_room_stuff[key]
		
				


	def find_current_tile(self):
		tile_x = int(round(self.sprite.x / 50))
		tile_y = int(round(self.sprite.y / 50))
		
		return [tile_y, tile_x]
	

	def am_i_in_a_wall(self):

		if player.sprite.x % TILE_LEN != 0:
			pos = self.find_current_tile()
			if self.maze.map[self.map_position[0]][self.map_position[1]].grid[pos[0] % self.CHUNKLEN][pos[1] % self.CHUNKLEN].wall:
				player.update_gui()
				if player.last_hor_move_right == True:
					player.sprite.x -= 50
					#time.sleep(1/60)
				else:
					player.sprite.y -= 50
					#time.sleep(1/60)

				player.update_gui()

		
		
				
				


	def update_map_position(self, y, x):
		self.map_position[0] += y
		self.map_position[1] += x

		self.render_manager()

	
	def move_up(self):
		if self.sprite.y % TILE_LEN == 0:
			tile_coords:list[int] = self.find_current_tile()
			tile_coords[0] -= 1
			current_chunk_y_start = ((self.map_position[0]-(self.CHUNKLEN//2)) * self.CHUNKLEN)

			if tile_coords[0] < current_chunk_y_start:
				self.update_map_position(-1, 0)

				
			if self.map_position[0] in range(self.maze.MAP_LEN):
				chunk:Chunk = self.maze.map[self.map_position[0]][self.map_position[1]]
			else:
				chunk = self.out_of_map_chunks[1][1]

			if DEBUG_NOCLIP == False:
				if chunk.grid[tile_coords[0] % self.CHUNKLEN][tile_coords[1] % self.CHUNKLEN].wall:
					return # DEBUG

		# Add trail at current position before moving
		# trail = scene.layers[0].add_rect(
		# 	width=10,
		# 	height=10,
		# 	pos=(self.sprite.x, self.sprite.y),
		# 	color=(1, 0, 0, 0.3),  # Red with transparency
		# )
		
		new_y = self.sprite.y - 10
		if not self.check_collision(self.sprite.x, new_y):
			player.attacking = 1
			self.sprite.y = new_y
			self.direction = 90
			player.attacking = 0

		player.update_gui()
		self.last_ver_move_up = True





	def move_down(self):

		if self.sprite.y % TILE_LEN == 0:
			tile_coords:list[int] = self.find_current_tile()
			tile_coords[0] += 1
			current_chunk_y_end = ((self.map_position[0]-(self.CHUNKLEN//2)) * self.CHUNKLEN) + self.CHUNKLEN

			if tile_coords[0] > current_chunk_y_end: # might need to change to a >=, but this works so it's fine
				self.update_map_position(1, 0)


			if self.map_position[0] in range(self.maze.MAP_LEN):
				chunk:Chunk = self.maze.map[self.map_position[0]][self.map_position[1]]
			else:
				chunk = self.out_of_map_chunks[1][1]

			if DEBUG_NOCLIP == False:
				if chunk.grid[tile_coords[0] % self.CHUNKLEN][tile_coords[1] % self.CHUNKLEN].wall:
					return

		# Add trail at current position before moving
		# trail = scene.layers[0].add_rect(
		# 	width=10,
		# 	height=10,
		# 	pos=(self.sprite.x, self.sprite.y),
		# 	color=(1, 0, 0, 0.3),  # Red with transparency
		# )
		
		new_y = self.sprite.y + 10
		if not self.check_collision(self.sprite.x, new_y):
			player.attacking = 1
			self.sprite.y = new_y
			self.direction = 270
			player.attacking = 0
		

		player.update_gui()
		self.last_ver_move_up = False





	def move_left(self):

		if self.sprite.x % TILE_LEN == 0:
			tile_coords:list[int] = self.find_current_tile()
			tile_coords[1] -= 1
			current_chunk_x_start = ((self.map_position[1]-(self.CHUNKLEN//2)) * self.CHUNKLEN)

			if tile_coords[1] < current_chunk_x_start:
				self.update_map_position(0, -1)


			if self.map_position[0] in range(self.maze.MAP_LEN):
				chunk:Chunk = self.maze.map[self.map_position[0]][self.map_position[1]]
			else:
				chunk = self.out_of_map_chunks[1][1]

			if DEBUG_NOCLIP == False:
				if chunk.grid[tile_coords[0] % self.CHUNKLEN][tile_coords[1] % self.CHUNKLEN].wall:
					print("ow my liver")
					return
			
		# Add trail at current position before moving
		# trail = scene.layers[0].add_rect(
		# 	width=10,
		# 	height=10,
		# 	pos=(self.sprite.x, self.sprite.y),
		# 	color=(1, 0, 0, 0.3),  # Red with transparency
		# )
		
		new_x = self.sprite.x - 10
		if not self.check_collision(new_x, self.sprite.y):
			player.attacking = 1
			self.sprite.x = new_x
			self.direction = 180
			player.attacking = 0

		player.update_gui()
		self.last_hor_move_right = False
		




	def move_right(self):

		if self.sprite.x % TILE_LEN == 0:
			tile_coords:list[int] = self.find_current_tile()
			tile_coords[1] += 1
			current_chunk_x_end = ((self.map_position[1]-(self.CHUNKLEN//2)) * self.CHUNKLEN) + self.CHUNKLEN

			if tile_coords[1] > current_chunk_x_end:
				self.update_map_position(0, 1)


			if self.map_position[0] in range(self.maze.MAP_LEN):
				chunk:Chunk = self.maze.map[self.map_position[0]][self.map_position[1]]
			else:
				chunk = self.out_of_map_chunks[1][1]

			if DEBUG_NOCLIP == False:
				if chunk.grid[tile_coords[0] % self.CHUNKLEN][tile_coords[1] % self.CHUNKLEN].wall:
					return
			
		# Add trail at current position before moving
		# trail = scene.layers[0].add_rect(
		# 	width=10,
		# 	height=10,
		# 	pos=(self.sprite.x, self.sprite.y),
		# 	color=(1, 0, 0, 0.3),  # Red with transparency
		# )
		
		new_x = self.sprite.x + 10
		if not self.check_collision(new_x, self.sprite.y):
			player.attacking = 1
			self.sprite.x = new_x
			self.direction = 180
			player.attacking = 0
		

		player.update_gui()
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
				animate(self.Sword, tween='linear', duration=0.3, angle=3, on_finished=on_animation_finished)
			elif self.direction == 90:  # facing up, swing down
				self.Sword.pos = (self.sprite.pos + (0, 25))
				animate(self.Sword, tween='linear', duration=0.3, angle=-3, on_finished=on_animation_finished)
			elif self.direction == 0:  # facing right, swing left
				self.Sword.pos = (self.sprite.pos + (25, 0))
				animate(self.Sword, tween='linear', duration=0.3, angle=-3, on_finished=on_animation_finished)
			elif self.direction == 270:  # facing down, swing up
				self.Sword.pos = (self.sprite.pos - (0, 25))
				animate(self.Sword, tween='linear', duration=0.3, angle=3, on_finished=on_animation_finished)
		else:
			# Swing sword normally
			if self.direction == 180:  # Player is facing left
				self.Sword.pos = (self.sprite.pos + (25, 0))
				animate(self.Sword, tween='linear', duration=0.3, angle=-3, on_finished=on_animation_finished)
				
			elif self.direction == 90:  # Player is facing up
				self.Sword.pos = (self.sprite.pos - (0, 25))
				animate(self.Sword, tween='linear', duration=0.3, angle=3, on_finished=on_animation_finished)
				
			elif self.direction == 0:  # Player is facing right
				self.Sword.pos = (self.sprite.pos - (25, 0))
				animate(self.Sword, tween='linear', duration=0.3, angle=3, on_finished=on_animation_finished) 
				
			elif self.direction == 270:  # Player is facing down
				self.Sword.pos = (self.sprite.pos + (0, 25))
				animate(self.Sword, tween='linear', duration=0.3, angle=-3, on_finished=on_animation_finished)

	def check_collision(self, new_x, new_y):
		"""
		Checks whether the player's next move will result in a collision with a wall.

		Args:
			new_x (int): The new x-coordinate of the player.
			new_y (int): The new y-coordinate of the player.

		Returns:
			bool: True if there is a collision, False otherwise.
		"""
		if DEBUG_NOCLIP == True:
			return False 
		# Calculate the tile coordinates of the player's next move
		if self.map_position[0] not in range(self.maze.MAP_LEN):
			return
		if self.map_position[1] not in range(self.maze.MAP_LEN):
			return

		tile_x = int((new_x + TILE_LEN/ 2) // TILE_LEN)
		tile_y = int((new_y + TILE_LEN/ 2) // TILE_LEN)
		
		# Get the chunk that the player is currently in
		chunk = self.maze.map[self.map_position[0]][self.map_position[1]]
		
		# Get the cell that the player is trying to move into
		cell = chunk.grid[tile_y % self.CHUNKLEN][tile_x % self.CHUNKLEN]
		
		# Check if the cell is a wall
		if cell.wall:
			return True
		else:
			return False
		
	
	def update_gui(self):
		scene.camera.pos = self.sprite.pos
		for i in range(len(self.progress_squares)):
			self.progress_squares[i].pos = (scene.camera.pos[0]-375 + (i * TILE_LEN), scene.camera.pos[1]-275) # REMEMBER ME
		









player = Player()



@w2d.event
def on_key_down(key):
	if player.attacking == 1:
		pass
	elif player.attacking == 0:
		# gets rid of the wall clip but isn't fun to play with
		# if player.up_pressed == True:
		# 	return
		# if player.down_pressed == True:
		# 	return
		# if player.right_pressed == True:
		# 	return
		# if player.left_pressed == True:
		# 	return

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
		elif key == w2d.keys.X:
			current_time = time.time()
			orb_type = player.orb_types[player.current_orb_index]
			if current_time - player.last_orb_time >= orb_type['cooldown']:
				new_orb = Orb(player, orb_type)
				player.active_orbs.append(new_orb)
				player.last_orb_time = current_time
		elif key == w2d.keys.E:
			player.current_orb_index = (player.current_orb_index + 1) % len(player.orb_types)
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

		

		if player.sprite.x % TILE_LEN != 0:
			for _ in range(4):
				player.update_gui()
				if player.last_hor_move_right == True:
					player.move_right()
					#time.sleep(1/60)
				else:
					player.move_left()
					#time.sleep(1/60)

				if player.sprite.x % TILE_LEN == 0:
					break
				player.update_gui()
		
		if player.sprite.y % TILE_LEN != 0:
			for _ in range(4):
				player.update_gui()
				if player.last_ver_move_up == True:
					player.move_up()
					#time.sleep(1/60)
				else:
					player.move_down()
					#time.sleep(1/60)

				if player.sprite.y % TILE_LEN == 0:
					break
				player.update_gui()


	

	else:
		print(player.attacking)
	

def update():
	player.update_gui()

	# player.am_i_in_a_wall()

	# Update orbs
	current_time = time.time()
	for orb in player.active_orbs[:]:
		orb.update()
		if orb.to_delete:
			player.active_orbs.remove(orb)

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
	else:
		pass
	w2d.clock.schedule(update, 1/60)
	if player.lives==0:
		scene.layers[2].add_rect(width=scene.width, height = scene.height, pos=player.sprite.pos, color='red')
	# scene.layers[0].add_label(text=f'Pos: {player.sprite.pos}', pos=player.sprite.pos, align='left')



# Run the scene
if __name__ == '__main__':
	update()
	player.render_manager()
	player.lives=0
	w2d.run()
