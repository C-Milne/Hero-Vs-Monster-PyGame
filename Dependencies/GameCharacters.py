import random
import pygame
import timeit
import sys
from Dependencies.Monster import Monster
from Dependencies.Goblin import Goblin
from Dependencies.Dialogbox import DialogBox
from Dependencies.Interactions.Battle import BattleScene
from Dependencies.Interactions.Goblin_Interaction_Scenes.Goblin_Interaction_Start import Goblin_Interaction_Start
from Dependencies.Interactions.GameOver import GameOver
from Dependencies.Chest import Chest


class Game_characters(pygame.sprite.Sprite):
    """Class to store monsters and Goblins"""
    def __init__(self, map, windowSize, settings, hero, gameDisplay):
        self.map = map
        self.windowSize = windowSize    # (Width, Height)
        self.settings = settings
        self.dialogBox = DialogBox(self.windowSize)
        self.gameDisplay = gameDisplay

        self.hero = hero
        self.goblins = {}
        self.monsters = {}
        self.monsters_remove_list = []

        pygame.sprite.Sprite.__init__(self)
        # Store the back ground Image here, for use in the interaction scenes
        self.backGround_image = pygame.image.load('Dependencies/Images/BlackBackground.png')
        self.backGround_image = pygame.transform.scale(self.backGround_image, (1300, 1000))

        self.backGround_image2 = pygame.image.load('Dependencies/Images/WhiteBackground.png')
        self.backGround_image2 = pygame.transform.scale(self.backGround_image2, (1300, 1000))

        self.heroBattle_image = pygame.image.load('Dependencies/Images/battleHero.png')
        self.heroBattle_image = pygame.transform.scale(self.heroBattle_image,(int(self.windowSize[0] * 0.3), int(self.windowSize[1] * 0.4)))
        self.heroBattle_imageRect = self.heroBattle_image.get_rect()
        self.heroBattle_imageRect.top = 0.3 * self.windowSize[1]
        self.heroBattle_imageRect.left = 0.05 * self.windowSize[0]

        self.monster_image = pygame.image.load('Dependencies/Images/battleMonster.jpg')
        self.monster_image = pygame.transform.scale(self.monster_image, (int(self.windowSize[0] * 0.3), int(self.windowSize[1] * 0.5)))
        self.monster_imageRect = self.monster_image.get_rect()
        self.monster_imageRect.top = 0.01 * self.windowSize[1]
        self.monster_imageRect.right = 0.95 * self.windowSize[0]

        self.interactionButton = pygame.image.load('Dependencies/Images/Button.png')
        self.interactionButton = pygame.transform.scale(self.interactionButton, (int(self.windowSize[0] * 0.25), int(self.windowSize[1] * 0.25)))

        self.Font = pygame.font.SysFont("Times New Roman", 30, bold=True)

        # Spawn goblins
        for index in range(5):
            self.spawnGoblin()

        self.chests = {}
        # Spawn chests
        for index in range(3):
            self.spawnChest()

    def spawnChest(self):
        coords = self.find_spawn_location("C")
        if coords is not None:
            self.chests[str(coords)] = Chest(coords, self.gameDisplay, self.windowSize, self.Font)

    def HeroFoundChest(self, X, Y):
        coords = str((X, Y))
        self.chests[coords].interaction(self.hero)

    def spawnGoblin(self):
        coords = self.find_spawn_location("G")
        if coords is not None:
            self.goblins[str(coords)] = Goblin(coords)

    def spawnMonster(self, level=0):
        coords = self.find_spawn_location("M")
        self.monsters[str(len(self.monsters))] = Monster(coords, self, level)

    def monsterMove(self, grid):
        for index in self.monsters.keys():
            self.monsters[index].search(grid)
        self.deleteMonsters()

    def deleteMonsters(self):
        # Delete monsters that have been defeated by the hero
        for i in self.monsters_remove_list:
            del self.monsters[i]
        self.monsters_remove_list = []

    def find_spawn_location(self, assignedLetter):
        """Only continue if free spots on grid - always leave 1 spot for monster"""
        if self.settings.grid.count_free_spaces() <= 1 and assignedLetter != "M":
            return None
        else:
            while True:
                # Spawn the character on a random open block
                X = random.randint(1, len(self.map.grid[1]) - 2)
                Y = random.randint(1, len(self.map.grid) - 2)

                # Write the Hero's co-ordinates to the game grid
                if self.map.grid[Y][X] == 0:
                    self.map.grid[Y][X] = assignedLetter
                    break
            return (X,Y)

    def HeroFoundGoblin(self, X, Y):
        coords = str((X, Y))
        Goblin_Interaction_Start(self.settings.display, self.windowSize, self.Font, self.goblins[coords], self.hero)
        pygame.event.clear()

    def move_goblin(self, goblin):
        del self.goblins[goblin.get_coords()]
        new_coords = self.find_spawn_location("G")
        goblin.coords = new_coords
        self.goblins[str(new_coords)] = goblin

    def move_chest(self, chest):
        del self.chests[chest.coords]
        new_coords = self.find_spawn_location("C")
        chest.coords = new_coords
        self.chests[str(new_coords)] = chest

    def HeroFoundMonster(self, X, Y):
        coords = str((X, Y))
        # Set grid block appropriately
        self.map.grid[Y][X] = "H/M"

        # Check if goblin is also on this block
        # If so goblin runs away and goes to a new block
        if self.map.grid[Y][X] == "G/M":
            # Move the goblin
            self.move_goblin(self.goblins[coords])
        elif self.map.grid[Y][X] == "C/M":
            # Move the chest
            self.move_chest(self.chests[coords])

        for index in self.monsters.keys():
            if self.monsters[str(index)].checkCoords() == coords:
                battle = BattleScene(self.hero, self.monsters[str(index)], self.settings.display, self.heroBattle_image,
                                     self.heroBattle_imageRect, self.monster_image, self.monster_imageRect,
                                     self.backGround_image2, self.windowSize, self.interactionButton, self.Font, self)
                result = battle.outcome
                break
        if result == "Monster":
            # Show game over scene
            GameOver(self.settings.display,  self.windowSize, self.settings.level)
        elif result == "Hero":
            # Remove monster from self.monsters
            self.monsters_remove_list.append(index)
            # Remove monster from map
            # Show hero on map
            self.map.set_coord(X, Y, "H")

            # Spawn 3 more goblins
            for i in range(3):
                self.spawnGoblin()

            # Spawn 1 more chest
            self.spawnChest()

            # Increase level by 1
            self.settings.level += 1

            # Give hero 6 more moves
            self.hero.moves += 6
            self.hero.defeatedMonster()

            self.map.drawGrid()
            pygame.display.update()
        else:
            # Result == "Smoke"
            self.map.drawGrid()
            pygame.display.update()
        pygame.event.clear()
        return result

    def wait(self, t):
        start = timeit.default_timer()
        while timeit.default_timer() - start < t:
            for event in pygame.event.get():
                # Check if game is being Quit
                if event.type == pygame.QUIT:
                    sys.exit()

    def getMonster(self):
        keys = list(self.monsters.keys())
        if len(keys) == 0:
            return None
        else:
            return self.monsters[keys[0]]
