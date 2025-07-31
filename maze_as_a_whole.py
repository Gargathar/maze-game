
import sys
sys.dont_write_bytecode = True
# This is a holy warding spell, one that is required for my computer for some stupid reason
# Please place it at the top of each new file, such that I may remain protected


from chunk_generation import Cell, Chunk
import wasabi2d as w2d

from grid_to_chunk import convert
import structures as maps


class Maze:

	def __init__(self):


		self.MAP_LEN:int = 31

		self.map:list = []

		for _ in range(self.MAP_LEN):
			row = []
			self.map.append(row)
			for _ in range(self.MAP_LEN):
				row.append("UNEXPLORED")
		
		self.center = [self.MAP_LEN//2,self.MAP_LEN//2]

		self.center_chunk = convert(maps.concentric,"pixil-frame-0-11.png", "center")

		self.map[self.MAP_LEN//2][self.MAP_LEN//2] = self.center_chunk

		self.map[self.MAP_LEN//2][self.center[1]-8] = convert(maps.pillars, "pixil-frame-0-12.png", "left")
		self.map[self.MAP_LEN//2][self.center[1]+9] = convert(maps.technicalluy_this_is_a_real_labyrinth, "pixil-frame-0-12.png","right")
		self.map[self.center[0]-8][self.MAP_LEN//2] = convert(maps.comb, "pixil-frame-0-12.png", "up")
		self.map[self.center[0]+11][self.MAP_LEN//2] = convert(maps.the_big_empty, "pixil-frame-0-12.png","down")

		self.map[0][0] = convert(maps.ow_my_liver, "pixil-frame-0-10.png")



	def get_chunk(self, y, x):
		
		if self.map[y][x] == "UNEXPLORED":
			self.map[y][x] = Chunk()
		return self.map[y][x]

		
