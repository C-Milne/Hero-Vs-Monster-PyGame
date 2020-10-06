import pygame
import random


class hero(pygame.sprite.Sprite):
    def __init__(self, gameGrid):
        pygame.sprite.Sprite.__init__(self)

        while True:
            # Spawn the hero on a random open block
            self.X = random.randint(1, len(gameGrid.grid[1]) - 2)
            self.Y = random.randint(1, len(gameGrid.grid) -2)

            # Write the Hero's co-ordinates to the game grid
            if gameGrid.grid[self.Y][self.X] == 0:
                gameGrid.grid[self.Y][self.X] = "H"
                break

        self.maxHealth = 100
        self.health = 100
        self.smokeBombs = 1
        self.hitChance = 50
        self.damage = 50
        self.alive = True
        self.moves = 10
        self.maxMoves = 5
        self.movesPerDay = 2

    def move(self, gameGrid, direction, gameDisplay, settings):
        next_block = None   # Initialise next_block
        current_block = gameGrid.grid[self.Y][self.X]
        wall = False

        if direction == "UP" and gameGrid.grid[self.Y - 1][self.X] != 1:
            new_x = self.X
            new_y = self.Y - 1

        elif direction == "DOWN" and gameGrid.grid[self.Y + 1][self.X] != 1:
            new_x = self.X
            new_y = self.Y + 1

        elif direction == "LEFT" and gameGrid.grid[self.Y][self.X - 1] != 1:
            new_x = self.X - 1
            new_y = self.Y

        elif direction == "RIGHT" and gameGrid.grid[self.Y][self.X + 1] != 1:
            new_x = self.X + 1
            new_y = self.Y
        else:
            wall = True

        if not wall:
            next_block = gameGrid.grid[new_y][new_x]

        # If hero has moved (Not hit a wall)
        if next_block is not None:
            # Check if hero has met a goblin
            if next_block == 'G':
                settings.Characters.HeroFoundGoblin(new_x, new_y)
            elif next_block == 'M' or next_block == 'G/M' or next_block == 'C/M':
                settings.Characters.HeroFoundMonster(new_x, new_y)
                next_block = gameGrid.grid[new_y][new_x]

            elif next_block == 'C':
                settings.Characters.HeroFoundChest(new_x, new_y)

            if current_block == 'H/M':
                gameGrid.grid[self.Y][self.X] = 'M'
            else:
                gameGrid.grid[self.Y][self.X] = 0

            self.Y, self.X = new_y, new_x
            if next_block != 'H/M':
                gameGrid.grid[self.Y][self.X] = 'H'
            gameGrid.drawGrid()
            settings.moved()

    def lightAttack(self):
        # Give boost to the chance of light attack hitting monster
        # Give light attack no damage boost
        chance = self.hitChance + (self.hitChance * 1.25)
        if chance >= random.randint(1,100):
            return self.damage
        else:
            return 0

    def heavyAttack(self):
        # Give no boost to chance of heavy attack hitting monster
        # Give heavy attack a damage boost
        damage = self.damage + (self.damage * 1.25)
        if self.hitChance >= random.randint(1,100):
            return damage
        else:
            return 0

    def useSmokeBomb(self):
        self.smokeBombs -= 1
        # Give hero 10 moves
        self.moves = 15

    def checkSmokeBombs(self):
        return self.smokeBombs

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.alive = False

    def moved(self):
        self.moves -= 1

    def giveSmokeBomb(self):
        self.smokeBombs += 1

    def gainedMaxHealth(self):
        """Called if hero meets Health goblin and wins the game
        Hero regains max health (100)
        If hero already has max health the hero's max is increased by 25"""
        if self.maxHealth == self.health:
            self.maxHealth += 25
            self.health += 25
        else:
            self.health = self.maxHealth

    def buffDamage(self, v):
        """Called from chest.interaction()
        Increase the hero's damage, by the given amount"""
        self.damage += v

    def buffChance(self, v):
        """Called from chest.interaction()
        Increase the hero's hit chance by the given amount
        Don't let the hit chance exceed 100%"""
        self.hitChance += v
        if self.hitChance > 100:
            self.hitChance = 100

    def defeatedMonster(self):
        """Called from GameCharacters.HeroFoundMonster()
        Increase the amount of moves the hero gets per day
        Don't increase amount of moves more than self.maxMoves"""
        if self.movesPerDay < self.maxMoves:
            self.movesPerDay += 1

