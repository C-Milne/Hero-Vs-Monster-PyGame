import time
import pygame
import random
from Dependencies.Search_Algorithm.Dijsktra import Dijkstra


class Monster():
    def __init__(self, coords, gameCharacters, level):
        self.X = coords[0]
        self.Y = coords[1]
        self.gameCharacters = gameCharacters
        self.alive = True

        self.health = int(150 * (1 + level/10))

        self.damage = 35
        self.moves = 0

    def search(self, grid):
        self.route = Dijkstra(grid.grid_copy, (self.X, self.Y))

        # Move the monster
        self.moves = len(self.route.steps[:6])
        self.stepsToTake = self.route.steps[::-1]
        for index in self.stepsToTake[:6]:
            if grid.grid[self.Y][self.X] == "G/M":
                grid.grid[self.Y][self.X] = "G"
            elif grid.grid[self.Y][self.X] == "C/M":
                grid.grid[self.Y][self.X] = "C"
            else:
                grid.grid[self.Y][self.X] = 0

            self.X, self.Y = index.coords[0], index.coords[1]

            if grid.grid[self.Y][self.X] == "H":
                 self.gameCharacters.HeroFoundMonster(self.X, self.Y)
            elif grid.grid[self.Y][self.X] == "G":
                grid.grid[self.Y][self.X] = "G/M"
            elif grid.grid[self.Y][self.X] == "C":
                grid.grid[self.Y][self.X] = "C/M"

            if self.alive and grid.grid[self.Y][self.X] != "H/M":
                if grid.grid[self.Y][self.X] != "G/M" and grid.grid[self.Y][self.X] != "C/M" :
                    grid.grid[self.Y][self.X] = "M"
                grid.drawGrid()
                self.gameCharacters.settings.statusPanel.blitme()
                pygame.display.update()
                time.sleep(0.2)
            self.moves -= 1

    def checkCoords(self):
        return str((self.X, self.Y))

    def takeDamage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.X = None
            self.Y = None

    def battle_turn(self):
        # Monster always hits the hero
        # Monster has a change on getting slightly more damage
        # 60% change of getting a critial hit
        if random.randint(1, 100) >= 60:
            return int(self.damage * 1.30)
        else:
            return self.damage
