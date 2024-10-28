import pygame
from random import choice

RES = WIDTH, HEIGHT = 1202, 902

TILE = 100

# Sets the tiling to be evenly spaced given the window sizing
cols, rows = WIDTH // TILE, HEIGHT // TILE

pygame.init()
window = pygame.display.set_mode(RES);
clock = pygame.time.Clock();

# Cell for the maze
class Cell: 
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = { "top": True, "right": True, "bottom": True, "left": True}
        self.visited = False
        self.solved = False

    def drawCurrentCell(self):
        x = self.x * TILE
        y = self.y * TILE

        pygame.draw.rect(window, pygame.Color('darkorange'), (x + 2, y + 2, TILE - 2, TILE -2))

    def drawCurrentCellSolve(self):
        x = self.x * TILE
        y = self.y * TILE

        pygame.draw.rect(window, pygame.Color('indigo'), (x + 10, y + 10, TILE - 20, TILE - 20))

    def draw(self):
        x = self.x * TILE
        y = self.y * TILE

        if (self.visited): 
            pygame.draw.rect(window, pygame.Color('black'), (x, y, TILE, TILE));

        # Defining the bounds of the Cell using lines
        if (self.walls['top']): 
            pygame.draw.line(window, pygame.Color('lavender'), (x, y), (x + TILE, y), 2)
        if (self.walls['right']): 
            pygame.draw.line(window, pygame.Color('lavender'), (x + TILE, y), (x + TILE, y + TILE), 2)
        if (self.walls['bottom']): 
            pygame.draw.line(window, pygame.Color('lavender'), (x + TILE, y + TILE), (x, y + TILE), 2)
        if (self.walls['left']): 
            pygame.draw.line(window, pygame.Color('lavender'), (x, y + TILE), (x, y), 2)

    def drawSolve(self):
        x = self.x * TILE
        y = self.y * TILE

        if (self.solved): 
            pygame.draw.rect(window, pygame.Color('red'), (x, y, TILE, TILE));

        # Defining the bounds of the Cell using lines
        if (self.walls['top']): 
            pygame.draw.line(window, pygame.Color('lavender'), (x, y), (x + TILE, y), 2)
        if (self.walls['right']): 
            pygame.draw.line(window, pygame.Color('lavender'), (x + TILE, y), (x + TILE, y + TILE), 2)
        if (self.walls['bottom']): 
            pygame.draw.line(window, pygame.Color('lavender'), (x + TILE, y + TILE), (x, y + TILE), 2)
        if (self.walls['left']): 
            pygame.draw.line(window, pygame.Color('lavender'), (x, y + TILE), (x, y), 2)

    def checkCellGen(self, x, y):
        # Functions to find the cell in a 1-D array: i + j * cols
        findIndex = lambda x, y: x + y * cols

        # Error-checking for going beyond the bounds of the grid
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False

        return gridCells[findIndex(x, y)]

    def checkNeighborsGen(self):
        neighbors = []
        top = self.checkCellGen(self.x, self.y - 1)
        right = self.checkCellGen(self.x + 1, self.y)
        bottom = self.checkCellGen(self.x, self.y + 1)
        left = self.checkCellGen(self.x - 1, self.y);

        # If cell neighbor exists and hasn't been visited, append to neighbors
        if (top and not top.visited):
            neighbors.append(top)
        if (right and not right.visited):
            neighbors.append(right)
        if (bottom and not bottom.visited):
            neighbors.append(bottom)
        if (left and not left.visited):
            neighbors.append(left)
    
        return choice(neighbors) if neighbors else False

    def checkNeighborsSol(self):
        neighbors = []
        top = self.checkCellGen(self.x, self.y - 1)
        right = self.checkCellGen(self.x + 1, self.y)
        bottom = self.checkCellGen(self.x, self.y + 1)
        left = self.checkCellGen(self.x - 1, self.y);

        # If neighbor exists AND not solved AND path exists to next cell from current cell, append neighbor
        if (top and not top.solved and top.walls['bottom'] != True):
            neighbors.append(top)
        if (right and not right.solved and right.walls['left'] != True):
            neighbors.append(right)
        if (bottom and not bottom.solved and bottom.walls['top'] != True):
            neighbors.append(bottom)
        if (left and not left.solved and left.walls['right'] != True):
            neighbors.append(left)

        return choice(neighbors) if neighbors else False

# Checks the wall beside the current cell and the next cell, then removes it (maze generation)
def removeWalls(current, next):
    # Difference of current and next cell shows the walls are beside each other
    dx = current.x - next.x
    dy = current.y - next.y

    if (dx == 1):
        current.walls['left'] = False
        next.walls['right'] = False
    elif (dx == -1):
        current.walls['right'] = False
        next.walls['left'] = False
    
    if (dy == 1):
        current.walls['top'] = False
        next.walls['bottom'] = False
    elif (dy == -1):
        current.walls['bottom'] = False
        next.walls['top'] = False

gridCells = [Cell(col, row) for row in range(rows) for col in range(cols)]
currentCell = gridCells[0]
stack = []
colors = []
color = 40

state = "GENERATING"

currentCell.walls['left'] = False
gridCells[len(gridCells) - 1].walls['right'] = False

# Game Loop
window.fill(pygame.Color('grey30'));
pygame.time.delay(10000)
while True:

    # Exiting the game loop
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            exit()

    # Game State: Maze Generation
    if (state == "GENERATING"):
        # Draw cells and grid
        [cell.draw() for cell in gridCells]
        currentCell.visited = True
        currentCell.drawCurrentCell()
        # [pygame.draw.rect(window, colors[i], (cell.x * TILE + 5, cell.y * TILE + 5, TILE - 10, TILE - 10), border_radius=12) for i, cell in enumerate(stack)]

        # Chooses the next cell based randomly and on availability
        # - Availability is based on whether there is a cell on top, bottom, left or right of current
        nextCell = currentCell.checkNeighborsGen()

        # Maze Generation
        if (nextCell):
            nextCell.visited = True
            stack.append(currentCell)
            # colors.append((min(color, 255), 10, 100))
            # color += 1
            removeWalls(currentCell, nextCell)
            currentCell = nextCell
        elif (stack):
            currentCell = stack.pop()

        # Framerate
        pygame.display.update();
        clock.tick(30)

        if (currentCell == gridCells[0]):
            state = "SOLVING"
            # stack = []
            # currentCell.draw()
            currentCell = gridCells[0]
            stack.append(currentCell)

            print("Maze Generation Completed. Solving...")
            pygame.time.delay(1000)

    # Game State: Solve the Maze
    elif (state == "SOLVING"):

        if (currentCell == gridCells[len(gridCells) - 1]):
            print("YOU FOUND THE PATH!!!" )
            pygame.time.delay(5000)
            exit()

        # Draw current cell
        currentCell.solved = True
        currentCell.drawCurrentCellSolve()
        # print("Current Cell: ", currentCell.x, ",", currentCell.y)
        # pygame.time.delay(200)
        # [pygame.draw.rect(window, colors[i], (cell.x * TILE + 10, cell.y * TILE + 10, TILE - 20, TILE - 20), border_radius=12) for i, cell in enumerate(stack)]

        # Chooses the next cell based randomly and on availability
        # - Availability is based on whether there is a cell on top, bottom, left or right of current
        nextCell = currentCell.checkNeighborsSol()
        # if (nextCell != False):
        #     print("Next Cell: ", nextCell.x, ",", nextCell.y)
        #     # pygame.time.delay(200)

        # Traversal
        if (nextCell):
            nextCell.solved = True
            stack.append(currentCell)
            colors.append((min(color, 255), 10, 100))
            color += 5
            currentCell = nextCell
        elif (stack):
            # Backtracking
            currentCell = stack.pop()
            currentCell.drawSolve()

        pygame.display.update();
        clock.tick(10)        