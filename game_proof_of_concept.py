
from math import floor

class Cell:

	def __init__(self, y:int, x:int):
		self.y:int = y
		self.x:int = x
		self.wall:bool = True
		self.bound = None
	
	def __repr__(self):
		# if cell.bound != None:
		# 	return cell.bound
		if self.wall == True:
			return "##"
		else:
			return ".."


class Grid:

	def __init__(self):

		self.GRIDLEN = 10 # this assumes the grid is a uniform square

		self.grid = []

		for i in range(11):
			self.grid.append([])
			for j in range(11):
				
				temp_cell = Cell(i,j)
				self.grid[i].append(temp_cell)

				if i == 0 and j == floor(self.GRIDLEN/2):
					temp_cell.bound = "north"
				
				elif i == floor(self.GRIDLEN/2) and j == 0:
					temp_cell.bound = "west"
				
				elif i == self.GRIDLEN and j == floor(self.GRIDLEN/2):
					temp_cell.bound = "south"
				
				elif i == floor(self.GRIDLEN/2) and j == self.GRIDLEN:
					temp_cell.bound = "east"
						



		for row in self.grid:
			for cell in row:
				print(cell, end="")
			print()


if __name__ == "__main__":
	g = Grid()