import random


class Goblin:
    def __init__(self, coords):
        self.visited = False
        self.chooseClass()
        self.coords = coords

    def chooseClass(self):
        """There are different types of Goblins:
        Health goblins - Increase hero health
        SmokeBombs goblins - Gives Smoke Bomb - if hero wins rock, paper, sissors
        Choice goblins - Hero can choose what ability the goblins has"""

        possibleTypes = ["Health", "Smoke", "Choice"]
        self.ability = possibleTypes[random.randint(0,2)]

    def get_coords(self):
        return self.coords
