from random import shuffle, choice

class Location():
    def __init__(self, type:str, size:int):
        self.type = type
        self.size = size
        self.room = []

    def generate_maze(self, player):
        pass

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