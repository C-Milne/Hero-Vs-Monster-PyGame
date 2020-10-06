import pygame
import timeit
import sys
import random
from Dependencies.Dialogbox import DialogBox


class Health_Goblin_Interaction:
    interactionButton = pygame.image.load('Dependencies/Images/Button.png')

    def __init__(self, gameDisplay, windowSize, goblinRect, heroRect, super, hero):
        """Hero plays best of 3 ODD or EVEN game with the goblin
            The hero must choose either ODD or EVEN, if the goblin has chosen the same then the hero wins a point
            If they have choosen different then the goblin wins a point"""
        self.super = super
        self.gameDisplay = gameDisplay
        self.hero = hero
        self.BigFont = pygame.font.SysFont("segoeprint", 78)
        self.SmallFont = pygame.font.SysFont("Times New Roman", 30)

        self.button = pygame.transform.scale(self.interactionButton,
                                             (int(windowSize[0] * 0.25), int(windowSize[1] * 0.25)))
        self.oddButtonRect = self.button.get_rect()
        self.evenButtonRect = self.button.get_rect()
        self.middleSectionRect = self.button.get_rect()

        self.middleSectionRect.center = (int(windowSize[0]/2), int(windowSize[1]/2))
        self.middleSectionRect.bottom = int(windowSize[1] * 0.95)

        self.oddButtonRect.bottom = self.middleSectionRect.bottom
        self.evenButtonRect.bottom = self.middleSectionRect.bottom
        self.oddButtonRect.right = self.middleSectionRect.left
        self.evenButtonRect.left = self.middleSectionRect.right

        # Create text boxes
        self.oddText = self.SmallFont.render("Odd", 1, (0, 0, 0))
        self.oddTextRect = self.oddText.get_rect()
        self.oddTextRect.center = self.oddButtonRect.center

        self.evenText = self.SmallFont.render("Even", 1, (0, 0, 0))
        self.evenTextRect = self.evenText.get_rect()
        self.evenTextRect.center = self.evenButtonRect.center

        self.continueText = self.SmallFont.render("Continue", 1, (0, 0, 0))
        self.continueTextRect = self.continueText.get_rect()
        self.continueTextRect.center = self.middleSectionRect.center

        # Define dialog box
        self.dialog = DialogBox(windowSize)
        self.dialog.set_rect_right(windowSize[0])
        self.dialog.set_rect_top(goblinRect.bottom)
        self.dialog.set_text("You are stumble accross a HEALTH goblin!")

        # Initilise
        self.choice = None
        self.result = False
        self.animationNumberCenter = (heroRect.center[0], goblinRect.top)

        self.play()

    def play(self):
        """Called from __init__
        Controls the mini game that the user is about to play"""

        # Change text in dialog to explain the game better
        self.drawScene(False)
        self.wait(1.5)
        self.dialog.set_text("The Goblin is thinking of a number\nIs it ODD or EVEN?")

        self.drawScene()

        # Wait for user to click button
        clicked = False
        while not clicked:
            for event in pygame.event.get():
                # Check if game is being Quit
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.oddButtonRect.collidepoint(event.pos):
                        self.choice = "Odd"
                        self.dialog.set_text("You chose ODD")
                        clicked = True

                    elif self.evenButtonRect.collidepoint(event.pos):
                        self.choice = "Even"
                        self.dialog.set_text("You chose EVEN")
                        clicked = True

        for i in range(random.randint(10, 20)):
            self.drawAnimation()
            self.wait(0.1)
        self.drawAnimation(True)

    def drawScene(self, buttons=True):
        """Draw a scene in which the user is given a choice between even and odd"""
        self.super.draw_scene(False)
        self.draw_dialog()

        if buttons:
            # Draw buttons
            self.gameDisplay.blit(self.button, self.evenButtonRect)
            self.gameDisplay.blit(self.button, self.oddButtonRect)

            # Draw text boxes
            self.gameDisplay.blit(self.evenText, self.evenTextRect)
            self.gameDisplay.blit(self.oddText, self.oddTextRect)
        pygame.display.update()

    def drawAnimation(self, final=False):
        """Draw the scene of changing numbers which eventually end on a value"""
        self.super.draw_scene(False)
        self.draw_dialog()
        # Choose random number to display
        n = random.randint(1, 9)
        number = self.BigFont.render(str(n), 1, (255, 0, 0))
        numberRect = number.get_rect()
        numberRect.center = self.animationNumberCenter
        self.gameDisplay.blit(number, numberRect)
        pygame.display.update()

        if final:
            # Check if user was correct
            n %= 2
            if n == 1:
                # Odd
                if self.choice == "Odd":
                    self.result = True
            else:
                # Even
                if self.choice == "Even":
                    self.result = True

            if self.result:
                self.dialog.set_text("Luck is on your side!\nYou have gained HEALTH")
                self.hero.gainedMaxHealth()
            else:
                self.dialog.set_text("You chose poorly!")

            # Draw scene again but with new dialog box and continue button
            self.super.draw_scene(False)
            self.draw_dialog()
            self.gameDisplay.blit(number, numberRect)
            self.gameDisplay.blit(self.button, self.middleSectionRect)
            self.gameDisplay.blit(self.continueText, self.continueTextRect)
            pygame.display.update()

            # Wait for user to click continue button
            chosen = False
            while not chosen:
                for event in pygame.event.get():
                    # Check if game is being Quit
                    if event.type == pygame.QUIT:
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONUP:
                        if self.middleSectionRect.collidepoint(event.pos):
                            chosen = True

    @staticmethod
    def wait(secs):
        start = timeit.default_timer()
        while timeit.default_timer() - start < secs:
            for event in pygame.event.get():
                # Check if game is being Quit
                if event.type == pygame.QUIT:
                    sys.exit()

    def draw_dialog(self):
        self.dialog.blitme(self.gameDisplay)
