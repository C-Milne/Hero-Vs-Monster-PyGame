import pygame
import sys
import os
from Dependencies.Settings import GameSettings
from Dependencies.Maze import maze
from Dependencies.Hero import hero
from Dependencies.status_bar import StatusPanel
from Dependencies.GameCharacters import Game_characters


class BackGround(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Dependencies/Images/BlackBackground.png')
        self.image = pygame.transform.scale(self.image, (1300, 1000))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = [0,0]


def runGame(settings):
    # Main game loop
    while True:
        settings.gameClock.tick(settings.framesPerSecond)

        for event in pygame.event.get():
            # Check if game is being Quit
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    # Move the hero up one block, if the block is clear
                    Hero.move(gameGrid, "UP", gameDisplay, settings)
                elif event.key == pygame.K_DOWN:
                    Hero.move(gameGrid, "DOWN", gameDisplay, settings)
                elif event.key == pygame.K_LEFT:
                    Hero.move(gameGrid, "LEFT", gameDisplay, settings)
                elif event.key == pygame.K_RIGHT:
                    Hero.move(gameGrid, "RIGHT", gameDisplay, settings)

        statusBar.blitme()
        """Update all sprites"""
        pygame.display.update()     # Load the new frame


if __name__ == "__main__":
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (10,40)
    # Initialize pygame
    pygame.init()

    settings = GameSettings()   # Initialize game settings

    # Set window size
    gameDisplay = pygame.display.set_mode((settings.windowSize[0], settings.windowSize[1]))
    gameDisplay.fill([255, 255, 255])   # Fill game display white

    backGround = BackGround()   # Set the BackGround
    gameDisplay.blit(backGround.image, backGround.rect)  # Draw onto the window

    pygame.display.set_caption("Hero vs Monster")   # Set window title

    # Generate Maze
    gameGrid = maze(settings.blockSize, gameDisplay, backGround)

    # Spawn Hero
    Hero = hero(gameGrid)

    # Draw Grid
    gameGrid.drawGrid()

    # Add accessibility to hero in the settings class
    settings.hero = Hero

    # store grid in settings
    settings.grid = gameGrid

    # Create object to store game characters
    Characters = Game_characters(gameGrid, settings.windowSize, settings, Hero, gameDisplay)
    settings.addCharacters(Characters)

    # Draw Grid
    gameGrid.drawGrid()

    # Add display and grid to settings for extra accessibility
    settings.display = gameDisplay
    settings.gameCharacters = Characters

    # Initialise Status bar
    statusBar = StatusPanel(settings.windowSize[1] - settings.status_panel_space, settings.scaleFactor, gameDisplay,
                            settings, Hero, settings.windowSize)

    settings.statusPanel = statusBar

    # Draw status bar
    statusBar.blitme()

    """Run the game"""
    runGame(settings)
