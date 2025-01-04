class Item():
    def __init__(self, name:str, type:str, healing:int, attack:int):
        self.name = name
        self.type = type
        self.healing = healing
        self.attack = attack

    def show_details(self):
        if self.type == "Healing":
            return f"{self.name.capitalize()}\nType: {self.type}\nHealing: {self.healing}"
        elif self.type == "Attack":
            return f"{self.name.capitalize()}\nType: {self.type}\nAttack: {self.attack}"
        else:
            return f"{self.name.capitalize()}\nType: {self.type}\nHealing: {self.healing}\nAttack: {self.attack}"