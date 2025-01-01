from math import floor
from getch import getch
from time import sleep, time
from random import randint
from termcolor import colored
from item import Item

class Entity:
    def __init__(self, name:str, health:list, weaknesses:list, weaknessBar:list, attack:int, speed:int, SP:list, abilities:list, abilityList:dict):
        self.name = name
        self.health = health
        self.weaknesses = weaknesses
        self.weaknessBar = weaknessBar
        self.resting = False
        self.broken = False
        self.atk = attack
        self.speed = speed
        self.sp = SP
        self.abilities = abilities
        self.abilityList = abilityList

    def Break(self):
        print(f"{self.name} has been broken! They took {floor(self.health[0]*0.2)} damage")
        self.health[1] -= floor(self.health[0]*0.2)
        self.broken = True

    def unBreak(self):
        print(f"{self.name} has recovered from being broken!")
        self.broken = False

    def attack(self, target, ability):
        if self.sp[1] >= ability.cost:
            print(f"{self.name} attacked {target.name} with {ability.name}")
            print(f"{target.name} took {floor(ability.multiplier*self.atk)} damage!")

            if ability.type in target.weaknesses:
                target.weaknessBar[1] -= ability.breakDamage
                if target.weaknessBar[1] <= 0:
                    target.Break()

            self.sp[1] -= ability.cost
            self.resting = False

            if target.resting:
                target.health[1] -= floor(ability.damage*self.atk)*1.5
            else:
                target.health[1] -= floor(ability.damage*self.atk)
        else:
            print("You flailed out of exhaustion")
            print(f"{self.name} dealt {floor(self.atk*0.5)} to {target.name} and lost {floor(self.health[0]*0.1)} health!")
            target.health[1] -= floor(self.atk*0.5)
            self.health[1] -= floor(self.health[0]*0.1)

        return target

    def wait(self):
        print(f"{self.name} is waiting this turn")
        self.resting = False
        self.sp[1] += floor(0.33*self.sp[0])
        if self.sp[1] > self.sp[0]:
            self.sp[1] = self.sp[0]
    
    def rest(self):
        print(f"{self.name} is resting this turn")
        self.resting = True
        self.sp[1] += floor(0.66*self.sp[0])
        if self.sp[1] > self.sp[0]:
            self.sp[1] = self.sp[0]

class Enemy(Entity):
    def __init__(self, name:str, health: list, weaknesses:list, weaknessBar:list, attack:int, speed:int, SP:list, abilities:list, abilityList:dict, exp:list, lvl:int):
        super().__init__(name, health, weaknesses, weaknessBar, attack, speed, SP, abilities, abilityList)
        self.exp = exp
        self.lvl = lvl
        self.isSummon = False

    def learn(self):
        available = []
        for key in self.abilityList:
            if key <= self.lvl:
                available.append(self.abilityList[key])
        for number, ability in enumerate(available):
            print(number+1, ability.name)
        print(f"What move does {self.name} want to learn?")
        num = int(getch())
        while num not in range(1, len(available)+1):
            print("Invalid input", end="\r")
            sleep(1)
            print("\033[K")
            num = int(getch())
        if len(self.abilities) < 5:
            print(f"{self.name} has learned {available[num-1].name}")
            self.abilities.append(available[num-1])
        elif len(self.abilities) >= 5:
            print(f"{self.name} has too many abilities, do you want to forget an ability? (y/n)")
            forget = getch.lower()
            while forget != "y" and forget != "n":
                print("Invalid input", end="\r")
                sleep(1)
                print("\033[K")
                forget = getch().lower()
            if forget == "y":
                for number, ability in enumerate(self.abilities):
                    print(number+1, ability.name)
                print("What move do you want to forget?")
                fMove = int(getch())
                while fMove not in range(1,6):
                    print("Invalid input", end="\r")
                    sleep(1)
                    print("\033[K")
                    fMove = int(getch())
                print(f"You have forgotten {self.abilities[fMove-1]} and learned {available[num-1].name}!")
                self.abilities[fMove-1] = available[num-1].name
        elif input == "n":
            print(f"{self.name} gave up learning {available[num-1].name}")

    def becomeSummon(self):
        self.isSummon = True

    def levelUp(self):
        self.lvl += 1
        self.exp[1] -= self.exp[0]
        self.exp[0] = floor(self.exp[0] * 1.1)
        print(f"{self.name} has leveled up to level {self.lvl}!")

class Player(Entity):
    def __init__(self, name:str, health:list, weaknesses:list, weaknessBar:list, attack:int, speed:int, SP:list, abilities:list):
        super().__init__(name, health, weaknesses, weaknessBar, attack, speed, SP, abilities, {})
        self.inventory = []
        self.currentPos = [1,0]
        self.summons = []
        self.reputation = 50
        self.alive = True

    def move(self, direction, location):
        location.room[self.currentPos[0]][self.currentPos[1]] = " "
        
        if direction == "w":
            self.currentPos[0] -= 1
            if location.room[self.currentPos[0]][self.currentPos[1]] == "x":
                self.currentPos[0] += 1
            if location.room[self.currentPos[0]][self.currentPos[1]] == "#" and location.room[self.currentPos[0]-1][self.currentPos[1]] != " " and location.room[self.currentPos[0]-1][self.currentPos[1]] != "'":
                self.currentPos[0] += 1
            if location.room[self.currentPos[0]][self.currentPos[1]] == "#" and location.room[self.currentPos[0]-1][self.currentPos[1]] != "x" and location.room[self.currentPos[0]-1][self.currentPos[1]] != "#":
                location.room[self.currentPos[0]-1][self.currentPos[1]] = "#"

        if direction == "a":
            self.currentPos[1] -= 1
            if location.room[self.currentPos[0]][self.currentPos[1]] == "x":
                self.currentPos[1] += 1
            if location.room[self.currentPos[0]][self.currentPos[1]] == "#" and location.room[self.currentPos[0]][self.currentPos[1]-1] != " " and location.room[self.currentPos[0]][self.currentPos[1]-1] != "'":
                self.currentPos[1] += 1
            if location.room[self.currentPos[0]][self.currentPos[1]] == "#" and location.room[self.currentPos[0]][self.currentPos[1]-1] != "x" and location.room[self.currentPos[0]][self.currentPos[1]-1] != "#":
                location.room[self.currentPos[0]][self.currentPos[1]-1] = "#"

        if direction == "s":
            self.currentPos[0] += 1
            if location.room[self.currentPos[0]][self.currentPos[1]] == "x":
                self.currentPos[0] -= 1
            if location.room[self.currentPos[0]][self.currentPos[1]] == "#" and location.room[self.currentPos[0]+1][self.currentPos[1]] != " " and location.room[self.currentPos[0]+1][self.currentPos[1]] != "'":
                self.currentPos[0] -= 1
            if location.room[self.currentPos[0]][self.currentPos[1]] == "#" and location.room[self.currentPos[0]+1][self.currentPos[1]] != "x" and location.room[self.currentPos[0]+1][self.currentPos[1]] != "#":
                location.room[self.currentPos[0]+1][self.currentPos[1]] = "#"

        if direction == "d":
            self.currentPos[1] += 1
            if location.room[self.currentPos[0]][self.currentPos[1]] == "x":
                self.currentPos[1] -= 1
            if location.room[self.currentPos[0]][self.currentPos[1]] == "#" and location.room[self.currentPos[0]][self.currentPos[1]+1] != " " and location.room[self.currentPos[0]][self.currentPos[1]+1] != "'":
                self.currentPos[1] -= 1
            if location.room[self.currentPos[0]][self.currentPos[1]] == "#" and location.room[self.currentPos[0]][self.currentPos[1]+1] != "x" and location.room[self.currentPos[0]][self.currentPos[1]+1] != "#":
                location.room[self.currentPos[0]][self.currentPos[1]+1] = "#"

        if location.room[self.currentPos[0]][self.currentPos[1]] == colored("P", 'light_yellow'):
            self = location.play(self)

        location.room[self.currentPos[0]][self.currentPos[1]] = colored("@", 'red')
    
    def learn(self, ability):
        print(f"Do you want to learn {ability.name}? (y/n)")
        input = getch().lower()
        while input != "y" and input != "n":
            print("Invalid input", end="\r")
            sleep(1)
            print("\033[K")
            input = getch().lower()
        
        if input == "y" and len(self.abilityList) <= 5:
            print(f"You have learned {ability.name}")
            self.abilities.append(ability)
            if ability not in self.abilityList.values():
                self.abilityList[len(self.abilityList)+1] = ability
        elif input == "y" and len(self.abilityList) > 5:
            print("You have too many abilities, do you want to forget an ability? (y/n)")
            forget = getch.lower()
            while forget != "y" and forget != "n":
                print("Invalid input", end="\r")
                sleep(1)
                print("\033[K")
                forget = getch().lower()
            if forget == "y":
                for number, ability in enumerate(self.abilities):
                    print(number+1, ability.name)
                print("What move do you want to forget?")
                num = int(getch())
                while num not in range(1,6):
                    print("Invalid input", end="\r")
                    sleep(1)
                    print("\033[K")
                    num = int(getch())
                print(f"You have forgotten {self.abilities[num-1]} and learned {ability.name}!")
                self.abilities[num-1] = ability
                if ability not in self.abilityList.values():
                    self.abilityList[len(self.abilityList)+1] = ability
        elif input == "n":
            print(f"You gave up learning {ability.name}")
            if ability in self.abilityList.values():
                self.abilityList[len(self.abilityList)+1] = ability

    def absorb(self, enemy):
        print(f"You absorbed the {enemy.name}")
        self.weaknesses = enemy.weaknesses
        for ability in enemy.abilities:
            if ability not in self.abilityList.values() and randint(1,4) == 1:
                self.abilityList[len(self.abilityList)+1] = ability
                print(f"You have successfully learned {ability.name}")
        self.health += floor(enemy.health*0.25)
        self.atk += floor(enemy.atk*0.25)
        self.speed += floor(enemy.speed*0.25)
        self.sp[0] += floor(enemy.sp[0]*0.25)

    def necromance(self, enemy):
        print(f"You have lost {floor(self.health[0]*0.33)} to necromance {enemy.name}")
        self.health[1] -= floor(self.health[0]*0.33)
        enemy.becomeSummon()
        self.summons.append(enemy)

    def add_item(self, item):
        if len(self.inventory) > 20:
            print(f"You added {item.name} to your inventory")
            self.inventory.append(item)
        else:
            print(f"Your bag was too full and {item.name} got lost")

    def use_item(self, item):
        if item.type == "healing":
            if self.health[1] + item.healing < self.health[0]:
                print(f"You were healed by {item.healing}")
                self.health[1] += item.healing
            else:
                print(f"You were healed by {self.health[0]-self.health[1]}")
                self.health[1] = self.health[0]
        elif item.type == "attack":
            print(f"Your attack was increased by {item.attack}")
            self.atk += item.attack
        elif item.type == "special":
            if self.health[1] + item.healing < self.health[0]:
                print(f"You were healed by {item.healing} and attack increased by {item.attack}")
                self.health[1] += item.healing
                self.atk += item.attack
            else:
                print(f"You were healed by {self.health[0]-self.health[1]} and attack increased by {item.attack}")
                self.health[1] = self.health[0]
                self.atk += item.attack

    def change_soul(self):
        for number, summon in enumerate(self.summons):
            print(number+1, summon.name)
        print("What summon do you want to soul swap with?")
        num = int(getch())
        while num not in range(len(self.summons)):
            print("Invalid input", end="\r")
            sleep(1)
            print("\033[K")
            num = int(getch())
        swap = self.summons.pop(num-1)
        self.health = swap.health
        self.weaknesses = swap.weaknesses
        self.atk = swap.atk
        self.speed = swap.speed
        self.sp = swap.sp

class NPC:
    def __init__(self, name:str, reputation:int, reward: Item, cost:int):
        self.name = name
        self.reputation = reputation
        self.reward = reward
        self.cost = cost