import pygame
import sys
from Dependencies.Dialogbox import DialogBox


class Choice_Goblin_Interaction:
    interactionButton = pygame.image.load('Dependencies/Images/Button.png')

    def __init__(self, gameDisplay, windowSize, super, Font, goblinRect):
        """Choose Weather you want the goblin top be a health goblin or a smoke goblin"""
        self.gameDisplay = gameDisplay
        self.super = super
        self.Font = Font
        
        # After choosing which ability the goblin has, re-choose the goblins interation keys
        self.button = pygame.transform.scale(self.interactionButton,
                                             (int(windowSize[0] * 0.25), int(windowSize[1] * 0.25)))

        self.smokeButtonRect = self.button.get_rect()
        self.healthButtonRect = self.button.get_rect()
        self.middleSectionRect = self.button.get_rect()

        self.middleSectionRect.center = (int(windowSize[0] / 2), int(windowSize[1] / 2))
        self.middleSectionRect.bottom = int(windowSize[1] * 0.95)

        self.smokeButtonRect.bottom = self.middleSectionRect.bottom
        self.healthButtonRect.bottom = self.middleSectionRect.bottom
        self.smokeButtonRect.right = self.middleSectionRect.left
        self.healthButtonRect.left = self.middleSectionRect.right

        self.smokeText = self.Font.render("Smoke", 1, (0, 0, 0))
        self.healthText = self.Font.render("Health", 1, (0, 0, 0))
        self.continueText = self.Font.render("Continue", 1, (0, 0, 0))

        self.smokeTextRect = self.smokeText.get_rect()
        self.healthTextRect = self.healthText.get_rect()
        self.continueTextRect = self.continueText.get_rect()

        self.smokeTextRect.center = self.smokeButtonRect.center
        self.healthTextRect.center = self.healthButtonRect.center
        self.continueTextRect.center = self.middleSectionRect.center

        # Define dialog box
        self.dialog = DialogBox(windowSize)
        self.dialog.set_rect_right(windowSize[0])
        self.dialog.set_rect_top(goblinRect.bottom)
        self.dialog.set_text("You are come face to face with a CHOICE goblin!")

        self.choice = None

    def get_choice(self):
        self.super.draw_scene(False)
        self.gameDisplay.blit(self.button, self.smokeButtonRect)
        self.gameDisplay.blit(self.button, self.healthButtonRect)

        self.gameDisplay.blit(self.smokeText, self.smokeTextRect)
        self.gameDisplay.blit(self.healthText, self.healthTextRect)
        self.dialog.set_text("You must choose which type of goblin\nyou wish to meet")
        self.draw_dialog()
        pygame.display.update()

        # Wait for user to click on a button
        chosen = False
        while not chosen:
            for event in pygame.event.get():
                # Check if game is being Quit
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.smokeButtonRect.collidepoint(event.pos):
                        chosen = True
                        self.choice = "Smoke"

                    elif self.healthButtonRect.collidepoint(event.pos):
                        chosen = True
                        self.choice = "Health"

        # Re-draw scene
        self.super.draw_scene(False)
        self.gameDisplay.blit(self.button, self.middleSectionRect)
        self.gameDisplay.blit(self.continueText, self.continueTextRect)
        self.dialog.set_text("You have chosen to meet a\n" + self.choice.upper() + " goblin")
        self.draw_dialog()
        pygame.display.update()

        # Wait for user to click continue
        chosen = False
        while not chosen:
            for event in pygame.event.get():
                # Check if game is being Quit
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.middleSectionRect.collidepoint(event.pos):
                        chosen = True

        return self.choice

    def draw_dialog(self):
        self.dialog.blitme(self.gameDisplay)