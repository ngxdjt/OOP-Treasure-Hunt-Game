from location import *
from entities import *
from item import *
from ability import *
import os

class Game():
    def __init__(self):
        self.currentPlace = None
        self.nextPlace = None

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

        gummy = Item("gummy", "attack", 0, 20)
        powderedGummy = Item("powdered gummy", "attack", 0, 50)
        condensedGummy = Item("condensed gummy", "attack", 0, 200)

        pizza = Item("pizza", "special", 25, 10)
        banana = Item("banana", "special", 100, 30)
        blackHole = Item("black hole", "special", 400, 100)

        # places

        
        # npcs


    def start(self):
        print("Welcome to my game...")
        print("Storyline...")
        name = input("Enter player name: ")
        player = Player(name)

        print("You are currently in " + self.current_place.name)
        self.current_place.show_next_places()
        opt = input("""
What would you like to do?
1. Go to a place
2. Pickup item
3. Check inventory
etc.      
""")
        if opt == "1":
            # add code
            pass
        elif opt == "2":
            # add code
            pass
        elif opt == "3":
            # add code
            pass
            
