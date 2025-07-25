
from math import floor

class Cell:

	def __init__(self, y:int, x:int):
		self.y:int = y
		self.x:int = x
		self.wall:bool = False
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

		self.GRIDLEN = 11 # this assumes the grid is a uniform square

		self.grid = []

		for i in range(self.GRIDLEN):
			self.grid.append([])
			for j in range(self.GRIDLEN):
				
				temp_cell = Cell(i,j)
				self.grid[i].append(temp_cell)

				if i == 0:
					if j == floor((self.GRIDLEN-1)/2):
						temp_cell.bound = "north"
					else:
						temp_cell.wall = True
				
				elif j == 0:
					if i == floor((self.GRIDLEN-1)/2):
						temp_cell.bound = "west"
					else:
						temp_cell.wall = True
				
				elif i == self.GRIDLEN-1: 
					if j == floor((self.GRIDLEN-1)/2):
						temp_cell.bound = "south"
					else:
						temp_cell.wall = True

				
				elif j == (self.GRIDLEN-1):
					if i == floor((self.GRIDLEN-1)/2):
						temp_cell.bound = "east"
					else:
						temp_cell.wall = True
						


	def print_grid(self):
		for row in self.grid:
			for cell in row:
				print(cell, end="")
			print()


class Player:

	def __init__(self, grid:Grid):
		self.grid:Grid = grid
		self.y:int = 0
		self.x:int = 5
	
	def display_clear(self):
		print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

	def draw(self):
		for vert_adj in range(-2,3):
			if (self.y + vert_adj) < 0:
				print("  ")
				continue
			if (self.y + vert_adj) > self.grid.GRIDLEN-1:
				print("  ")
				continue
			for hor_adj in range(-2,3):
				if (self.x + hor_adj) < 0:
					print("  ", end="")
					continue
				if (self.x + hor_adj) > self.grid.GRIDLEN-1:
					print("  ", end="")
					continue

				if hor_adj == 0 and vert_adj == 0:
					print("7∆", end="")
				else:
					print(f"{self.grid.grid[self.y + vert_adj][self.x + hor_adj].__repr__()}", end="")
			print()
	
	def move(self):
		stay_going = True
		while stay_going:
			self.display_clear()
			self.draw()
			match input("> ").lower():
				case 'w':
					option_y = self.y - 1
					option_x = self.x
				case 's':
					option_y = self.y + 1
					option_x = self.x
				case 'a':
					option_x = self.x - 1
					option_y = self.y
				case 'd':
					option_x = self.x + 1
					option_y = self.y
				case 'exit':
					stay_going = False
					break
				case _:
					continue
			try:
				if self.grid.grid[option_y][option_x].wall == True:
					continue
				else:
					if option_x >= 0 and option_y >= 0:
						self.x = option_x
						self.y = option_y
			except:
				continue
				
				
def dfs(g:Grid, i:int, j:int, vis:list[list[bool]]):
    shuffle(g.dir)
    vis[i][j] = True
    g.grid[2*i+1][2*j+1].wall = False
    
    mid = g.GRIDLEN//2
    for d in g.dir:
        newI, newJ = i + d[0], j + d[1]
        if newI>=0 and newI < mid and newJ>=0 and newJ < mid and not vis[newI][newJ]:
            g.grid[2*i+1 + d[0]][2*j+1 + d[1]].wall = False
            dfs(g, newI, newJ, vis)

def build_maze(g:Grid):
    mid = g.GRIDLEN//2
    vis = [[False for _ in range(mid)] for _ in range(mid)]
    dfs(g, 0, 0, vis)


if __name__ == "__main__":
	g = Grid()
	build_maze(g)
	g.print_grid()
	p = Player(g)
	p.move()
