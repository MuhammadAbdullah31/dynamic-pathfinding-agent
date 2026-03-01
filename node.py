import pygame

class Node:
    # 1. self, 2. row, 3. col, 4. gap, 5. total_rows
    def __init__(self, row, col, gap, total_rows):
        self.row = row
        self.col = col
        self.x = row * gap
        self.y = col * gap
        self.color = (255, 255, 255) # WHITE
        self.neighbors = []
        self.gap = gap
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.gap, self.gap))

    def update_neighbors(self, grid):
        self.neighbors = []
        # Check Down, Up, Right, Left
        if self.row < self.total_rows - 1 and grid[self.row + 1][self.col].color != (0, 0, 0):
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and grid[self.row - 1][self.col].color != (0, 0, 0):
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and grid[self.row][self.col + 1].color != (0, 0, 0):
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and grid[self.row][self.col - 1].color != (0, 0, 0):
            self.neighbors.append(grid[self.row][self.col - 1])