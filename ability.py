class Ability:
    def __init__(self, name:str, multiplier:float, type:str, breakDamage:int, cost:int, recoil: int):
        self.name = name
        self.multiplier = multiplier
        self.type = type
        self.breakDamage = breakDamage
        self.cost = cost
        self.recoil = recoil

    def show_info(self):
        return f"{self.name}\nMultiplier: {self.multiplier*100}%\nType: {self.type}\nBreak Damage: {self.breakDamage}\nSP Cost: {self.cost}\nRecoil: {self.recoil}%"