class Place():
    def __init__(self, given_name, given_size, locked=False):
        # locked=False means that the locked parameter will be False by default if not provided.
        self.name = given_name
        self.size = given_size
        self.locked = locked
        self.next_places = []
        self.items = []
        # add more atributes as needed

    def add_next_place(self, place_instance):
        self.next_places.append(place_instance)

    def add_item(self, item_instance):
        # add code here
        pass

    def show_next_places(self):
        print("The possible places you can go to are: ")
        for place in self.next_places:
            # remember that next_places is a list of Place instances hence why we can use place.name
            print(place.name)

    # add more methods as needed
