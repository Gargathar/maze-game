
import sys
sys.dont_write_bytecode = True
# This is a holy warding spell, one that is required for my computer for some stupid reason
# Please place it at the top of each new file, such that I may remain protected


from chunk_generation import Cell, Chunk
import wasabi2d as w2d


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

		self.center_chunk = Chunk()

		self.map[self.MAP_LEN//2][self.MAP_LEN//2] = self.center_chunk



	def get_chunk(self, y, x):
		
		if self.map[y][x] == "UNEXPLORED":
			self.map[y][x] = Chunk()
		return self.map[y][x]

		
