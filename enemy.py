import sys
sys.dont_write_bytecode = True
import wasabi2d as w2d
from Player import player, scene
from math import fabs
import time
from pewpew import Orb

enemy = scene.layers[1].add_circle(radius=10, pos=(150,150), color='yellow')
TILE_LEN=50

# Same as in Player.py
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
				# scene.camera.pos = player.sprite.pos
				if player.last_hor_move_right == True:
					player.move_right()
					#time.sleep(1/60)
				else:
					player.move_left()
					#time.sleep(1/60)

				if player.sprite.x % TILE_LEN == 0:
					break
				# scene.camera.pos = player.sprite.pos
		
		if player.sprite.y % TILE_LEN != 0:
			for _ in range(4):
				# scene.camera.pos = player.sprite.pos
				if player.last_ver_move_up == True:
					player.move_up()
					#time.sleep(1/60)
				else:
					player.move_down()
					#time.sleep(1/60)

				if player.sprite.y % TILE_LEN == 0:
					break
				# scene.camera.pos = player.sprite.pos


	

	else:
		print(player.attacking)

class Timer:
	def __init__(self, dur):
		self.start=-dur
		self.dur = dur
	def elapsed(self):
		cur = time.time()
		if cur - self.start >= self.dur:
			self.start = cur
			return True
		return False
class Velocity():
	def __init__(self):
		self.dx=-1
		self.dy=-1
v=1
a_timer = Timer(3)
vel = Velocity()
@w2d.event
def update(dt):
	scene.camera.pos = player.sprite.pos

	# Update orbs
	for orb in player.active_orbs:
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
	# Enemy code continues
	x, y = enemy.x, enemy.y
	dx, dy = vel.dx, vel.dy
	cell_x, cell_y, new_cell_x, new_cell_y = int((x + TILE_LEN/2) // TILE_LEN), int((y + TILE_LEN/2) // TILE_LEN), int((x + dx + TILE_LEN/2) // TILE_LEN), int((y + dy + TILE_LEN/2) // TILE_LEN)
	chunk = player.maze.map[player.map_position[0]][player.map_position[1]]
	if chunk.grid[new_cell_y%31][new_cell_x%31].wall:
		vel.dx, vel.dy = v * (player.sprite.x - enemy.x) * dt, v * (player.sprite.y - enemy.y) * dt
		if cell_x == new_cell_x:
			dx=0
			dy*=-1
		else:
			dy=0
			dx*=-1
	enemy.x += dx
	enemy.y += dy
	print(player.health)
	if fabs(player.sprite.x - enemy.x) < 50 and fabs(player.sprite.y - enemy.y) < 50 and a_timer.elapsed():
		player.health-=2
	# w2d.clock.schedule(update, 1/60)

# Run the scene

player.render_chunk(15,15)
w2d.run()