
from chunk_generation import Cell, Chunk
import wasabi2d as w2d

class Maze:

	def __init__(self, TILE_LEN):

		self.TILE_LEN:int = TILE_LEN

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
