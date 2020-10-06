import pygame
import sys
from Dependencies.Dialogbox import DialogBox


class Chest:
    # Load required images
    backGround = pygame.image.load('Dependencies/Images/WhiteBackground.png')
    button = pygame.image.load('Dependencies/Images/button.png')
    chest = pygame.image.load('Dependencies/Images/chestInteraction.png')

    def __init__(self, coords, gameDisplay, windowSize, Font):
        """Hero can choose extra damage or extra hit chance
        Interaction can only be used once"""
        self.coords = coords    # String
        self.gameDisplay = gameDisplay
        self.windowSize = windowSize

        # Scale images
        self.backGround = pygame.transform.scale(self.backGround, self.windowSize)
        self.backGroundRect = self.backGround.get_rect()
        self.backGroundRect.left, self.backGroundRect.top = 0, 0

        self.chest = pygame.transform.scale(self.chest, (int(windowSize[0] * 0.5), int(windowSize[1] * 0.4)))
        self.chestRect = self.chest.get_rect()
        self.chestRect.center = self.backGroundRect.center

        self.button = pygame.transform.scale(self.button, (int(windowSize[0] * 0.25), int(windowSize[1] * 0.25)))

        self.damageButtonRect = self.button.get_rect()
        self.chanceButtonRect = self.button.get_rect()
        self.continueButtonRect = self.button.get_rect()

        self.continueButtonRect.center = (int(windowSize[0] / 2), int(windowSize[1] / 2))
        self.continueButtonRect.bottom = int(windowSize[1] * 0.95)

        self.damageButtonRect.right, self.damageButtonRect.top = self.continueButtonRect.left, self.continueButtonRect.top
        self.chanceButtonRect.left, self.chanceButtonRect.top = self.continueButtonRect.right, self.continueButtonRect.top

        # Create text boxes
        self.damageText = Font.render("Damage", 1, (0, 0, 0))
        self.chanceText = Font.render("Chance",1, (0, 0, 0))
        self.continueText = Font.render("Continue", 1, (0, 0, 0))

        self.damageTextRect = self.damageText.get_rect()
        self.chanceTextRect = self.chanceText.get_rect()
        self.continueTextRect = self.continueText.get_rect()

        self.damageTextRect.center = self.damageButtonRect.center
        self.chanceTextRect.center = self.chanceButtonRect.center
        self.continueTextRect.center = self.continueButtonRect.center

        # Define dialog box
        self.dialog = DialogBox(windowSize)
        self.dialog.set_rect_left(0)
        self.dialog.set_rect_top(0)
        self.dialog.set_text("You find a CHEST! You must choose!\nEither more damage or better hit chance!")

    def interaction(self, hero):
        """Run the interaction between the hero and chest"""
        self.draw_interaction()
        pygame.display.update()
        self.wait_for_choice()

        if self.choice == "Damage":
            # Buff hero damage
            hero.buffDamage(10)
        else:   # self.choice == "Chance"
            # Buff hero chance
            hero.buffChance(15)

        self.draw_interaction(True)
        pygame.display.update()
        self.wait_for_continue()

    def draw_interaction(self, end=False):
        """Hero is shown 2 buttons - must choose one
        Draw chest image in the middle of the window
        Buttons under chest"""
        # Draw white background
        self.gameDisplay.blit(self.backGround, self.backGroundRect)
        # Draw chest image
        self.gameDisplay.blit(self.chest, self.chestRect)
        # Draw dialog box
        self.draw_dialog()

        if not end:
            # Draw damage and chance buttons
            self.gameDisplay.blit(self.button, self.damageButtonRect)
            self.gameDisplay.blit(self.button, self.chanceButtonRect)

            # Draw text boxes
            self.gameDisplay.blit(self.damageText, self.damageTextRect)
            self.gameDisplay.blit(self.chanceText, self.chanceTextRect)
        else:
            # Draw continue Button
            self.gameDisplay.blit(self.button, self.continueButtonRect)

            # Draw text box
            self.gameDisplay.blit(self.continueText, self.continueTextRect)

    def wait_for_choice(self):
        """called from self.interaction
        Wait for the hero to click on a button"""

        chosen = False
        while not chosen:
            for event in pygame.event.get():
                # Check if game is being Quit
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.damageButtonRect.collidepoint(event.pos):
                        chosen = True
                        self.choice = "Damage"
                        self.dialog.set_text("You choose MORE DAMAGE!")
                    elif self.chanceButtonRect.collidepoint(event.pos):
                        chosen = True
                        self.choice = "Chance"
                        self.dialog.set_text("You choose HIGHER HIT CHANCE!")

    def wait_for_continue(self):
        """called from self.interaction
        Wait for the hero to click on continue button"""

        chosen = False
        while not chosen:
            for event in pygame.event.get():
                # Check if game is being Quit
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.continueButtonRect.collidepoint(event.pos):
                        chosen = True

    def draw_dialog(self):
        self.dialog.blitme(self.gameDisplay)
