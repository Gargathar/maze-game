
from chunk_generation import Cell, Chunk


class Maze:

	def __init__(self):

		self.MAP_LEN = 31

		self.map = []

		for _ in range(self.MAP_LEN):
			row = []
			self.map.append(row)
			for _ in range(self.MAP_LEN):
				row.append("UNEXPLORED")

		self.map[self.MAP_LEN//2,self.MAP_LEN//2] = Chunk()
