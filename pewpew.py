
import wasabi2d as w2d 
TILE_LEN = 50

class Orb:
	def __init__(self, player, orb_type):
		from Player import Player
		from Player import scene
		
		self.player = player
		self.type = orb_type
		self.color = orb_type['color']
		self.expand_on_impact = orb_type['expand_on_impact']
		self.speed = 10
		self.to_delete = False
		self.fading = False
		self.fade_alpha = 1.0
		self.exploding = False
		self.explosion_radius = 0
		self.max_explosion_radius = 50

		# Start position at player center (absolute center of player sprite)
		self.x = player.sprite.x + player.sprite.width / 2
		self.y = player.sprite.y + player.sprite.height / 2

		# Direction vector based on player direction
		if player.direction == 0:  # right
			self.dx = 1
			self.dy = 0
		elif player.direction == 90:  # up
			self.dx = 0
			self.dy = -1
		elif player.direction == 180:  # left
			self.dx = -1
			self.dy = 0
		elif player.direction == 270:  # down
			self.dx = 0
			self.dy = 1
		else:
			self.dx = 0
			self.dy = 0

		# Adjust orb start position based on direction to spawn from correct side of player
		if player.direction == 0:  # right
			self.x = player.sprite.x + player.sprite.width
			self.y = player.sprite.y + player.sprite.height / 2
		elif player.direction == 90:  # up
			self.x = player.sprite.x + player.sprite.width / 2
			self.y = player.sprite.y
		elif player.direction == 180:  # left
			self.x = player.sprite.x
			self.y = player.sprite.y + player.sprite.height / 2
		elif player.direction == 270:  # down
			self.x = player.sprite.x + player.sprite.width / 2
			self.y = player.sprite.y + player.sprite.height

		# Create orb sprite
		self.sprite = scene.layers[2].add_circle(
			radius=10,
			pos=(self.x, self.y),
			color=self.color,
		)

	def update(self):
		if self.to_delete:
			return

		if self.fading:
			self.fade_alpha -= 0.05
			if self.fade_alpha <= 0:
				self.sprite.delete()
				self.to_delete = True
			else:
				self.sprite.color = (self.color[0], self.color[1], self.color[2], self.fade_alpha)
			return

		if self.exploding:
			self.explosion_radius += 5
			self.sprite.radius = 10 + self.explosion_radius
			if self.explosion_radius >= self.max_explosion_radius:
				self.sprite.delete()
				self.to_delete = True
			return

		# Move orb
		# Debug: print current position and direction
		#print(f"Orb pos before move: ({self.x}, {self.y}), direction: ({self.dx}, {self.dy})")
		self.x += self.dx * self.speed
		self.y += self.dy * self.speed
		self.sprite.pos = (self.x, self.y)

		# Check collision with walls
		tile_x = int(self.x // TILE_LEN)
		tile_y = int(self.y // TILE_LEN)

		chunk_y = self.player.map_position[0]
		chunk_x = self.player.map_position[1]
		chunk = self.player.maze.get_chunk(chunk_y, chunk_x)

		# Check bounds
		if tile_y < 0 or tile_y >= chunk.CHUNKLEN or tile_x < 0 or tile_x >= chunk.CHUNKLEN:
			self.handle_collision()
			return

		cell = chunk.grid[tile_y][tile_x]
		if cell.wall:
			self.handle_collision()

	def handle_collision(self):
		if self.expand_on_impact:
			self.exploding = True
		else:
			self.fading = True
