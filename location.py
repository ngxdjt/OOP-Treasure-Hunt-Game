from random import shuffle, choice, randint
from entities import *
from getch import getch
from time import sleep
from termcolor import colored
import os

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

        self.room = [["x" for i in range(self.size)] for i in range(self.size)]

        x, y = (-1, 1)
        stack = [(y, x)]
        directions = [(0,2), (0,-2), (2,0), (-2,0)]
        
        while len(stack) > 0:
            y, x = stack[-1]

            shuffle(directions)

            for dy, dx in directions:
                ny, nx = y + dy, x + dx
                if nx > 0 and ny > 0 and nx < self.size-1 and ny < self.size-1 and self.room[ny][nx] == "x":
                    self.room[ny][nx] = " "
                    self.room[ny-dy//2][nx-dx//2] = " "
                    stack.append((ny, nx))
                    break
            else:
                stack.pop()

        self.room[-2][-1] = " "
    
    def show_room(self):
        for row in self.room:
            print(' '.join(row))

    def load_enemies(self):
        for i in range(self.size*7):
            y = randint(1, self.size-1)
            x = randint(1, self.size-1)
            if randint(1, 10) == 1 and self.room[y][x] == " ":
                self.room[y][x] = colored("E", 'light_magenta')
                
    def load_items(self):
        for i in range(self.size*7):
            y = randint(1, self.size-1)
            x = randint(1, self.size-1)
            if randint(1, 10) == 1 and self.room[y][x] == " ":
                self.room[y][x] = colored("I", 'light_blue')

    def load_npcs(self):
        for i in range(self.size*7):
            y = randint(1, self.size-1)
            x = randint(1, self.size-1)
            if randint(1, 10) == 1 and self.room[y][x] == " ":
                self.room[y][x] = colored("N", 'light_green')

class Minigame(Location):
    def __init__(self, room):
        super().__init__("Minigame", len(room))
        self.room = room
        self.won = False

class Combat():
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.turnOrder = sorted(player.summons.extend([player, enemy]), key=lambda x: x.speed)
        self.exp = enemy.exp[0]

    def start(self):
        while self.player.health[1] > 0 and self.enemy.health[1] > 0:
            current = self.turnOrder[0].pop()

            if type(current) is Player:
                for number, ability in enumerate(current.abilities):
                    print(number+1, ability.name)
                print("What move do you want to use?")
                num = int(getch())
                while num not in range(1,6):
                    print("Invalid input", end="\r")
                    sleep(1)
                    print("\033[K")
                    num = int(getch())
                current.attack(self.enemy, ability[num])
            else:
                moves = shuffle(current.abilities)
                for move in moves:
                    if move.cost <= current.sp[1]:
                        if current.isSummon:
                            current.attack(self.enemy, move)
                        else:
                            current.attack(choice(self.turnOrder), move)
                        break
                else:
                    if current.sp[1] < 0.1 * current.sp[0]:
                        current.rest()
                    else:
                        current.wait()

            self.turnOrder.append(current)

        if self.enemy.health[1] <= 0:
            for summon in self.player.summons:
                summon.exp[1] += self.exp
                while summon.exp[1] > summon.exp[0]:
                    summon.levelUp()

player = Player("Bob", [100,100], ["Fire"], [100,100], 20, 10, [50,50], ["Fireball"])
maze = Location("Maze", 51)
maze.generate_maze()
maze.load_enemies()
maze.load_items()
maze.load_npcs()
maze.room[1][0] = colored("@", 'red')
while True:
    maze.show_room()
    direction = getch()
    player.move(direction, maze)
    os.system("clear")