import sys
sys.dont_write_bytecode = True

import wasabi2d as w2d
from Player import player, scene
from math import fabs
import time
from pewpew import Orb

TILE_LEN=50

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
class Enemy():
	def __init__(self, pos, player, scene):
		self.dx, self.dy=-1,-1
		self.player = player
		self.sprite = scene.layers[1].add_circle(radius=10, pos=pos, color='yellow')
v=1
a_timer = Timer(3)
enemy = Enemy((150,150), player, scene)
sprite = enemy.sprite
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
	x, y = sprite.x, sprite.y
	dx, dy = enemy.dx, enemy.dy
	cell_x, cell_y, new_cell_x, new_cell_y = int((x + 25) // 50), int((y + 25) // 50), int((x + dx + 25) // 50), int((y + dy + 25) // 50)
	chunk = player.maze.map[player.map_position[0]][player.map_position[1]]
	if chunk.grid[new_cell_y%31][new_cell_x%31].wall:
		enemy.dx, enemy.dy = v * (player.sprite.x - sprite.x) * dt, v * (player.sprite.y - sprite.y) * dt
		if cell_x == new_cell_x:
			# dx=0
			dy*=-1
		else:
			# dy=0
			dx*=-1
	sprite.x += dx
	sprite.y += dy
	print(player.health)
	if fabs(player.sprite.x - sprite.x) < 25 and fabs(player.sprite.y - sprite.y) < 25 and a_timer.elapsed():
		player.health-=2
	# w2d.clock.schedule(update, 1/60)

# Run the scene

player.render_chunk(15,15)
w2d.run()