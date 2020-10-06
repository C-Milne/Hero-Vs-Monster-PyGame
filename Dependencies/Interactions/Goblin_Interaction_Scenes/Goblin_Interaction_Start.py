import pygame
from .Smoke_Goblin_Interaction import Smoke_Goblin_Interaction
from .Health_Goblin_Interaction import Health_Goblin_Interaction
from .Choice_Goblin_Interaction import Choice_Goblin_Interaction


class Goblin_Interaction_Start:
    # Set background image to white
    background = pygame.transform.scale(pygame.image.load('Dependencies/Images/WhiteBackground.png'), (1300, 1000))
    backgroundRect = background.get_rect()
    backgroundRect.top, backgroundRect.left = 0, 0

    # Load hero and goblin images
    hero_image = pygame.transform.scale(pygame.image.load('Dependencies/Images/interactionHero.png'), (1300, 1000))
    goblin_image = pygame.transform.scale(pygame.image.load('Dependencies/Images/goblin_new_interaction.jpg'), (1300, 1000))

    def __init__(self, gameDisplay, windowSize, Font, goblin, hero):
        """Called from GameCharacters.py - HeroFoundGoblin
        Params: gameDisplay - Pygame window
        windowSize - Pygame window size
        Font - Ready made font
        goblin - Goblin the hero has met
        """

        self.gameDisplay = gameDisplay

        self.heroInteraction_image = pygame.transform.scale(self.hero_image,
                                                       (int(windowSize[0] * 0.3), int(windowSize[1] * 0.4)))
        self.heroInteraction_imageRect = self.heroInteraction_image.get_rect()
        self.heroInteraction_imageRect.top = 0.3 * windowSize[1]
        self.heroInteraction_imageRect.left = 0.05 * windowSize[0]

        self.goblinInteraction_image = pygame.transform.scale(self.goblin_image,
                                                              (int(windowSize[0] * 0.3), int(windowSize[1] * 0.4)))
        self.goblinInteraction_imageRect = self.goblinInteraction_image.get_rect()
        self.goblinInteraction_imageRect.top = 0.05 * windowSize[1]
        self.goblinInteraction_imageRect.right = 0.95 * windowSize[0]

        self.draw_scene()

        if goblin.ability == "Smoke":
            Smoke_Goblin_Interaction(self.gameDisplay, windowSize, Font, self.goblinInteraction_imageRect,
                                     self.heroInteraction_imageRect, self, hero)
        elif goblin.ability == "Health":
            Health_Goblin_Interaction(self.gameDisplay, windowSize, self.goblinInteraction_imageRect,
                                     self.heroInteraction_imageRect, self, hero)
        else:
            choiceGoblin = Choice_Goblin_Interaction(self.gameDisplay, windowSize, self, Font, self.goblinInteraction_imageRect)
            choice = choiceGoblin.get_choice()
            if choice == "Smoke":
                Smoke_Goblin_Interaction(self.gameDisplay, windowSize, Font, self.goblinInteraction_imageRect,
                                         self.heroInteraction_imageRect, self, hero)
            else:
                Health_Goblin_Interaction(self.gameDisplay, windowSize, self.goblinInteraction_imageRect,
                                          self.heroInteraction_imageRect, self, hero)

    def draw_scene(self, update=True):
        # White background
        self.gameDisplay.blit(self.background, self.backgroundRect)
        # Draw hero
        self.gameDisplay.blit(self.heroInteraction_image, self.heroInteraction_imageRect)
        # Draw goblin
        self.gameDisplay.blit(self.goblinInteraction_image, self.goblinInteraction_imageRect)

        if update:
            # Update screen
            pygame.display.update()
