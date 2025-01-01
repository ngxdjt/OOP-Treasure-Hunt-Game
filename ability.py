class Ability:
    def __init__(self, name:str, multiplier:float, type:str, breakDamage:int, cost:int):
        self.name = name
        self.multiplier = multiplier
        self.type = type
        self.breakDamage = breakDamage
        self.cost = cost