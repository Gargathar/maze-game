
import sys
sys.dont_write_bytecode = True
# This is a holy warding spell, one that is required for my computer for some stupid reason
# Please place it at the top of each new file, such that I may remain protected


from random import shuffle, randint

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


class Chunk:

	def __init__(self, wall_to_use:str=None, brick:bool=False, story:str=None):

		self.CHUNKLEN:int = 31 # this assumes the grid is a uniform square
		mid:int = self.CHUNKLEN//2

		self.dir:list = [[1,0],[-1,0],[0,1],[0,-1]]
		self.grid:list = []

		self.special_story_stuff:str = story

		self.wall_to_use:str = wall_to_use

		for i in range(self.CHUNKLEN):
			self.grid.append([])
			for j in range(self.CHUNKLEN):
				
				temp_cell = Cell(i,j)
				self.grid[i].append(temp_cell)

				if i == 0 and j == mid:
					temp_cell.bound = "north"
				
				elif i == mid and j == 0:
					temp_cell.bound = "west"
				
				elif i == self.CHUNKLEN-1 and j == mid:
					temp_cell.bound = "south"
				
				elif i == mid and j == self.CHUNKLEN-1:
					temp_cell.bound = "east"

	

		def dfs(i:int, j:int, vis:list[list[bool]]): # helps buils the maze
			shuffle(self.dir)
			vis[i][j] = True
			self.grid[2*i+1][2*j+1].wall = False
			
			mid = self.CHUNKLEN//2
			for d in self.dir:
				newI, newJ = i + d[0], j + d[1]
				if newI>=0 and newI < mid and newJ>=0 and newJ < mid and not vis[newI][newJ]:
					self.grid[2*i+1 + d[0]][2*j+1 + d[1]].wall = False
					dfs(newI, newJ, vis)

		def build_maze(): # involved in dfs building
			mid = self.CHUNKLEN//2
			vis = [[False for _ in range(mid)] for _ in range(mid)]
			dfs(randint(0, mid-1), randint(0, mid-1), vis)
		if brick == False: # just in case
			build_maze()

		self.grid[0][mid].wall = False
		self.grid[mid][0].wall = False
		self.grid[self.CHUNKLEN-1][mid].wall = False
		self.grid[mid][self.CHUNKLEN-1].wall = False





	def print_chunk(self):
		for row in self.grid:
			for cell in row:
				print(cell, end="")
			print()



if __name__ == "__main__":
	g = Chunk()

	g.print_chunk()
