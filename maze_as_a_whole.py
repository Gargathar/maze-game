
from game_proof_of_concept import Cell, Chunk


class Maze:

	def __init__(self):

		MAP_LEN = 31

		self.map = []

		for _ in range(MAP_LEN):
			row = []
			self.map.append(row)
			for _ in range(MAP_LEN):
				row.append("UNEXPLORED")

		self.map[MAP_LEN//2,MAP_LEN//2] = Chunk()


		self.player_position = [MAP_LEN//2,MAP_LEN//2] #! the player class (may it be soon created) should store this
