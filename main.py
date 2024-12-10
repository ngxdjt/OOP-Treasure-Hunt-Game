from place import Place
from player import Player
from item import Item

class Game():
    def __init__(self):
        self.current_place = None
        # add more atributes as needed

    def setup(self):
        # here you will setup your Game
        # places
        home = Place('Home', 10)
        bedroom = Place('Bedroom', 5)
        bathroom = Place('Bathroom', 4, True) # bathroom is locked
        garden = Place('Garden', 15)
        shed = Place('Shed', 3)
        cave = Place('Cave', 50)
        
        home.add_next_place(garden)
        home.add_next_place(bedroom)
        bedroom.add_next_place(bathroom)
        garden.add_next_place(shed)
        # etc. 
        
        # items
        hammer = Item('Hammer')
        pen = Item('Pen')

        home.add_item(hammer)
        bedroom.add_item(pen)

        # home will be our starting place
        self.current_place = home
        
        # finish the setup function...

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
            
