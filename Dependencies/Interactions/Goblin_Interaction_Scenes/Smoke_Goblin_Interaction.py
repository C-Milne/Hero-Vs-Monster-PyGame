import pygame
import random
import sys
import timeit
from Dependencies.Dialogbox import DialogBox


class Smoke_Goblin_Interaction:
    # Set standard interaction images
    interactionButton = pygame.image.load('Dependencies/Images/Button.png')
    thinkingBubble = pygame.image.load('Dependencies/Images/thinkingCloudFromRight.png')
    thinkingBubbleBottom = pygame.image.load('Dependencies/Images/thinkingCloudFromBottom.png')
    rock = pygame.image.load('Dependencies/Images/rock.png')
    paper = pygame.image.load('Dependencies/Images/paper.png')
    scissors = pygame.image.load('Dependencies/Images/scissors.png')

    goblinChoices = ["Rock", "Paper", "Scissors"]

    def __init__(self, gameDisplay, windowSize, Font, goblinRect, heroRect, super, hero):
        """Hero Interacts with a Goblin with the Smoke ability
                The hero and goblin play Rock, Paper, Scissors
                If the Hero wins the goblin rewards a smokebomb
                Selection:
                1 - rock
                2 - paper
                3 - Scissors"""
        self.gameDisplay = gameDisplay
        self.super = super
        self.hero = hero

        # Define buttons along with rect's
        self.rockButton = pygame.transform.scale(self.interactionButton,
                                                        (int(windowSize[0] * 0.25), int(windowSize[1] * 0.25)))
        self.rockButtonRect = self.rockButton.get_rect()

        self.paperButton = pygame.transform.scale(self.interactionButton,
                                                        (int(windowSize[0] * 0.25), int(windowSize[1] * 0.25)))
        self.paperButtonRect = self.paperButton.get_rect()

        self.scissorsButton = pygame.transform.scale(self.interactionButton,
                                             (int(windowSize[0] * 0.25), int(windowSize[1] * 0.25)))
        self.scissorsButtonRect = self.scissorsButton.get_rect()

        # Set bottom coord for buttons
        self.rockButtonRect.bottom = windowSize[1] * 0.95
        self.paperButtonRect.bottom = windowSize[1] * 0.95
        self.scissorsButtonRect.bottom = windowSize[1] * 0.95

        # Set left coord for buttons
        self.rockButtonRect.left = windowSize[0] * 0.075
        self.paperButtonRect.left = (windowSize[0] * 0.075) + int(windowSize[0] * 0.3)
        self.scissorsButtonRect.left = (windowSize[0] * 0.075) + (int(windowSize[0] * 0.3) * 2)

        # Create text boxes
        self.rockText = Font.render("Rock", 1, (0, 0, 0))
        self.rockTextRect = self.rockText.get_rect()
        self.rockTextRect.center = self.rockButtonRect.center

        self.paperText = Font.render("Paper", 1, (0, 0, 0))
        self.paperTextRect = self.paperText.get_rect()
        self.paperTextRect.center = self.paperButtonRect.center

        self.scissorsText = Font.render("Scissors", 1, (0, 0, 0))
        self.scissorsTextRect = self.scissorsText.get_rect()
        self.scissorsTextRect.center = self.scissorsButtonRect.center

        self.endGameButtonText = Font.render("Continue", 1, (0, 0, 0))
        self.endGameButtonTextRect = self.endGameButtonText.get_rect()
        self.endGameButtonTextRect.center = self.paperButtonRect.center

        # Create thinking bubbles
        self.rightThinkingCloud = pygame.transform.scale(self.thinkingBubble,
                                                         (int(windowSize[0] * 0.25), int(windowSize[1] * 0.25)))
        self.rightThinkingCloudRect = self.rightThinkingCloud.get_rect()
        self.rightThinkingCloudRect.top = 0
        self.rightThinkingCloudRect.right = goblinRect.left

        self.bottomThinkingCloud = pygame.transform.scale(self.thinkingBubbleBottom,
                                                         (int(windowSize[0] * 0.25), int(windowSize[1] * 0.25)))
        self.bottomThinkingCloudRect = self.bottomThinkingCloud.get_rect()
        self.bottomThinkingCloudRect.center = heroRect.center
        self.bottomThinkingCloudRect.bottom = heroRect.top

        # Create rock, paper, and scissor images
        bubbleSize = self.rightThinkingCloudRect.size
        self.rockImage = pygame.transform.scale(self.rock, (int(bubbleSize[0] * 0.5), int(bubbleSize[1] * 0.5)))
        self.rockImageRect = self.rockImage.get_rect()

        self.paperImage = pygame.transform.scale(self.paper, (int(bubbleSize[0] * 0.5), int(bubbleSize[1] * 0.5)))
        self.paperImageRect = self.paperImage.get_rect()

        self.scissorsImage = pygame.transform.scale(self.scissors, (int(bubbleSize[0] * 0.5), int(bubbleSize[1] * 0.5)))
        self.scissorsImageRect = self.scissorsImage.get_rect()

        # Define dialog box
        self.dialog = DialogBox(windowSize)
        self.dialog.set_rect_right(windowSize[0])
        self.dialog.set_rect_top(goblinRect.bottom)
        self.dialog.set_text("You are approached by a SMOKE goblin!")

        """Currently undefined variables"""
        self.heroChoice = None
        self.winner = None  # Winner of the game

        self.draw_hero_choices()    # Get user to make a choice

    def draw_hero_choices(self):
        """Called form __init__"""
        self.super.draw_scene()
        self.draw_dialog()

        # Draw buttons on display
        self.gameDisplay.blit(self.rockButton, self.rockButtonRect)
        self.gameDisplay.blit(self.paperButton, self.paperButtonRect)
        self.gameDisplay.blit(self.scissorsButton, self.scissorsButtonRect)

        # Draw text boxes
        self.gameDisplay.blit(self.rockText, self.rockTextRect)
        self.gameDisplay.blit(self.paperText, self.paperTextRect)
        self.gameDisplay.blit(self.scissorsText, self.scissorsTextRect)

        # Update the display
        pygame.display.update()

        # Wait for player selection
        # Wait until a button is selected
        chosen = False
        while not chosen:
            for event in pygame.event.get():
                # Check if game is being Quit
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.rockButtonRect.collidepoint(event.pos):
                        chosen = True
                        self.heroChoice = "Rock"
                    elif self.paperButtonRect.collidepoint(event.pos):
                        chosen = True
                        self.heroChoice = "Paper"
                    elif self.scissorsButtonRect.collidepoint(event.pos):
                        chosen = True
                        self.heroChoice = "Scissors"
        self.result()

    def result(self):
        """Called from draw_hero_choices
        Handles end of interaction
        Compares hero choice to randomly generated goblin choice"""
        # Goblin chooses - rock, paper, or scissors
        goblinChoice = self.goblinChoices[random.randint(0, 2)]
        self.super.draw_scene(False)     # Draw the standard goblin interaction scene

        # Show the goblin's Choice
        # Draw thinking cloud near goblins head
        self.gameDisplay.blit(self.rightThinkingCloud, self.rightThinkingCloudRect)

        # Draw thinking cloud near heros head
        self.gameDisplay.blit(self.bottomThinkingCloud, self.bottomThinkingCloudRect)

        # Draw goblins choice in the cloud
        if goblinChoice == "Rock":
            self.rockImageRect.center = (self.rightThinkingCloudRect.center[0],
                                         self.rightThinkingCloudRect.center[1] - (self.rightThinkingCloudRect.size[1] * 0.15))
            self.gameDisplay.blit(self.rockImage, self.rockImageRect)

        elif goblinChoice == "Paper":
            self.paperImageRect.center = (self.rightThinkingCloudRect.center[0],
                                          self.rightThinkingCloudRect.center[1] - (self.rightThinkingCloudRect.size[1] * 0.15))
            self.gameDisplay.blit(self.paperImage, self.paperImageRect)

        else:   # GoblinChoice == "Scissors"
            self.scissorsImageRect.center = (self.rightThinkingCloudRect.center[0],
                                             self.rightThinkingCloudRect.center[1] - (self.rightThinkingCloudRect.size[1] * 0.15))
            self.gameDisplay.blit(self.scissorsImage, self.scissorsImageRect)

        # Draw hero's choice in bubble
        if self.heroChoice == "Rock":
            # Draw rock in hero bubble
            self.rockImageRect.center = (self.bottomThinkingCloudRect.center[0],
                                         self.bottomThinkingCloudRect.center[1] -
                                         (self.bottomThinkingCloudRect.size[1] * 0.15))
            self.gameDisplay.blit(self.rockImage, self.rockImageRect)
            self.dialog.set_text("You choose ROCK")

        elif self.heroChoice == "Paper":
            # Draw paper in hero bubble
            self.paperImageRect.center = (self.bottomThinkingCloudRect.center[0],
                                          self.bottomThinkingCloudRect.center[1] -
                                          (self.bottomThinkingCloudRect.size[1] * 0.15))
            self.gameDisplay.blit(self.paperImage, self.paperImageRect)
            self.dialog.set_text("You choose PAPER")

        else: # self.heroChoice == "Scissors"
            # Draw scissors in hero bubble
            self.scissorsImageRect.center = (self.bottomThinkingCloudRect.center[0],
                                             self.bottomThinkingCloudRect.center[1] -
                                             (self.bottomThinkingCloudRect.size[1] * 0.15))
            self.gameDisplay.blit(self.scissorsImage, self.scissorsImageRect)
            self.dialog.set_text("You choose SCISSORS")

        self.draw_dialog()
        pygame.display.update()
        self.wait(1)

        # Compare choices and decide winner
        if self.heroChoice == "Rock":
            if goblinChoice == "Rock":
                # Re-match
                self.dialog.set_text("Draw! Time for a REMATCH")
                self.draw_hero_choices()

            elif goblinChoice == "Paper":
                # Goblin wins
                self.winner = "Goblin"
                self.dialog.set_text("The goblin has BEAT you!")
                self.end_game()

            else: # goblinChoice == "Scissors"
                # Hero wins
                self.winner = "Hero"
                self.dialog.set_text("You have BESTED the goblin!\nYou are rewarded with a SMOKE bomb")
                self.end_game()

        elif self.heroChoice == "Paper":
            if goblinChoice == "Rock":
                # Hero wins
                self.winner = "Hero"
                self.dialog.set_text("You have BESTED the goblin!\nYou are rewarded with a SMOKE bomb")
                self.end_game()

            elif goblinChoice == "Paper":
                # Re-match
                self.dialog.set_text("Draw! Time for a REMATCH")
                self.draw_hero_choices()

            else:  # goblinChoice == "Scissors"
                # Goblin wins
                self.winner = "Goblin"
                self.dialog.set_text("The goblin has BEAT you!")
                self.end_game()

        else:   # self.heroChoice == "Scissors"
            if goblinChoice == "Rock":
                # Goblin wins
                self.winner = "Goblin"
                self.dialog.set_text("The goblin has BEAT you!")
                self.end_game()

            elif goblinChoice == "Paper":
                # Hero wins
                self.winner = "Hero"
                self.dialog.set_text("You have BESTED the goblin!\nYou are rewarded with a SMOKE bomb")
                self.end_game()

            else:  # goblinChoice == "Scissors"
                # Rematch
                self.dialog.set_text("Draw! Time for a REMATCH")
                self.draw_hero_choices()

    def end_game(self):
        # Give hero a smoke bomb if hero wins
        if self.winner == "Hero":
            self.hero.giveSmokeBomb()

        # User needs to click button to continue
        self.super.draw_scene()
        self.draw_dialog()
        # Draw button
        self.gameDisplay.blit(self.paperButton, self.paperButtonRect)
        # Draw text on the button
        self.gameDisplay.blit(self.endGameButtonText, self.endGameButtonTextRect)

        pygame.display.update()
        # Wait for user to click button
        clicked = False
        while not clicked:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    # Check if user clicked on button
                    if self.paperButtonRect.collidepoint(event.pos):
                        clicked = True

    def draw_dialog(self):
        self.dialog.blitme(self.gameDisplay)

    def wait(self, secs):
        start = timeit.default_timer()
        while timeit.default_timer() - start < secs:
            for event in pygame.event.get():
                # Check if game is being Quit
                if event.type == pygame.QUIT:
                    sys.exit()
