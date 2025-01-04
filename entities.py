from math import floor
from getch import getch
from time import sleep
from random import randint, choice, shuffle
from termcolor import colored
from item import Item
import os
from delayed_print import dprint
from copy import deepcopy

class Combat:
    def __init__(self, player, enemy, item):
        self.player = player
        self.enemy = enemy
        self.exp = enemy.exp[0]
        self.itemAtk = 0
        self.item = item

    def start(self):
        turnOrder = sorted(self.player.summons + [self.player, self.enemy], key=lambda x: x.speed, reverse=True)
        for entity in turnOrder:
            entity.sp[1] = entity.sp[0]

        def show_info():
            print(f"Health: {self.player.health[1]}/{self.player.health[0]}")
            print(f"SP: {self.player.sp[1]}/{self.player.sp[0]}")
            print(f"Weakness: {self.player.weaknessBar[1]}/{self.player.weaknessBar[0]}")
            print()
            print(f"Enemy Health: {self.enemy.health[1]}/{self.enemy.health[0]}")
            print(f"Enemy SP: {self.enemy.sp[1]}/{self.enemy.sp[0]}")
            print(f"Enemy Weakness: {self.enemy.weaknessBar[1]}/{self.enemy.weaknessBar[0]}")
            print()


        while self.player.health[1] > 0 and self.enemy.health[1] > 0:
            os.system("clear")
            show_info()

            current = turnOrder.pop(0)

            if current.broken:
                current.unBreak()
                continue

            if type(current) is Player:
                print("Do you want to attack (1), wait (2), rest (3) or use an item (4)?")
                action = getch()
                while action not in ["1","2","3","4"]:
                    action = getch()
                os.system("clear")
                show_info()
                if action == "1":
                    for number, ability in enumerate(current.abilities):
                        print(f"{number+1}: {ability.name} (Damage: {floor(ability.multiplier*self.player.atk)}) (Type: {ability.type}) (SP: {ability.cost}) ")
                    print("What move do you want to use?")
                    num = getch()
                    while True:
                        try:
                            num = int(num)
                            if num in range(1,len(self.player.abilities)+1):
                                break
                        except:
                            pass
                        num = getch()
                    os.system("clear")
                    show_info()
                    self.enemy = current.attack(self.enemy, self.player.abilities[num-1])
                    sleep(1.5)
                elif action == "2":
                    self.player.wait()
                    sleep(1.5)
                elif action == "3":
                    self.player.rest()
                    sleep(1.5)
                elif action == "4":
                    if len(self.player.inventory) > 0:
                        for number, item in enumerate(current.inventory):
                            print(f"{number+1}:", item.name)
                        print("What item do you want to use?")
                        num = getch()
                        while True:
                            try:
                                num = int(num)
                                if num in range(1,len(self.player.inventory)+1):
                                    break
                            except:
                                pass
                            num = getch()
                        os.system("clear")
                        show_info()
                        self.itemAtk += self.player.inventory[num-1].attack
                        current.use_item(self.player.inventory.pop(num-1))
                    else:
                        print("Your inventory is empty")
                    sleep(1.5)
            else:
                shuffle(current.abilities)
                for move in current.abilities:
                    if move.cost <= current.sp[1]:
                        if current.isSummon:
                            self.enemy = current.attack(self.enemy, move)
                            sleep(1.5)
                            break
                        else:
                            target = choice(turnOrder)
                            target = current.attack(target, move)
                            if target.isSummon and target.health[1] < 0:
                                print(f"{target} has died.")
                                turnOrder.remove(target)
                                self.player.summons.remove(target)
                            sleep(1.5)
                            break
                else:
                    if current.sp[1] < 0.1 * current.sp[0]:
                        current.rest()
                        sleep(1.5)
                    else:
                        current.wait()
                        sleep(1.5)

            turnOrder.append(current)

        if self.enemy.health[1] <= 0:
            self.enemy.health[1] = self.enemy.health[0]
            self.enemy.sp[1] = self.enemy.sp[0]
            self.enemy.weaknessBar[1] = self.enemy.weaknessBar[0]
            os.system("clear")
            self.player.weaknessBar[1] = self.player.weaknessBar[0]
            self.player.atk -= self.itemAtk
            for summon in self.player.summons:
                summon.exp[1] += self.exp
                summon.weaknessBar[1] = summon.weaknessBar[0]
                while summon.exp[1] > summon.exp[0]:
                    summon.levelUp()
            print(f"You have defeated the {self.enemy.name}")
            if randint(1,10) == 1:
                print(f"The {self.enemy.name} dropped a {self.item.name}")
                self.player.add_item(self.item)
            print("Do you want to absorb it (1) or necromance it (2)")
            input = getch()
            while input != "1" and input != "2":
                input = getch()
            os.system("clear")
            if input == "1":
                self.player.absorb(self.enemy)
            elif input == "2":
                self.player.necromance(self.enemy)
            print("\nPress space to continue")
            opt = getch()
            while opt != " ":
                print("\033[K\033[F")
                opt = getch()
            os.system("clear")
        else:
            print("A fatal hit!")
            print("\nPress space to go back")
            back = getch()
            while back != " ":
                back = getch()

        return self.player, self.enemy

class Entity:
    def __init__(self, name:str, health:int, weaknesses:list, weaknessBar:int, attack:int, speed:int, SP:int, abilities:list, abilityList:dict):
        self.name = name
        self.health = [health,health]
        self.weaknesses = weaknesses
        self.weaknessBar = [weaknessBar,weaknessBar]
        self.resting = False
        self.broken = False
        self.atk = attack
        self.speed = speed
        self.sp = [SP,SP]
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
                target.health[1] -= floor(floor(ability.multiplier*self.atk)*1.5)
            else:
                target.health[1] -= floor(ability.multiplier*self.atk)

            if ability.recoil > 0:
                print(f"self.name took {self.health[0] * ability.recoil//100} recoil damage from using {ability.name}")
            if ability.recoil < 0:
                print(f"self.name healed {self.health[0] * ability.recoil//100} from using {ability.name}")
            self.health[1] -= self.health[0] * ability.recoil//100

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
    def __init__(self, name:str, health: int, weaknesses:list, weaknessBar:int, attack:int, speed:int, SP:int, abilities:list, abilityList:dict, exp:int, lvl:int):
        super().__init__(name, health, weaknesses, weaknessBar, attack, speed, SP, abilities, abilityList)
        self.exp = [exp,0]
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
        num = getch()
        while True:
            try:
                num = int(num)
                if num in range(len(available)+1):
                    break
            except:
                pass
            num = getch()
        if len(self.abilities) < 5:
            print(f"{self.name} has learned {available[num-1].name}")
            self.abilities.append(available[num-1])
        elif len(self.abilities) >= 5:
            print(f"{self.name} has too many abilities, do you want to forget an ability? (y/n)")
            forget = getch
            while forget != "y" and forget != "n":
                forget = getch()
            if forget == "y":
                for number, ability in enumerate(self.abilities):
                    print(number+1, ability.name)
                print(f"What move does {self.name} want to forget?")
                fMove = getch()
                while True:
                    try:
                        fMove = int(fMove)
                        if fMove in range(1,6):
                            break
                    except:
                        pass
                    fMove = getch()
                print(f"{self.name} has forgotten {self.abilities[fMove-1]} and learned {available[num-1].name}!")
                self.abilities[fMove-1] = available[num-1].name
        elif input == "n":
            print(f"{self.name} gave up learning {available[num-1].name}")

    def becomeSummon(self):
        summon = deepcopy(self)
        summon.isSummon = True
        summon.name = "Summoned " + summon.name

        return summon

    def levelUp(self, hidden):
        self.lvl += 1
        self.exp[1] -= self.exp[0]
        if self.exp[1] < 0:
            self.exp[1] = 0
        self.exp[0] = floor(self.exp[0] * 1.1)

        self.health[1] += floor(self.health[0] * 1.05) - self.health[0]
        self.health[0] = floor(self.health[0] * 1.05)
        self.atk = floor(self.atk * 1.05)
        self.sp[1] += floor(self.sp[0] * 1.05) - self.sp[0]
        self.sp[0] = floor(self.sp[0] * 1.05)


        if not hidden:
            print(f"{self.name} has leveled up to level {self.lvl}!")
            if self.lvl in self.abilityList:
                if len(self.abilities) > 5:
                    print(f"{self.name} wants to learn {self.abilityList[self.lvl].name}")
                    print(f"Do you want to teach {self.name} {self.abilityList[self.lvl].name}? (y/n)")
                    input = getch()
                    while input != "y" and input != "n":
                        input = getch()
                    
                    if input == "y" and len(self.abilities) < 5:
                        print(f"{self.name} has learned {self.abilityList[self.lvl].name}")
                        self.abilities.append(self.abilityList[self.lvl])
                    elif input == "y" and len(self.abilities) > 5:
                        print(f"{self.name} has too many abilities, do you want to forget an ability? (y/n)")
                        forget = getch()
                        while forget != "y" and forget != "n":
                            forget = getch()
                        if forget == "y":
                            for number, ability in enumerate(self.abilities):
                                print(number+1, ability.name)
                            print(f"\nWhat move does {self.name} want to forget?")
                            num = getch()
                            while True:
                                try:
                                    num = int(num)
                                    if num in range(1,6):
                                        break
                                except:
                                    pass
                                num = getch()
                            print(f"{self.name} has forgotten {self.abilities[num-1]} and learned {self.abilityList[self.lvl].name}!")
                            self.abilities[num-1] = self.abilityList[self.lvl]
                    elif input == "n":
                        print(f"{self.name} gave up learning {self.abilityList[self.lvl].name}")
                else:
                    print(f"{self.name} has learned {self.abilityList[self.lvl].name}")
                    self.abilities.append(self.abilityList[self.lvl])
            else:
                if self.lvl in self.abilityList:
                    self.abilities.append(self.abilityList[self.lvl])
                    if len(self.abilities) > 5:
                        self.abilities.pop(0)

    def calculate_stats(self):
        for i in range(self.lvl-1):
            self.levelUp(True)

    def show_details(self):
        return f"Name: {self.name}\nHealth: {self.health[1]}/{self.health[0]}\nWeaknesses: {", ".join(self.weaknesses)}\nAttack: {self.atk}\nSpeed: {self.speed}\nSP: {self.sp[0]}\nAbilities: {", ".join([x.name for x in self.abilities])}\nlvl: {self.lvl} ({self.exp[1]}/{self.exp[0]})"

class Player(Entity):
    def __init__(self, name:str, health:int, weaknesses:list, weaknessBar:int, attack:int, speed:int, SP:int, abilities:list):
        super().__init__(name, health, weaknesses, weaknessBar, attack, speed, SP, abilities, {1: abilities[0]})
        self.inventory = []
        self.currentPos = [1,0]
        self.summons = []
        self.reputation = 50
        self.alive = True
        self.explosives = 1
        self.isSummon = False

    def move(self, direction, location):
        location.room[self.currentPos[0]][self.currentPos[1]] = " "
        
        if direction == "w":
            self.currentPos[0] -= 1
            if self.currentPos[0] < 0 or self.currentPos[0] > len(location.room)-1:
                self.currentPos[0] += 1
            if location.room[self.currentPos[0]][self.currentPos[1]] == "x":
                self.currentPos[0] += 1
            if location.room[self.currentPos[0]][self.currentPos[1]] == "#" and location.room[self.currentPos[0]-1][self.currentPos[1]] != " " and location.room[self.currentPos[0]-1][self.currentPos[1]] != "'":
                self.currentPos[0] += 1
            if location.room[self.currentPos[0]][self.currentPos[1]] == "#" and location.room[self.currentPos[0]-1][self.currentPos[1]] != "x" and location.room[self.currentPos[0]-1][self.currentPos[1]] != "#":
                location.room[self.currentPos[0]-1][self.currentPos[1]] = "#"

        if direction == "a":
            self.currentPos[1] -= 1
            if self.currentPos[1] < 0 or self.currentPos[1] > len(location.room)-1:
                self.currentPos[1] += 1
            if location.room[self.currentPos[0]][self.currentPos[1]] == "x":
                self.currentPos[1] += 1
            if location.room[self.currentPos[0]][self.currentPos[1]] == "#" and location.room[self.currentPos[0]][self.currentPos[1]-1] != " " and location.room[self.currentPos[0]][self.currentPos[1]-1] != "'":
                self.currentPos[1] += 1
            if location.room[self.currentPos[0]][self.currentPos[1]] == "#" and location.room[self.currentPos[0]][self.currentPos[1]-1] != "x" and location.room[self.currentPos[0]][self.currentPos[1]-1] != "#":
                location.room[self.currentPos[0]][self.currentPos[1]-1] = "#"

        if direction == "s":
            self.currentPos[0] += 1
            if self.currentPos[0] < 0 or self.currentPos[0] > len(location.room)-1:
                self.currentPos[0] -= 1
            if location.room[self.currentPos[0]][self.currentPos[1]] == "x":
                self.currentPos[0] -= 1
            if location.room[self.currentPos[0]][self.currentPos[1]] == "#" and location.room[self.currentPos[0]+1][self.currentPos[1]] != " " and location.room[self.currentPos[0]+1][self.currentPos[1]] != "'":
                self.currentPos[0] -= 1
            if location.room[self.currentPos[0]][self.currentPos[1]] == "#" and location.room[self.currentPos[0]+1][self.currentPos[1]] != "x" and location.room[self.currentPos[0]+1][self.currentPos[1]] != "#":
                location.room[self.currentPos[0]+1][self.currentPos[1]] = "#"

        if direction == "d":
            self.currentPos[1] += 1
            if self.currentPos[1] < 0 or self.currentPos[1] > len(location.room)-1:
                self.currentPos[1] -= 1
            if location.room[self.currentPos[0]][self.currentPos[1]] == "x":
                self.currentPos[1] -= 1
            if location.room[self.currentPos[0]][self.currentPos[1]] == "#" and location.room[self.currentPos[0]][self.currentPos[1]+1] != " " and location.room[self.currentPos[0]][self.currentPos[1]+1] != "'":
                self.currentPos[1] -= 1
            if location.room[self.currentPos[0]][self.currentPos[1]] == "#" and location.room[self.currentPos[0]][self.currentPos[1]+1] != "x" and location.room[self.currentPos[0]][self.currentPos[1]+1] != "#":
                location.room[self.currentPos[0]][self.currentPos[1]+1] = "#"

        if location.room[self.currentPos[0]][self.currentPos[1]] == colored("P", 'light_yellow'):
            location.room[self.currentPos[0]][self.currentPos[1]] = colored("@", 'red')
            os.system("clear")
            print(f"Controls:\nMovement (wasd)\nPlace Explosive (e)\nManage Player (q)\n\nHealth: {self.health[1]}/{self.health[0]}\nExplosives: {self.explosives}\n")
            location.show_room()
            sleep(0.5)
            self = location.play(self)
        elif location.room[self.currentPos[0]][self.currentPos[1]] == colored("E", 'light_magenta'):
            location.room[self.currentPos[0]][self.currentPos[1]] = colored("@", 'red')
            os.system("clear")
            print(f"Controls:\nMovement (wasd)\nPlace Explosive (e)\nManage Player (q)\n\nHealth: {self.health[1]}/{self.health[0]}\nExplosives: {self.explosives}\n")
            location.show_room()
            sleep(0.5)
            enemy  = choice(location.enemyList)
            item = choice(location.itemList)
            os.system("clear")
            print(f"You encountered a {enemy.name}")
            sleep(1)
            self, enemy = Combat(self, enemy, item).start()
        elif location.room[self.currentPos[0]][self.currentPos[1]] == colored("I", 'light_blue'):
            location.room[self.currentPos[0]][self.currentPos[1]] = colored("@", 'red')
            os.system("clear")
            print(f"Controls:\nMovement (wasd)\nPlace Explosive (e)\nManage Player (q)\n\nHealth: {self.health[1]}/{self.health[0]}\nExplosives: {self.explosives}\n")
            location.show_room()
            sleep(0.5)
            os.system("clear")
            item = choice(location.itemList)
            print(f"You picked up a {item.name}")
            self.add_item(item)
            print("\nPress space to continue")
            opt = getch()
            while opt != " ":
                print("\033[K\033[F")
                opt = getch()
            os.system("clear")
        elif location.room[self.currentPos[0]][self.currentPos[1]] == colored("N", 'light_green'):
            location.room[self.currentPos[0]][self.currentPos[1]] = colored("@", 'red')
            os.system("clear")
            print(f"Controls:\nMovement (wasd)\nPlace Explosive (e)\nManage Player (q)\n\nHealth: {self.health[1]}/{self.health[0]}\nExplosives: {self.explosives}\n")
            location.show_room()
            sleep(0.5)
            os.system("clear")
            if location.npcList:
                npc = choice(location.npcList)
                self = npc.interact(self, location)
            else:
                print("You killed everyone on this floor")
            print("\nPress space to continue")
            opt = getch()
            while opt != " ":
                print("\033[K\033[F")
                opt = getch()
            os.system("clear")
        elif location.room[self.currentPos[0]][self.currentPos[1]] == colored("e", 'light_yellow'):
            location.room[self.currentPos[0]][self.currentPos[1]] = colored("@", 'red')
            self.explosives += 1
        else:
            location.room[self.currentPos[0]][self.currentPos[1]] = colored("@", 'red')
 
    def learn(self, ability):
        print(f"Do you want to learn {ability.name}? (y/n)")
        input = getch()
        while input != "y" and input != "n":
            input = getch()
        
        if input == "y" and len(self.abilities) < 5:
            print(f"You have learned {ability.name}")
            self.abilities.append(ability)
            if ability not in self.abilityList.values():
                self.abilityList[len(self.abilityList)+1] = ability
        elif input == "y" and len(self.abilities) > 5:
            print("You have too many abilities, do you want to forget an ability? (y/n)")
            forget = getch()
            while forget != "y" and forget != "n":
                forget = getch()
            if forget == "y":
                for number, ability in enumerate(self.abilities):
                    print(number+1, ability.name)
                print("\nWhat move do you want to forget?")
                num = getch()
                while True:
                    try:
                        num = int(num)
                        if num in range(1,6):
                            break
                    except:
                        pass
                    num = getch()
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
            if ability not in self.abilityList.values() and randint(1,2) == 1:
                self.abilityList[len(self.abilityList)+1] = ability
                print(f"You have successfully gained {ability.name}")
                self.learn(ability)
        print()
        print(f"+{floor(enemy.health[0]*0.25)} health")
        print(f"+{floor(enemy.atk*0.25)} attack")
        print(f"+{floor(enemy.speed*0.25)} speed")
        print(f"+{floor(enemy.sp[0]*0.25)} sp")
        self.health[0] += floor(enemy.health[0]*0.25)
        self.health[1] += floor(enemy.health[0]*0.25)
        self.atk += floor(enemy.atk*0.25)
        self.speed += floor(enemy.speed*0.25)
        self.sp[0] += floor(enemy.sp[0]*0.25)

    def necromance(self, enemy):
        print(f"You have lost {floor(self.health[0]*0.2)} health to necromance the {enemy.name}")
        self.health[1] -= floor(self.health[0]*0.2)
        self.summons.append(enemy.becomeSummon())

    def add_item(self, item):
        if len(self.inventory) < 20:
            print(f"You added a {item.name} to your inventory")
            self.inventory.append(item)
        else:
            print(f"Your bag was too full and the {item.name} got lost")

    def use_item(self, item):
        print(f"You used the {item.name}")
        if item.type == "Healing":
            if self.health[1] + item.healing < self.health[0]:
                print(f"You were healed by {item.healing}")
                self.health[1] += item.healing
            else:
                print(f"You were healed by {self.health[0]-self.health[1]}")
                self.health[1] = self.health[0]
        elif item.type == "Attack":
            print(f"Your attack was increased by {item.attack}")
            self.atk += item.attack
        elif item.type == "Special":
            if self.health[1] + item.healing < self.health[0]:
                print(f"You were healed by {item.healing} and attack increased by {item.attack}")
                self.health[1] += item.healing
                self.atk += item.attack
            else:
                print(f"You were healed by {self.health[0]-self.health[1]} and attack increased by {item.attack}")
                self.health[1] = self.health[0]
                self.atk += item.attack

    def change_soul(self, swap):
        self.health = swap.health
        self.weaknesses = swap.weaknesses
        self.atk = swap.atk
        self.speed = swap.speed
        self.sp = swap.sp

    def place_explosive(self, location):
        if self.explosives > 0:
            os.system("clear")
            print("You placed an explosive -20 health")
            self.health[1] -= 20
            sleep(1)
            os.system("clear")
            location.room[self.currentPos[0]+1][self.currentPos[1]] = " "
            location.room[self.currentPos[0]-1][self.currentPos[1]] = " "
            location.room[self.currentPos[0]][self.currentPos[1]+1] = " "
            location.room[self.currentPos[0]][self.currentPos[1]-1] = " "
            location.show_room()

    def manage(self):
        os.system("clear")
        print(f"{self.name}\nHealth: {self.health[1]}/{self.health[0]}\nWeaknesses: {", ".join(self.weaknesses)}\nAttack: {self.atk}\nSpeed: {self.speed}\nSP: {self.sp[0]}\nAbilities: {", ".join([x.name for x in self.abilities])}\n")
        print("1: Manage abilities\n2: Manage Summons\n3: View Inventory")
        opt = getch()
        while opt != "1" and opt != "2" and opt != "3":
            opt = getch()
        
        if opt == "1":
            os.system("clear")
            for number, ability in enumerate(self.abilities):
                print(f"{number+1}:", ability.name)

            print("\nSelect an ability")
            ability = getch()
            while True:
                try:
                    ability = int(ability)
                    if ability in range(1,len(self.abilities)+1):
                        break
                except:
                    pass
                ability = getch()

            os.system("clear")
            print(f"Do you want to swap {self.abilities[ability-1].name} (1) or view its details (2)")
            manage = getch()
            while manage != "1" and manage != "2":
                manage = getch()
            os.system("clear")

            if manage == "1":
                os.system("clear")
                for i in self.abilityList:
                    print(f"{i}:", self.abilityList[i].name)
                print(f"\nWhat move do you want to replace {self.abilities[ability-1].name} with?")
                replace = getch()
                while True:
                    try:
                        replace = int(replace)
                        if replace in range(1,len(self.abilityList)+1):
                            break
                    except:
                        pass
                    replace = getch()
                    os.system("clear")

                os.system("clear")
                print(f"You have forgotten {self.abilities[ability-1].name} and learned {self.abilityList[replace].name}!")
                self.abilities[ability-1] = self.abilityList[replace]
            elif manage == "2":
                print(self.abilities[ability-1].show_info())
            
            print("\nPress space to go back")
            back = getch()
            while back != " ":
                back = getch()
        elif opt == "2":
            os.system("clear")
            if self.summons:
                for number, summon in enumerate(self.summons):
                    print(f"{number+1}:", summon.name)
                print("\nWhat summon do you want to manage?")
                manage = getch()
                while True:
                    try:
                        manage = int(manage)
                        if manage in range(1,len(self.summons)+1):
                            break
                    except:
                        pass
                    manage = getch()
                os.system("clear")
                print(self.summons[manage-1].show_details())
                if len(self.summons[manage-1].abilities) > 5:
                    print("\nDo you want to change a move (1) or Soul Swap (2) or go back to the map (3)?")
                    change = getch()
                    while change != "1" and change != "2" and change != "3":
                        change = getch()
                        
                    if change == "1":
                        self.summons[manage-1].learn()
                    elif change == "2":
                        print(f"You haved swapped souls with {self.summon[manage-1].name}")
                        self.change_soul(self.summon[manage-1])
                        self.summons.remove(self.summon[manage-1])
                else:
                    print("\nDo you want to Soul Swap (1) or go back to the map (2)?")
                    swap = getch()
                    while swap != "1" and swap != "2":
                        swap = getch()
                        
                    if swap == "1":
                        print(f"You haved swapped souls with {self.summon[manage-1].name}")
                        self.change_soul(self.summon[manage-1])
                        self.summons.remove(self.summon[manage-1])
                    elif swap == "2":
                        pass

            else:
                print("You have no summons!")
            print("\nPress space to go back")
            back = getch()
            while back != " ":
                back = getch()
        elif opt == "3":
            os.system("clear")
            if self.inventory:
                for number, item in enumerate(self.inventory):
                    print(f"{number+1}:", item.name.capitalize())
                
                print("\nSelect an item")
                item = getch()
                while True:
                    try:
                        item = int(item)
                        if item in range(1,len(self.inventory)+1):
                            break
                    except:
                        pass
                    item = getch()
                
                os.system("clear")
                print(f"Do you want to use {self.inventory[item-1].name.capitalize()} (1) or view its details (2) or discard it (3)?")
                manage = getch()
                while manage != "1" and manage != "2" and manage == "3":
                    manage = getch()
                
                os.system("clear")
                if manage == "1":
                    if self.inventory[item-1].type == "Attack":
                        print("Cannot use attack items outside of battle.")
                    elif self.inventory[item-1].type == "Special":
                        print("Cannot use special items outside of battle.")
                    else:
                        self.use_item(self.inventory.pop(item-1))
                elif manage == "2":
                    print(self.inventory[item-1].show_details())
                elif manage == "3":
                    print(f"You discarded {self.inventory.pop(item-1)}")

            else:
                print("Your inventory is empty!")
            print("\nPress space to go back")
            back = getch()
            while back != " ":
                back = getch()

class NPC:
    def __init__(self, names:list, reputation:int, reward: Item, cost:int, intro:str):
        self.names = names
        self.reputation = reputation
        self.reward = reward
        self.cost = cost
        self.intro = intro

    def interact(self, player, location):
        name = choice(self.names)
        if player.reputation >= 30:
            dprint(f'{name}: "{self.intro}"')
            dprint(f"{name} is offering a {self.reward.name} for {self.cost} health")
            print(f"Do you want to accept (1) or decline (2) or kill (3) Current Health: {player.health[1]}/{player.health[0]}")
            option = getch()
            while option != "1" and option != "2" and option != "3":
                option = getch()
            
            os.system("clear")
            if option == "1":
                print("You accepted the offer")
                print(f"+{self.reputation//2} reputation")
                player.health[1] -= self.cost
                player.reputation += self.reputation//2
                player.add_item(self.reward)
            elif option == "2":
                print("You declined the offer")
            elif option == "3":
                print(f"You killed {name}")
                print(f"-{self.reputation//2} reputation")
                player.reputation -= self.reputation//2
                if player.reputation < 0:
                    player.reputation = 0
                player.add_item(self.reward)
                location.npcList.remove(self)
        else:
            dprint("Go die in a ditch")

        return player
