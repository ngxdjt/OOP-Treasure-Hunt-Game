from location import *
from entities import *
from item import *
from ability import *
from reusable import dprint, space_to_continue
import os
# Remember to pip install the following:
# termcolor, getch, pyfiglet

class Game():
    def __init__(self):
        self.places = []
        self.currentPlace = None

    def setup(self):
        # Starting abilities

        Smack = Ability("Smack", 0.5, "Physical", 5, 5, 0)
        Fireball = Ability("Fireball", 0.8, "Fire", 25, 20, 0)
        FrostBeam = Ability("Frost Beam", 0.7, "Ice", 20, 15, 0)
        Thunderbolt = Ability("Thunderbolt", 0.65, "Lightning", 10, 10, 0)
        StrongAroma = Ability("Strong Aroma", 0.55, "Wind", 5, 15, -2)

        # Middle abilities

        Tackle = Ability("Tackle", 1, "Physical", 15, 15, 0)
        Incinerate = Ability("Incinerate", 1.3, "Fire", 35, 30, 2)
        Cryokinesis = Ability("Cryokinesis", 1.15, "Ice", 30, 20, 0)
        Thunderstorm = Ability("Thunderstorm", 1.1, "Lightning", 30, 15, 0)
        PurifyingWind = Ability("Purifying Wind", 0.9, "Wind", 20, 20, -10)

        # Late abilities

        UnrelentingBarrage = Ability("Unrelenting Barrage", 2.5, "Physical", 50, 50, 15)
        ScorchingRage = Ability("Scorching Rage", 2.2, "Fire", 45, 40, 5)
        ColdShoulder = Ability("Cold Shoulder", 1.75, "Ice", 50, 35, 0)
        ElectrifyingPassion = Ability("Electrifying Passion", 1.55, "Lightning", 40, 20, 0)
        PungentOdour = Ability("Pungent Odour", 1.85, "Wind", 55, 30, 10)

        # Base Enemy (name, health, weaknesses, weaknessBar, attack, speed, SP, abilities, abilityList, exp, lvl)

        # Early enemies (3 Weaknesses, 150 BST, 3 Early Abilities, 2 Middle Abilities, 1 Late Ability)

        Goblin = Enemy("Goblin", 30, ["Physical","Fire","Ice"], 50, 10, 20, 40, [Smack], {1: Smack, 5: StrongAroma, 7: Fireball, 10: Tackle, 20: Incinerate, 27: UnrelentingBarrage}, 100, 1)
        Slime = Enemy("Slime", 60, ["Fire","Ice","Lightning"], 25, 5, 10, 50, [FrostBeam], {1: FrostBeam, 5: Thunderbolt, 10: StrongAroma, 15: PurifyingWind, 24: Thunderstorm, 46: PungentOdour}, 100, 1)

        # Middle enemies (2 Weaknesses, 300 BST, 3 Early Abilities, 3 Middle Abilities, 2 Late Abilities)

        Orc = Enemy("Orc", 125, ["Fire","Wind"], 75, 30, 15, 55, [Smack], {1: Smack, 5: Fireball, 7: StrongAroma, 10: Tackle, 13: Incinerate, 24: PurifyingWind, 32: UnrelentingBarrage, 46: ScorchingRage}, 150, 1)
        Golem = Enemy("Golem", 150, ["Ice","Wind"], 100, 20, 5, 25, [Smack], {1: Smack, 5: Fireball, 10: FrostBeam, 14: Cryokinesis, 25: Incinerate, 30: Thunderstorm, 52: ColdShoulder, 64: UnrelentingBarrage}, 200, 1)
        Elf = Enemy("Elf", 75, ["Lightning","Physical"], 50, 25, 50, 100, [Thunderbolt], {1: Thunderbolt, 5: Fireball, 10: FrostBeam, 20: PurifyingWind, 30: Cryokinesis, 37: Incinerate, 51: ColdShoulder, 66: ElectrifyingPassion}, 150, 1)

        # Late enemies (1 Weakness, 600 BST, 4 Early Abilities, 4 Middle Abilities, 4 Late Abilities)

        Dragon = Enemy("Dragon", 280, ["Ice"], 125, 50, 20, 125, [Fireball], {1: Fireball, 5: FrostBeam, 7: Smack, 10: Thunderbolt, 20: Incinerate, 25: PurifyingWind, 27: Cryokinesis, 30: Thunderstorm, 45: ColdShoulder, 50: ScorchingRage, 53: PungentOdour, 57: ElectrifyingPassion}, 250, 1)
        Phoenix = Enemy("Phoenix", 350, ["Lightning"], 50, 25, 30, 145, [Thunderbolt], {1: Thunderbolt, 5: Fireball, 8: Smack, 10: StrongAroma, 23: Incinerate, 26: Tackle, 32: PurifyingWind, 35: Thunderstorm, 44: ScorchingRage, 49: UnrelentingBarrage, 53: ElectrifyingPassion, 57: PungentOdour}, 225, 1)

        # items

        Potion = Item("potion", "Healing", 50, 0)
        superPotion = Item("super potion", "Healing", 200, 0)
        hyperPotion = Item("hyper potion", "Healing", 500, 0)

        Gummy = Item("gummy", "Attack", 0, 20)
        powderedGummy = Item("powdered gummy", "Attack", 0, 50)
        condensedGummy = Item("condensed gummy", "Attack", 0, 200)

        Pizza = Item("pizza", "Special", 25, 10)
        Banana = Item("banana", "Special", 100, 30)
        blackHole = Item("black hole", "Special", 400, 400)

        # npcs

        PotionSeller = NPC(["John", "Dave", "Hagatha", "Kirsten", "Mitchell"], 50, Potion, 25, "I have some mystery liquid with me")
        DrugDealer = NPC(["Emily", "Keith", "Dawn", "Clarence", "Sebastian"], 25, Gummy, 10, "Want some drugs?")
        Chef = NPC(["Bryson", "Jennie", "Gordon", "James", "Arnold"], 75, Pizza, 12, "I tried really hard to make this")

        betterPotionSeller = NPC(["Phillip", "Aya", "William", "Wojciech", "Zaynah"], 50, superPotion, 50, "Best stuff I could find")
        powderedDrugDealer = NPC(["Liberty", "Valerie", "Steffan", "Izabella", "Dillon"], 25, powderedGummy, 25, "This is the good stuff")
        Monkey = NPC(["Grease", "Cooter", "Beppo", "Takekei", "Brass"], 100, Banana, 40, "OOH OOH AH AH")

        bestPotionSeller = NPC(["Eddie", "Kieran", "Dora", "Iona", "Aaryan"], 75, hyperPotion, 250, "This is a one of the kind")
        condensedDrugDealer = NPC(["Jose", "Myah", "Hashim", "Olivia", "Macauley"], 10, condensedGummy, 100, "I've got the real deal")
        god = NPC(["Andre", "Faye", "Ffion", "Josiah", "Cameron"], 150, blackHole, 200, "I am god")

        # places

        maze1 = Maze(11, [Goblin, Slime], [Potion, Gummy, Pizza], [PotionSeller, DrugDealer, Chef])
        maze2 = Maze(13, [Goblin, Slime, Elf], [Potion, Gummy, Pizza], [PotionSeller, DrugDealer, Chef])
        maze3 = Maze(17, [Goblin, Slime, Elf, Golem], [Potion, superPotion, Gummy, powderedGummy, Pizza, Banana], [PotionSeller, betterPotionSeller, DrugDealer, powderedDrugDealer, Chef, Monkey])
        maze4 = Maze(23, [Elf, Orc, Golem], [superPotion, powderedGummy, Banana], [betterPotionSeller, powderedDrugDealer, Monkey])
        maze5 = Maze(31, [Elf, Orc, Golem, Dragon, Phoenix], [hyperPotion, condensedGummy, Banana], [bestPotionSeller, condensedDrugDealer, god, Monkey])

        colour = ColourSwitch()
        box = BoxPush()
        buckshot = Buckshot()
        slot = Slot()
        maths = Maths()

        # rooms

        mazes = [maze1, maze2, maze3, maze4, maze5]
        minigames = [colour, maths, box, buckshot, slot]
        roomOrder = ["maze","maze","maze","minigame","minigame","minigame","minigame","minigame"]
        shuffle(roomOrder)

        self.places.append(mazes.pop(0))
        for room in roomOrder:
            if room == "maze":
                self.places.append(mazes.pop(0))
            else:
                self.places.append(minigames.pop(0))
        self.places.append(mazes.pop(-1))

    def start(self):
        os.system("clear")
        print(pfg.figlet_format("Labyrinth of the Damned",font="larry3d"))
        print("Press space to start")
        start = getch()
        while start != " ":
            os.system("clear")
            print(pfg.figlet_format("Labyrinth of the Damned",font="larry3d"))
            print("Press space to start")
            start = getch()
        os.system("clear")

        dprint("You are a necromancer wandering down the streets. Such a happy lad you are!")
        dprint("That is until this group of weirdos comes and kidnaps you. Oh no!")
        dprint("So now you are in a labyrinth where you must face off many adversities.")
        dprint("However, the currency down here seems to be life energy which you have the ability to manipulate due to your necromantic abilities.")
        dprint("This is quite convenient, it's almost as if you are the main character!")
        space_to_continue()
        name = input("Enter your name: ")
        player = Player(name, 50, ["Physical", "Fire", "Ice", "Wind", "Lightning"], 100, 25, 15, 25, [Ability("Punch", 0.4, "Physical", 10, 5, 0)])
        os.system("clear")

        print("Press 1 for the tutorial.\nPress 2 to skip the tutorial.")
        tutorial = getch()
        while tutorial != "1" and tutorial != "2":
            print("\033[K\033[F")
            tutorial = getch()
        os.system("clear")

        if tutorial == "1":
            dprint("This labyrinth comprises of two main rooms: mazes and minigames.")
            dprint("To move around, press w (up), a (left), s (down), and d (right).")
            dprint("To manage your player, press q.")
            dprint("To place an explosive, press e.")
            dprint("The following is an example of a maze you might encounter:\n")
            exampleMaze = Maze(11, [], [], [])
            exampleMaze.generate_maze(player)
            exampleMaze.load_enemies()
            exampleMaze.load_items()
            exampleMaze.load_npcs()
            exampleMaze.load_explosives()
            exampleMaze.show_room()
            print()
            dprint(f"{colored("@", 'red')} represents you, the player.")
            dprint(f"{colored("E", 'light_magenta')} represents an enemy. When stepping on an enemy tile, you will be put into combat.")
            dprint(f"{colored("I", 'light_blue')} represents an item. When stepping on an item tile, you pick up the item. Healing items can be used inside or outside of combat. You can only hold a maximum of 20 items.")
            dprint(f"{colored("N", 'light_green')} represents an NPC. When stepping on an NPC tile, you interact with an NPC to exchange items for your health. You can also kill them to gain the item at the expense of your reputation and their existence on the current room.")
            dprint(f"{colored("e", 'light_yellow')} represents an explosive. When stepping on an explosive tile, you gain an explosive. On use you lose 20 health and destory adjacent tiles.\n")

            dprint("The following is an example of a minigame room you may encounter:\n")
            room = [["x", "x", "x", "x", "x"], 
                    [colored("@", 'red'), " ", colored("P", 'light_yellow'), " ", "x"], 
                    ["x", " ", " ", " ", "x"], 
                    ["x", " ", " ", " ", " "], 
                    ["x", "x", "x", "x", "x"]
                ]
            for row in room:
                print(' '.join(row))
            print()
            dprint(f"{colored("P", 'light_yellow')} represents the minigame. Stepping on a minigame tile will start the minigame.")
            dprint(f"You will always be able to skip minigames and move onto the next room, however you will miss out on a few rewards.")
            
            space_to_continue()

            dprint("Let's move onto the combat")
            dprint("You have four main stats: Health, Attack, Speed, and SP.")
            dprint("Health is the amount of damage you can take until you die.")
            dprint("Attack influences your damage.")
            dprint("Speed influences the turn order. Higher speed leads to you starting first in the battle.")
            dprint("SP is what is used when using an ability.")
            dprint("Let's see what ability you have right now!")
            print()
            print(player.abilities[0].show_info())
            print()
            dprint("The multiplier is used to calculate your damage using the formula multiplier*attack")
            dprint("The type influences what weakness damage the ability inflicts. The five weaknesses are Physical, Fire, Ice, Lightning, Wind.")
            dprint("The break damage is how much damage the ability does to the target's weakness bar which can lead to breaks.")
            dprint("Breaking deals 20% of the target's max hp and skips their next turn.")
            dprint("The SP cost is the amount of SP the ability takes to use.")
            dprint("The recoil is the percentage of your max health you lose (or gain if negative) upon using the ability.")
            dprint("If you don't have enough SP when using a move, you will flail instead. Flailing is typeless and has a multiplier of 50% with 10% recoil.")
            print()
            dprint("During you turn you have four actions: attack, wait, rest, use item.")
            dprint("Attacking allows you to use a move on the enemy.")
            dprint("Waiting recovers 33% of your SP.")
            dprint("Resting recovers 66& of your SP, however, you will take 1.5x more damage until your next turn.")
            dprint("Using an item allows you to access your inventory and use an item from it.")
            print()
            dprint("After defeating an enemy, there is a 10% chance of an item dropping and you can choose to either absorb or necromance the enemy.")
            dprint("Absorbing allows you to gain 50% of the enemy's stats and you inherit their weaknesses and you have a 50% chance of gaining each of their abilities.")
            dprint("Necromancing consumes 20% of you max health but in exchange you get a summon with the exact stats of the enemy you just faced.")
            dprint("Summons attack in battle and can gain levels as you fight more enemies.")
            dprint("You may also swap your soul with summons at any time to gain their stats and weaknesses while removing them from your party.")
            
            print("\nPress space to get into the game!")
            opt = getch()
            while opt != " ":
                print("\033[K\033[F")
                opt = getch()
            os.system("clear")
 
        room = 1
        self.currentPlace = self.places[room-1]
        self.places[room-1].visited = True
        secretCondition = []

        if isinstance(self.currentPlace, Maze):
            self.currentPlace.generate_maze(player)
            self.currentPlace.load_enemies()
            self.currentPlace.load_items()
            self.currentPlace.load_npcs()
            self.currentPlace.load_explosives()

        while player.health[1] > 0 and room <= 10:
            os.system("clear")
            print(f"Controls:\nMovement (wasd)\nPlace Explosive (e)\nManage Player (q)\n\nHealth: {player.health[1]}/{player.health[0]}\nExplosives: {player.explosives}\nReputation: {player.reputation}\n")
            self.currentPlace.show_room()
            
            if self.currentPlace.room[-2][-1] == colored("@", 'red') and room < 10:
                os.system("clear")
                print(f"Controls:\nMovement (wasd)\nPlace Explosive (e)\nManage Player (q)\n\nHealth: {player.health[1]}/{player.health[0]}\nExplosives: {player.explosives}\nReputation: {player.reputation}\n")
                self.currentPlace.show_room()
                direction = getch()
                if direction == "d":
                    secretCondition.append(direction)
                    room += 1
                    player.currentPos = [1,0]
                    self.currentPlace = self.places[room-1]
                    self.currentPlace.roomNumber = room
                    if isinstance(self.currentPlace, Maze) and not self.places[room-1].visited:
                        self.currentPlace.generate_maze(player)
                        self.currentPlace.load_enemies()
                        self.currentPlace.load_items()
                        self.currentPlace.load_npcs()
                        self.currentPlace.load_explosives()
                    self.currentPlace.room[player.currentPos[0]][player.currentPos[1]] = colored("@", 'red')
                    self.places[room-1].visited = True
                    continue
                else:
                    secretCondition.append(direction)
                    player.move(direction, self.currentPlace)
                    continue
            
            elif self.currentPlace.room[1][0] == colored("@", 'red') and room > 1:
                os.system("clear")
                print(f"Controls:\nMovement (wasd)\nPlace Explosive (e)\nManage Player (q)\n\nHealth: {player.health[1]}/{player.health[0]}\nExplosives: {player.explosives}\nReputation: {player.reputation}\n")
                self.currentPlace.show_room()
                direction = getch()
                if direction == "a":
                    secretCondition.append(direction)
                    room -= 1
                    self.currentPlace = self.places[room-1]
                    self.currentPlace.roomNumber = room
                    player.currentPos = [self.currentPlace.size-2,self.currentPlace.size-1]
                    self.currentPlace.room[player.currentPos[0]][player.currentPos[1]] = colored("@", 'red')
                    continue
                else:
                    secretCondition.append(direction)
                    player.move(direction, self.currentPlace)
                    continue

            if room == 10:
                start = len(secretCondition)
                if (len(secretCondition) - start) % 15 == 0:
                    self.currentPlace.generate_maze(player)
                    self.currentPlace.load_enemies()
                    self.currentPlace.load_items()
                    self.currentPlace.load_npcs()
                    self.currentPlace.load_explosives()

            direction = getch()
            if direction == "e":
                player.place_explosive(self.currentPlace)
            elif direction == "q":
                player.manage()
            elif direction in ["w","a","s","d"]:
                secretCondition.append(direction)
                player.move(direction, self.currentPlace)

        os.system("clear")
        if player.health[1] <= 0:
            dprint("You died")
        elif player.reputation >= 50 and "wwssadad" not in ''.join(secretCondition):
            dprint("That's it! The exit!")
            dprint("What is that around the corner?")
            dprint("A chest! Wow! You are so excited!")
            dprint("You open the chest and it starts talking. Weird world. Says you the necromancer.")
            dprint('Chest: "Oh so belated one, please accept this gift before you leave."')
            dprint("Who are you to reject a gift from a talking treasure chest so of course you accept it.")
            dprint("You walk out of the labyrinth with the power of the gods.")

            space_to_continue()

            print(pfg.figlet_format("Good Ending",font="larry3d"))
        elif player.reputation < 50 and "wwssadad" not in ''.join(secretCondition):
            dprint("That's it! The exit!")
            dprint("What is that around the corner?")
            dprint("A chest! Wow! You are so excited!")
            dprint("You open the chest and it starts talking. Weird world. Says you the necromancer.")
            dprint('Chest: "Oh so fiendish one, please accept this gift before you leave."')
            dprint("Who are you to reject a gift from a talking treasure chest so of course you accept it.")
            dprint("However, it was a trap!")
            dprint("Shackled down with the light of the outside world within your reach.")
            dprint("Guess this is it.")
            dprint("Forever until the end of time, until the heat death of the universe, you stay lamenting.")

            space_to_continue()

            print(pfg.figlet_format("Bad Ending",font="larry3d"))
        else:
            dprint("That's it! The exit!")
            dprint("What is that around the corner?")
            dprint("A chest! Wow! You are so excited!")
            dprint("You open the chest and it starts talking. Weird world. Says you the necromancer.")
            dprint('Chest: "Oh so transcended one, please accept this gift before you leave."')
            dprint("Who are you to reject a gift from a talking treasure chest so of course you accept it.")
            dprint('Chest: "Look behind you"')
            dprint("Another chest appears.")
            dprint("Bleep. Bleep. Bleep.")
            dprint("SO MANY CHESTS.")
            dprint("Perhaps it was fate. Perhaps it was destiny.")
            dprint("Those weirdos. They had a purpose, a reason.")
            dprint("Swimming in treasure chests, this was your dream.")
            dprint("Consumed by bliss, you drown in your own saliva.")

            space_to_continue()

            print(pfg.figlet_format("Secret Ending",font="larry3d"))


def main():
    game = Game()
    game.setup()
    game.start()

if __name__ == '__main__':
    main()