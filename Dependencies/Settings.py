import pygame
import ctypes


class GameSettings():
    def __init__(self):
        self.gameClock = pygame.time.Clock()

        user32 = ctypes.windll.user32
        self.screenResolution = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

        self.getWindowSize()

        self.framesPerSecond = 30
        self.scaleFactor = self.blockSize/40

        self.level = 0
        self.day = 1
        self.movesLeft = 10

        """settings.display
        settings.grid
        settings.hero
        settings.gameCharacters
        settings.statusPanel
        are all defined for this object"""

    def newDay(self):
        self.day += 1
        self.hero.moves = self.hero.movesPerDay

        self.Characters.deleteMonsters()

        if len(self.gameCharacters.monsters) == 0:
            # Spawn a monster
            self.Characters.spawnMonster(self.level)
            self.grid.drawGrid()
        else:
            self.grid.copyGrid()
            self.Characters.monsterMove(self.grid)

    def moved(self):
        self.hero.moved()
        if self.hero.moves == 0:
            pygame.event.wait()
            # Update stats panel here
            self.statusPanel.blitme()
            pygame.display.update()
            self.newDay()
            pygame.event.get()

    def set_moves(self, n):
        self.hero.moves = n

    def getWindowSize(self):
        # Get the screen resolution
        self.height = self.screenResolution[1]

        # Round height values down to the nearest multiple of 10
        self.height *= 0.9
        self.height = (int(self.height/10)) * 10

        # Store the final window size
        if self.height >= 940:
            # Store the final window size
            self.windowSize = (1240, 940)   # (Width, Height)
            self.blockSize = 40
            self.status_panel_space = 100
        else:
            # Assign space for grid and space for status panel
            self.grid_space = self.height * 0.9
            self.status_panel_space = self.height - self.grid_space

            # Calculate the size that each grid block should be
            self.blockSize = int(self.grid_space / 21)
            self.width = self.blockSize * 31
            self.windowSize = (self.width, self.height)

    def addCharacters(self, Characters):
        self.Characters = Characters
