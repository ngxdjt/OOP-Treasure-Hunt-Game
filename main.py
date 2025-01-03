from location import *
from entities import *
from item import *
from ability import *
from delayed_print import dprint
import os

class Game():
    def __init__(self):
        self.places = []
        self.currentPlace = None

    def setup(self):
        # Starting abilities

        Smack = Ability("Smack", 0.3, "Physical", 5, 5, 0)
        Fireball = Ability("Fireball", 0.8, "Fire", 25, 20, 0)
        FrostBeam = Ability("Frost Beam", 0.7, "Ice", 20, 15, 0)
        Thunderbolt = Ability("Thunderbolt", 0.65, "Lightning", 10, 10, 0)
        StrongAroma = Ability("Strong Aroma", 0.55, "Wind", 5, 15, -5)

        # Middle abilities

        Tackle = Ability("Tackle", 1, "Physical", 15, 15, 0)
        Incinerate = Ability("Incinerate", 1.3, "Fire", 35, 30, 5)
        Cryokinesis = Ability("Cryokinesis", 1.15, "Ice", 30, 20, 0)
        Thunderstorm = Ability("Thunderstorm", 1.1, "Lightning", 30, 15, 0)
        PurifyingWind = Ability("Purifying Wind", 0.9, "Wind", 20, 20, -15)

        # Late abilities

        UnrelentingBarrage = Ability("Unrelenting Barrage", 2.5, "Physical", 50, 50, 25)
        ScorchingRage = Ability("Scorching Rage", 2.2, "Fire", 45, 40, 10)
        ColdShoulder = Ability("Cold Shoulder", 1.75, "Ice", 50, 35, 0)
        ElectrifyingPassion = Ability("Electrifying Passion", 1.55, "Lightning", 40, 20, 0)
        PungentOdour = Ability("Pungent Odour", 1.85, "Wind", 55, 30, 15)

        # Base Enemy (name, health, weaknesses, weaknessBar, attack, speed, SP, abilities, abilityList, exp, lvl)

        # Early enemies (3 Weaknesses, 150 BST, 3 Early Abilities, 2 Middle Abilities, 1 Late Ability)

        Goblin = Enemy("Goblin", 25, ["Physical","Fire","Ice"], 50, 15, 20, 40, [Smack], {1: Smack, 5: StrongAroma, 7: Fireball, 10: Tackle, 20: Incinerate, 27: UnrelentingBarrage}, 100, 1)
        Slime = Enemy("Slime", 60, ["Fire","Ice","Lightning"], 25, 10, 5, 50, [FrostBeam], {1: FrostBeam, 5: Thunderbolt, 10: StrongAroma, 15: PurifyingWind, 24: Thunderstorm, 46: PungentOdour}, 100, 1)

        # Middle enemies (2 Weaknesses, 300 BST, 3 Early Abilities, 3 Middle Abilities, 2 Late Abilities)

        Orc = Enemy("Orc", 125, ["Fire","Wind"], 75, 30, 15, 55, [Smack], {1: Smack, 5: Fireball, 7: StrongAroma, 10: Tackle, 13: Incinerate, 24: PurifyingWind, 32: UnrelentingBarrage, 46: ScorchingRage}, 150, 1)
        Golem = Enemy("Golem", 150, ["Ice","Wind"], 100, 20, 5, 25, [Smack], {1: Smack, 5: Fireball, 10: FrostBeam, 14: Cryokinesis, 25: Incinerate, 30: Thunderstorm, 52: ColdShoulder, 64: UnrelentingBarrage}, 200, 1)
        Elf = Enemy("Elf", 75, ["Lightning","Physical"], 50, 25, 50, 100, [Thunderbolt], {1: Thunderbolt, 5: Fireball, 10: FrostBeam, 20: PurifyingWind, 30: Cryokinesis, 37: Incinerate, 51: ColdShoulder, 66: ElectrifyingPassion}, 150, 1)

        # Late enemies (1 Weakness, 600 BST, 4 Early Abilities, 4 Middle Abilities, 4 Late Abilities)

        Dragon = Enemy("Dragon", 280, ["Ice"], 125, 50, 20, 125, [Fireball], {1: Fireball, 5: FrostBeam, 7: Smack, 10: Thunderbolt, 20: Incinerate, 25: PurifyingWind, 27: Cryokinesis, 30: Thunderstorm, 45: ColdShoulder, 50: ScorchingRage, 53: PungentOdour, 57: ElectrifyingPassion}, 250, 1)
        Phoenix = Enemy("Phoenix", 350, ["Lightning"], 50, 25, 30, 145, [Thunderbolt], {1: Thunderbolt, 5: Fireball, 8: Smack, 10: StrongAroma, 23: Incinerate, 26: Tackle, 32: PurifyingWind, 35: Thunderstorm, 44: ScorchingRage, 49: UnrelentingBarrage, 53: ElectrifyingPassion, 57: PungentOdour}, 225, 1)

        # items

        Potion = Item("potion", "healing", 50, 0)
        superPotion = Item("super potion", "healing", 200, 0)
        hyperPotion = Item("hyper potion", "healing", 500, 0)

        Gummy = Item("gummy", "attack", 0, 20)
        powderedGummy = Item("powdered gummy", "attack", 0, 50)
        condensedGummy = Item("condensed gummy", "attack", 0, 200)

        Pizza = Item("pizza", "special", 25, 10)
        Banana = Item("banana", "special", 100, 30)
        blackHole = Item("black hole", "special", 400, 400)

        # npcs

        PotionSeller = NPC(["John", "Dave", "Hagatha", "Kirsten", "Mitchell"], 50, Potion, 25, "I have some mystery liquid with me")
        DrugDealer = NPC(["Emily", "Keith", "Dawn", "Clarence", "Sebastian"], 25, Gummy, 10, "Want some drugs?")
        Chef = NPC(["Bryson", "Jennie", "Gordon", "James", "Arnold"], 75, Pizza, 12, "I tried really hard to make this")

        betterPotionSeller = NPC(["Phillip", "Aya", "William", "Wojciech", "Zaynah"], 50, superPotion, 50, "Best stuff I could find")
        powderedDrugDealer = NPC(["Liberty", "Valerie", "Steffan", "Izabella", "Dillon"], 25, powderedGummy, 25, "This is the good stuff")
        Monkey = NPC(["Grease", "Cooter", "Beppo", "Takekei", "Brass"], 100, Banana, 40, "OOH OOH AH AH")

        bestPotionSeller = NPC(["Eddie", "Kieran", "Dora", "Iona", "Aaryan"], 75, hyperPotion, 250, "This is a one of the kind")
        condensedDrugDealer = NPC(["Jose", "Myah", "Hashim", "Olivia", "Macauley"], 10, condensedGummy, 100, "I've got the real deal")
        god = NPC(["Andre", "Faye", "Ffion", "Katie", "Cameron"], 150, blackHole, 200, "I am god")

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
        minigames = [colour, box, buckshot, slot, maths]
        roomOrder = ["maze","maze","maze","maze","maze","minigame","minigame","minigame","minigame","minigame"]
        shuffle(roomOrder)
        shuffle(minigames)

        for room in roomOrder:
            if room == "maze":
                self.places.append(mazes.pop(0))
            else:
                self.places.append(minigames.pop(0))

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
        dprint("However, the currency down here seems to be life energy which you have the ability to manipulate due to your necromatic abilities.")
        dprint("This is quite convenient, it's almost as if you are the main character!")
        print("\nPress space to continue")
        opt = getch()
        while opt != " ":
            print("\033[K\033[F")
            opt = getch()
        os.system("clear")
        name = input("Enter your name: ")
        player = Player(name, 100, ["Physical", "Fire", "Ice", "Wind", "Lightning"], 100, 10, 20, 100, [Ability("Punch", 0.5, "Physical", 10, 10, 0)])
        os.system("clear")

        print("Press 1 for the tutorial. Press 2 to skip it.")
        tutorial = getch()
        while tutorial != "1" and tutorial != "2":
            print("\033[K\033[F")
            tutorial = getch()
        os.system("clear")

        if tutorial == "1":
            dprint("This labyrinth comprises of two main rooms: mazes and minigames.")
            dprint("The following is an example of a maze you might encounter:\n")
            exampleMaze = Maze(11, [], [], [])
            exampleMaze.generate_maze(player)
            exampleMaze.load_enemies()
            exampleMaze.load_items()
            exampleMaze.load_npcs()
            exampleMaze.show_room()
            print()
            dprint(f"The {colored("@", 'red')} represents you, the player.")
            dprint(f"The {colored("E", 'light_magenta')} represents an enemy. When killing an enemy, you can either absorb or necromance it.")
            dprint(f"The {colored("I", 'light_blue')} represents an item. You can pick up and use items inside or outside of battle. You can only hold a maximum of 20 items.")
            dprint(f"The {colored("N", 'light_green')} represents an NPC. NPCs exchange items for your health. You can also kill them to gain the item at the expense of your reputation.\n")

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
            dprint(f"The {colored("@", 'red')} again represents you, the player.")
            dprint(f"The {colored("P", 'light_yellow')} represents the tile you step on to start the minigame.")
            dprint(f"You will always be able to skip minigames and move onto the next room, however you may miss out on a few rewards.")
            
            print("\nPress space to continue")
            opt = getch()
            while opt != " ":
                print("\033[K\033[F")
                opt = getch()
            os.system("clear")

            dprint("Let's move onto the combat")
            dprint("You have four main stats: Health, Attack, Speed, and SP.")
            dprint("Health is the amount of damage you can take until you die.")
            dprint("Attack is what influences your damage and is multiplied with the multiplier of your attack.")
            dprint("Speed influences the turn order. Higher speed leads to you starting first in the battle.")
            dprint("Let's see what move you have right now!")
            print()
            print(player.abilities[0].show_info())
            print()
            dprint("The multiplier is used to calculate your damage using the formula multiplier*attack")
            dprint("The type influences what weakness damage the ability inflicts. The five weaknesses are Physical, Fire, Ice, Lightning, Wind.")
            dprint("The break damage is how much damage the ability does to the target's weakness bar which can lead to breaks.")
            dprint("The SP cost is the amount of SP the ability takes to use.")
            dprint("The recoil is the percentage of your max health you lose (or gain if negative) upon using the ability.")
            
            print("\nPress space to continue")
            opt = getch()
            while opt != " ":
                print("\033[K\033[F")
                opt = getch()
            os.system("clear")
        elif tutorial == "2":
            pass





game = Game()
game.start()