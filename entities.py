from math import floor
from getch import getch
from time import sleep
from random import randint, choice, shuffle
from termcolor import colored
from item import Item
import os
from reusable import dprint, space_to_continue, list_select
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
            entity.weaknessBar[1] = entity.weaknessBar[0]

        def show_info():
            print(f"Health: {self.player.health[1]}/{self.player.health[0]}")
            print(f"SP: {self.player.sp[1]}/{self.player.sp[0]}")
            print(f"Weakness: {self.player.weaknessBar[1]}/{self.player.weaknessBar[0]}")
            print()
            print(f"Enemy Health: {self.enemy.health[1]}/{self.enemy.health[0]}")
            print(f"Enemy SP: {self.enemy.sp[1]}/{self.enemy.sp[0]}")
            print(f"Enemy Weakness: {self.enemy.weaknessBar[1]}/{self.enemy.weaknessBar[0]}")
            print()
            print(f"Turn Order: {', '.join([x.name for x in turnOrder])}")
            print()


        while self.player.health[1] > 0 and self.enemy.health[1] > 0:
            os.system("clear")
            show_info()

            current = turnOrder[0]

            if current.broken:
                current.unBreak()
                turnOrder.append(turnOrder.pop(0))
                space_to_continue()
                continue
            
            current.resting = False

            if isinstance(current, Player):
                print("Do you want to attack (1), wait (2), rest (3) or use an item (4)?")
                action = getch()
                while action not in ["1","2","3","4"] or (not self.player.inventory and action == "4"):
                    if action == "4":
                        print("Your inventory is empty!")
                        space_to_continue()
                        show_info()
                        print("Do you want to attack (1), wait (2), rest (3) or use an item (4)?")
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
                    self.enemy, msg = current.attack(self.enemy, self.player.abilities[num-1])
                    os.system("clear")
                    show_info()
                    print(msg)
                    if self.enemy.weaknessBar[1] <= 0 and not self.enemy.broken:
                        self.enemy.Break()
                    space_to_continue()
                elif action == "2":
                    msg = self.player.wait()
                    os.system("clear")
                    show_info()
                    print(msg)
                    space_to_continue()
                elif action == "3":
                    msg = self.player.rest()
                    os.system("clear")
                    show_info()
                    print(msg)
                    space_to_continue()
                elif action == "4":
                    item, index = list_select(self.player.inventory, "What item do you want to use?")
                    if item == " ":
                        print("Your indecisiveness has you pondering and you miss your turn.")
                    else:
                        self.itemAtk += item.attack
                        current.use_item(self.player.inventory.pop(index))
                    space_to_continue()
            else:
                shuffle(current.abilities)
                for move in current.abilities:
                    if move.cost <= current.sp[1]:
                        if current.isSummon:
                            self.enemy, msg = current.attack(self.enemy, move)
                            os.system("clear")
                            show_info()
                            print(msg)
                            if self.enemy.weaknessBar[1] <= 0 and not self.enemy.broken:
                                self.enemy.Break()
                            space_to_continue()
                            break
                        else:
                            target = choice(turnOrder)
                            while (not isinstance(target, Player)) and (not target.isSummon):
                                target = choice(turnOrder)
                            target, msg = current.attack(target, move)
                            if target.isSummon and target.health[1] < 0:
                                print(f"{target.name} has died.")
                                turnOrder.remove(target)
                                self.player.summons.remove(target)
                            os.system("clear")
                            show_info()
                            print(msg)
                            if target.weaknessBar[1] <= 0 and not self.enemy.broken:
                                target.Break()
                            space_to_continue()
                            break
                else:
                    if current.sp[1] < 0.1 * current.sp[0]:
                        msg = current.rest()
                        os.system("clear")
                        show_info()
                        print(msg)
                    else:
                        msg = current.wait()
                        os.system("clear")
                        show_info()
                        print(msg)
                    space_to_continue()

            turnOrder.append(turnOrder.pop(0))

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
                while summon.exp[1] >= summon.exp[0]:
                    summon.levelUp(False)
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
            space_to_continue()
        else:
            print("A fatal hit!")
            space_to_continue()

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
        self.weaknessBar[1] = self.weaknessBar[0]

    def attack(self, target, ability):
        if self.sp[1] >= ability.cost:
            print(f"{self.name} attacked {target.name} with {ability.name}")

            if ability.type in target.weaknesses:
                target.weaknessBar[1] -= ability.breakDamage
                if target.weaknessBar[1] == 0:
                    target.weaknessBar[1] = 0

            self.sp[1] -= ability.cost

            if target.resting:
                target.health[1] -= floor(floor(ability.multiplier*self.atk)*1.5)
            else:
                target.health[1] -= floor(ability.multiplier*self.atk)

            if ability.recoil > 0:
                print(f"self.name took {self.health[0] * ability.recoil//100} recoil damage from using {ability.name}")
            if ability.recoil < 0:
                print(f"self.name healed {self.health[0] * ability.recoil//100} from using {ability.name}")
            self.health[1] -= self.health[0] * ability.recoil//100
            if self.health[1] > self.health[0]:
                self.health[1] = self.health[0]

        else:
            print("You flailed out of exhaustion")
            print(f"{self.name} dealt {floor(self.atk*0.5)} to {target.name} and lost {floor(self.health[0]*0.1)} health!")
            target.health[1] -= floor(self.atk*0.5)
            self.health[1] -= floor(self.health[0]*0.1)

        if target.resting:
            return target, f"{self.name} attacked {target.name} with {ability.name}\n{target.name} took {floor(floor(ability.multiplier*self.atk)*1.5)} damage!"
        else:
            return target, f"{self.name} attacked {target.name} with {ability.name}\n{target.name} took {floor(ability.multiplier*self.atk)} damage!"

    def wait(self):
        self.resting = False
        self.sp[1] += floor(0.33*self.sp[0])
        if self.sp[1] > self.sp[0]:
            self.sp[1] = self.sp[0]
        return f"{self.name} is waiting this turn"
    
    def rest(self):
        self.resting = True
        self.sp[1] += floor(0.66*self.sp[0])
        if self.sp[1] > self.sp[0]:
            self.sp[1] = self.sp[0]
        return f"{self.name} is resting this turn"

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
        ability, index = list_select(available, f"What move does {self.name} want to learn?")
        if len(self.abilities) < 5:
            print(f"{self.name} has learned {ability.name}")
            self.abilities.append(ability)
        elif len(self.abilities) >= 5:
            print(f"{self.name} has too many abilities, do you want to forget an ability? (y/n)")
            forget = getch
            while forget != "y" and forget != "n":
                forget = getch()
            if forget == "y":
                fMove, fIndex = list_select(self.abilities, f"What move does {self.name} want to forget?")
                print(f"{self.name} has forgotten {fMove.name} and learned {ability.name}!")
                self.abilities[fIndex] = ability
        elif input == "n":
            print(f"{self.name} gave up learning {ability.name}")

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
        self.atk = floor(self.atk * 1.2)
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
            print(f"Controls:\nMovement (wasd)\nPlace Explosive (e)\nManage Player (q)\n\nHealth: {self.health[1]}/{self.health[0]}\nExplosives: {self.explosives}\nReputation: {self.reputation}\n")
            location.show_room()
            sleep(0.5)
            self = location.play(self)
        elif location.room[self.currentPos[0]][self.currentPos[1]] == colored("E", 'light_magenta'):
            location.room[self.currentPos[0]][self.currentPos[1]] = colored("@", 'red')
            os.system("clear")
            print(f"Controls:\nMovement (wasd)\nPlace Explosive (e)\nManage Player (q)\n\nHealth: {self.health[1]}/{self.health[0]}\nExplosives: {self.explosives}\nReputation: {self.reputation}\n")
            location.show_room()
            sleep(0.5)
            enemy  = choice(location.enemyList)
            item = choice(location.itemList)
            os.system("clear")
            print(f"You encountered a {enemy.name}")
            sleep(0.5)
            self, enemy = Combat(self, enemy, item).start()
        elif location.room[self.currentPos[0]][self.currentPos[1]] == colored("I", 'light_blue'):
            location.room[self.currentPos[0]][self.currentPos[1]] = colored("@", 'red')
            os.system("clear")
            print(f"Controls:\nMovement (wasd)\nPlace Explosive (e)\nManage Player (q)\n\nHealth: {self.health[1]}/{self.health[0]}\nExplosives: {self.explosives}\nReputation: {self.reputation}\n")
            location.show_room()
            sleep(0.5)
            os.system("clear")
            item = choice(location.itemList)
            print(f"You picked up a {item.name}")
            self.add_item(item)
            space_to_continue()
        elif location.room[self.currentPos[0]][self.currentPos[1]] == colored("N", 'light_green'):
            location.room[self.currentPos[0]][self.currentPos[1]] = colored("@", 'red')
            os.system("clear")
            print(f"Controls:\nMovement (wasd)\nPlace Explosive (e)\nManage Player (q)\n\nHealth: {self.health[1]}/{self.health[0]}\nExplosives: {self.explosives}\nReputation: {self.reputation}\n")
            location.show_room()
            sleep(0.5)
            os.system("clear")
            if location.npcList:
                npc = choice(location.npcList)
                self = npc.interact(self, location)
            else:
                print("You killed everyone on this floor")
            space_to_continue()
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
            if ability not in self.abilityList.values():
                self.abilityList[len(self.abilityList)+1] = ability

    def absorb(self, enemy):
        print(f"You absorbed the {enemy.name}\n")
        self.weaknesses = enemy.weaknesses
        print(f"+{floor(enemy.health[0]*0.5)} health")
        print(f"+{floor(enemy.atk*0.5)} attack")
        print(f"+{floor(enemy.speed*0.5)} speed")
        print(f"+{floor(enemy.sp[0]*0.5)} SP")

        for ability in enemy.abilities:
            if ability not in self.abilityList.values() and randint(1,2) == 1:
                self.abilityList[len(self.abilityList)+1] = ability
                print(f"\nYou have successfully gained {ability.name}")
                self.learn(ability)

        self.health[0] += floor(enemy.health[0]*0.5)
        self.health[1] += floor(enemy.health[0]*0.5)
        self.atk += floor(enemy.atk*0.5)
        self.speed += floor(enemy.speed*0.5)
        self.sp[0] += floor(enemy.sp[0]*0.5)
        self.weaknessBar[0] += floor(enemy.weaknessBar[0]*0.5)

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
            location.room[self.currentPos[0]+1][self.currentPos[1]] = " "
            location.room[self.currentPos[0]-1][self.currentPos[1]] = " "
            location.room[self.currentPos[0]][self.currentPos[1]+1] = " "
            location.room[self.currentPos[0]][self.currentPos[1]-1] = " "
            print("\nPress space to continue")
            opt = getch()
            while opt != " ":
                print("\033[K\033[F")
                opt = getch()
            os.system("clear")

    def manage(self):
        os.system("clear")
        print(f"{self.name}\nHealth: {self.health[1]}/{self.health[0]}\nWeaknesses: {", ".join(self.weaknesses)}\nAttack: {self.atk}\nSpeed: {self.speed}\nSP: {self.sp[0]}\nAbilities: {", ".join([x.name for x in self.abilities])}\n")
        print("1: Manage abilities\n2: Manage Summons\n3: View Inventory\n(Press space to go back)")
        opt = getch()
        while opt != "1" and opt != "2" and opt != "3" and opt != " ":
            opt = getch()
        
        if opt == "1":
            os.system("clear")
            select = list_select(self.abilities, "\nSelect an ability or press space to go back")[0]
            if select != " ":
                os.system("clear")
                print(f"Swap {select.name} (1)\nView {select.name} details (2)\n(Press space to go back)")
                manage = getch()
                if manage != " ":
                    while manage != "1" and manage != "2":
                        manage = getch()
                    os.system("clear")

                    if manage == "1":
                        replace, index = list_select(list(self.abilityList.values()), f"\nWhat move do you want to replace {select.name} with?")

                        os.system("clear")
                        print(f"You have forgotten {select.name} and learned {replace.name}!")
                        for i in range(len(self.abilities)):
                            if self.abilities[i] == select:
                                self.abilities[i] = replace
                                break
                    elif manage == "2":
                        print(select.show_info())
            
                    print("\nPress space to go back")
                    back = getch()
                    while back != " ":
                        back = getch()
        elif opt == "2":
            os.system("clear")
            if self.summons:
                summon, index = list_select(self.summons, "\nWhat summon do you want to manage?\n(Press space to go back)")
                if summon != " ":
                    os.system("clear")
                    print(summon.show_details())
                    if len(summon.abilities) > 5:
                        print("\nChange an ability (1)\nHeal summon (2)\nSoul Swap (3)\n(Press space to go back)")
                        change = getch()
                        while change != "1" and change != "2" and change != "3" and change != " ":
                            change = getch()
                        
                        os.system("clear")
                        if change == "1":
                            summon.learn()
                        elif change == "2":
                            print(f"How much health do you want to give it?")
                            heal = input()
                            while True:
                                try:
                                    heal = int(heal)
                                    break
                                except:
                                    os.system("clear")
                                    print(f"How much health do you want to give it?")
                                    heal = input()
                            os.system("clear")
                            if summon.health[1] + heal > summon.health[0]:
                                print(f"{summon.name} was healed by {summon.health[0]-summon.health[1]}")
                                self.health[1] -= (summon.health[0]-summon.health[1])
                                self.summons[index].health[1] += (summon.health[0]-summon.health[1])
                            else:
                                print(f"{summon.name} was healed by {heal}")
                                self.health[1] -= heal
                                self.summons[index].health[1] += heal
                            print("\nPress space to go back")
                            back = getch()
                            while back != " ":
                                back = getch()
                        elif change == "3":
                            print(f"You have swapped souls with {summon.name}")
                            self.change_soul(summon)
                            self.summons.remove(summon)
                        print("\nPress space to go back")
                        back = getch()
                        while back != " ":
                            back = getch()
                    else:
                        print("\nDo you want to Soul Swap (1)\nHeal summon (2)\n(Press space to go back)")
                        swap = getch()
                        while swap != "1" and swap != "2" and swap != " ":
                            swap = getch()

                        os.system("clear")
                        if swap == "1":
                            print(f"You haved swapped souls with {summon.name}")
                            self.change_soul(summon)
                            self.summons.remove(summon)
                            print("\nPress space to go back")
                            back = getch()
                            while back != " ":
                                back = getch()
                        elif swap == "2":
                            print(f"How much health do you want to give it?")
                            heal = input()
                            while True:
                                try:
                                    heal = int(heal)
                                    break
                                except:
                                    os.system("clear")
                                    print(f"How much health do you want to give it?")
                                    heal = input()
                            os.system("clear")
                            if summon.health[1] + heal > summon.health[0]:
                                print(f"{summon.name} was healed by {summon.health[0]-summon.health[1]}")
                                self.health[1] -= (summon.health[0]-summon.health[1])
                                self.summons[index].health[1] += (summon.health[0]-summon.health[1])
                            else:
                                print(f"{summon.name} was healed by {heal}")
                                self.health[1] -= heal
                                self.summons[index].health[1] += heal
                            print("\nPress space to go back")
                            back = getch()
                            while back != " ":
                                back = getch()

            else:
                print("You have no summons!")

                print("\nPress space to go back")
                back = getch()
                while back != " ":
                    back = getch()
        elif opt == "3":
            os.system("clear")
            if self.inventory:
                item, index = list_select(self.inventory, "\nSelect an item\n(Press space to go back)")
                if item != " ":
                    os.system("clear")
                    print(f"Use {item.name.capitalize()} (1)\nView {item.name.capitalize()} details (2)\nDiscard {item.name.capitalize()} (3)\n(Press space to go back)")
                    manage = getch()
                    if manage != " ":
                        while manage != "1" and manage != "2" and manage == "3":
                            manage = getch()
                        
                        os.system("clear")
                        if manage == "1":
                            if item.type == "Attack":
                                print("Cannot use attack items outside of battle.")
                            elif item.type == "Special":
                                print("Cannot use special items outside of battle.")
                            else:
                                self.use_item(self.inventory.pop(index))
                        elif manage == "2":
                            print(item.show_details())
                        elif manage == "3":
                            print(f"You discarded {self.inventory.pop(index)}")
                        print("\nPress space to go back")
                        back = getch()
                        while back != " ":
                            back = getch()
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
        if player.reputation <= 30 and randint(1,17+(15-player.reputation)) == 1:
            dprint(f'{name}: "Go die in a ditch."')
        else:
            dprint(f'{name}: "{self.intro}"')
            print(f"{name} is offering a {self.reward.name} for {self.cost} health")
            print(f"Current Health: {player.health[1]}/{player.health[0]}\nDo you want to accept (1) or decline (2) or kill (3)")
            option = getch()
            while option != "1" and option != "2" and option != "3":
                option = getch()
            
            os.system("clear")
            if option == "1":
                print("You accepted the offer")
                print(f"+{self.reputation//2} reputation")
                if player.reputation >= 100:
                    player.reputation = 100
                player.health[1] -= self.cost
                player.reputation += self.reputation//2
                player.add_item(self.reward)
            elif option == "2":
                print("You declined the offer")
            elif option == "3":
                print(f"You killed {name}")
                print(f"-{self.reputation//2} reputation")
                player.reputation -= self.reputation//2
                if player.reputation <= 0:
                    player.reputation = 0
                player.add_item(self.reward)
                location.npcList.remove(self)

        return player
