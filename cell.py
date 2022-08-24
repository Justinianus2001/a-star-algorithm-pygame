class Cell:
    neighbor = []
    def __init__(self, x, y, isObstacle):
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.parent = None
        self.isObstacle = isObstacle
    def add_neighbor(self, width, height, table):
        if self.x > 0:
            self.neighbor.append(table[self.x - 1][self.y])
        if self.x + 1 < width:
            self.neighbor.append(table[self.x + 1][self.y])
        if self.y > 0:
            self.neighbor.append(table[self.x][self.y - 1])
        if self.y + 1 < height:
            self.neighbor.append(table[self.x][self.y + 1])
