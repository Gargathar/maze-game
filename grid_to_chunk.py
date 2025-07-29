import sys
sys.dont_write_bytecode = True
from chunk_generation import Cell, Chunk

def convert(level:list[list[str]]) -> Chunk:
    chunk = Chunk()
    size = len(level)
    chunk.grid = []
    for i in range(size):
        chunk.grid.append([])
        for j in range(size):
            cur = Cell(i,j)
            chunk.grid[i].append(cur)
            if level[i][j] == '..':
                cur.wall = False
    return chunk

if __name__ == '__main__':
    ch = convert([['..','##'],['##','..']])
    ch.print_chunk()