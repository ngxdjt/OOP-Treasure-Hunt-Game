from random import shuffle, choice, randint
from entities import *
from getch import getch
from time import sleep
from termcolor import colored
import os

class MazeDimensionError(Exception):
    pass

class Location:
    def __init__(self, size:int):
        self.size = size
        self.room = []

    def show_room(self):
        for row in self.room:
            print(' '.join(row))

class Maze(Location):
    def __init__(self, size:int):
        super().__init__(size)

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
    def __init__(self, room:list, reward:tuple):
        self.room = room
        self.reward = reward

class ColourSwitch(Minigame):
    def __init__(self):
        super().__init__([["x", "x", "x", "x", "x"], 
                          [" ", " ", colored("P", 'light_yellow'), " ", "x"], 
                          ["x", " ", " ", " ", "x"], 
                          ["x", " ", " ", " ", " "], 
                          ["x", "x", "x", "x", "x"]], (100, 5))

    def play(self, player):
        os.system("clear")
        print("Press any button when this message changes colour")
        sleep(randint(1,5))
        start = time()
        print(colored("\033[FPress any button when this message changes colour", 'red'))
        input = getch()
        end = time()

        if end-start < 1:
            os.system("clear")
            print("You succeeded!")
            print("You gained 100 health and 5 attack")
            player.atk += self.reward[1]
            player.health[0] += self.reward[0]
            player.health[1] += self.reward[0]
            sleep(2)
        else:
            os.system("clear")
            print("You reacted too slowly and lost 100 health and 5 attack")
            player.atk -= self.reward[1]
            player.health[0] -= self.reward[0]
            player.health[1] -= self.reward[0]
            sleep(2)

        return player

class BoxPush(Minigame):
    def __init__(self):
        super().__init__([["x","x", "x", "x", "x", "x", "x"],
                          [" "," ", " ", " ", " ", "'", "x"],
                          ["x"," ", "#", " ", "'", "'", "x"],
                          ["x"," ", " ", " ", " ", " ", "x"],
                          ["x"," ", " ", "#", "#", " ", "x"],
                          ["x"," ", " ", " ", " ", " ", " "],
                          ["x","x", "x", "x", "x", "x", "x"]], (40, 40))
        
    def play(self, player):
        print("Push the boxes over the flames to put them out")
        print("Be careful as setpping on the flames will kill you")
        sleep(2)
        os.system("clear")

        while any("'" in row for row in self.room):
            if self.room[1][5] != "#":
                self.room[1][5] = "'"
            if self.room[2][5] != "#":
                self.room[2][5] = "'"
            if self.room[2][4] != "#":
                self.room[2][4] = "'"
            
            os.system("clear")
            self.show_room()
            direction = getch()
            player.move(direction, self)
            os.system("clear")
            self.show_room()

            if player.currentPos == [5, 6]:
                break
            if player.currentPos == [1, 5] or player.currentPos == [2, 5] or player.currentPos == [2, 4]:
                player.health[1] = 0
                sleep(0.5)
                os.system("clear")
                print("You died by stepping in the fire")
                break
        
        if not any("'" in row for row in self.room):
            sleep(0.5)
            os.system("clear")
            print("You succeeded!")
            print("You gained 40 health and 40 attack")
            player.atk += self.reward[1]
            player.health[0] += self.reward[0]
            player.health[1] += self.reward[0]

        return player
    
class Combat:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.turnOrder = sorted(player.summons.extend([player, enemy]), key=lambda x: x.speed)
        self.exp = enemy.exp[0]

    def start(self):
        while self.player.health[1] > 0 and self.enemy.health[1] > 0:
            current = self.turnOrder.pop(0)

            if current.broken:
                current.unBreak()
                continue

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
                self.enemy = current.attack(self.enemy, ability[num-1])
            else:
                moves = shuffle(current.abilities)
                for move in moves:
                    if move.cost <= current.sp[1]:
                        if current.isSummon:
                            self.enemy = current.attack(self.enemy, move)
                        else:
                            target = choice(self.turnOrder)
                            target = current.attack(target, move)
                else:
                    if current.sp[1] < 0.1 * current.sp[0]:
                        current.rest()
                    else:
                        current.wait()

            self.turnOrder.append(current)

        if self.enemy.health[1] <= 0:
            self.player.weaknessBar[1] = self.player.weaknessBar[0]
            for summon in self.player.summons:
                summon.exp[1] += self.exp
                summon.weaknessBar[1] = summon.weaknessBar[0]
                while summon.exp[1] > summon.exp[0]:
                    summon.levelUp()
        else:
            self.player.alive = False

        return self.player

os.system("clear")
player = Player("Bob", [100,100], ["Fire"], [100,100], 20, 10, [50,50], ["Fireball"])
maze = Maze(51)
maze.generate_maze()
maze.load_enemies()
maze.load_items()
maze.load_npcs()
maze.room[1][0] = colored("@", 'red')
box = BoxPush()
box.room[1][0] = colored("@", 'red')
colour = ColourSwitch()
colour.room[1][0] = colored("@", 'red')

# box = BoxPush()dd
# box.room[1][0] = colored("@", 'red')
# player = box.play(player)

while True:
    os.system("clear")
    colour.show_room()
    direction = getch()
    player.move(direction, colour)