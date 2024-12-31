from random import shuffle, choice

class MazeDimensionError(Exception):
    pass

class Location():
    def __init__(self, type:str, size:int):
        self.type = type
        self.size = size
        self.room = []

    def generate_maze(self):
        if self.size % 2 == 0:
            raise MazeDimensionError("Dimensions must be odd")

        maze = [["x" for i in range(self.size)] for i in range(self.size)]

        x, y = (-1, 1)
        stack = [(y, x)]
        directions = [(0,2), (0,-2), (2,0), (-2,0)]
        
        while len(stack) > 0:
            y, x = stack[-1]

            shuffle(directions)

            for dy, dx in directions:
                ny, nx = y + dy, x + dx
                if nx > 0 and ny > 0 and nx < self.size-1 and ny < self.size-1 and maze[ny][nx] == "x":
                    maze[ny][nx] = " "
                    maze[ny-dy//2][nx-dx//2] = " "
                    stack.append((ny, nx))
                    break
            else:
                stack.pop()

        maze[self.size-2][self.size-1] = " "

        self.room = maze
        #for row in maze:
        #    print(str(row).replace("[", "").replace("]", "").replace(",", "").replace("'", ""))

    def load_enemies(self, enemies):
        pass

    def load_items(self, items):
        pass

    def load_npcs(self, npcs):
        pass

class Minigame(Location):
    def __init__(self, room):
        super().__init__("Minigame", len(room))
        self.room = room
        self.won = False

class Combat():
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy