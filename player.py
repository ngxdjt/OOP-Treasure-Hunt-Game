class Player():
    def __init__(self, given_name):
        self.name = given_name
        self.health = 100
        self.energy = 100
        self.inventory_max_weight = 50
        self.inventory = []
        # add more atributes as needed

    def calculate_inventory_size(self):
        # write code here
        pass

    def add_item(self, item_instance):
        if self.calculate_inventory_size() > self.inventory_max_weight:
            self.inventory.append(item_instance)
        else:
            print("Your inventory is full...")

    def use_item(self, item_instance):
        if item_instance.type == "food":
            self.energy += 50
        elif item_instance.type == "medicine":
            self.health += 50
        # add more code here

    # add more methods as needed
