import pygame
import sys


class BattleScene:
    heroBattleOptions = [(1, "Light Attack"), (2, "Heavy Attack"), (3, "Smoke Bomb Escape")]

    def __init__(self, hero, monster, gameDisplay, hero_image, heroRect, monster_image, monsterRect, backGroundImage,
                 windowSize, buttonImage, Font, gameCharacters):
        self.hero = hero
        self.monster = monster
        self.gameDisplay = gameDisplay
        self.gameCharacters = gameCharacters
        self.outcome = ""
        self.battle(gameDisplay, hero_image, heroRect, monster_image, monsterRect, backGroundImage, windowSize,
                    buttonImage, Font)

    def blit_battle(self, gameDisplay, hero_image, heroRect, monster_image, monsterRect, backGroundImage, windowSize,
                    buttonImage, Font):
        # Draw white background
        backGroundRect = backGroundImage.get_rect()
        backGroundRect.top, backGroundRect.left = 0, 0
        gameDisplay.blit(backGroundImage, backGroundRect)

        # Draw hero and monster
        gameDisplay.blit(hero_image, heroRect)
        gameDisplay.blit(monster_image, monsterRect)

        # Draw hero and monster health
        gameDisplay.blit((Font.render("Monster Health: " + str(self.monster.health), 1, (255, 0, 0))),
                         (monsterRect.left - 15, monsterRect.top - 10))  # Monster
        gameDisplay.blit((Font.render("Hero Health: " + str(self.hero.health), 1, (0, 255, 0))),
                         (heroRect.left, heroRect.top - 30))

        # Draw hero options
        self.lightButton = buttonImage.get_rect()
        self.heavyButton = buttonImage.get_rect()
        self.smokeButton = buttonImage.get_rect()

        self.lightButton.bottom, self.heavyButton.bottom, self.smokeButton.bottom = windowSize[1] * 0.95, \
                                                                                    windowSize[1] * 0.95, \
                                                                                    windowSize[1] * 0.95
        self.heavyButton.centerx = int(windowSize[0]/2)
        gameDisplay.blit(buttonImage, self.heavyButton)

        self.lightButton.centerx = int(windowSize[0]/6)
        gameDisplay.blit(buttonImage, self.lightButton)

        self.smokeButton.right = int(windowSize[0] - (self.lightButton.left))
        gameDisplay.blit(buttonImage, self.smokeButton)

        # Draw text
        lightText = Font.render("Light Attack", 1, (0, 0, 0))
        lightTextRect = lightText.get_rect()
        lightTextRect.center = self.lightButton.center
        gameDisplay.blit(lightText, lightTextRect)

        heavyText = Font.render("Heavy Attack", 1, (0, 0, 0))
        heavyTextRect = heavyText.get_rect()
        heavyTextRect.center = self.heavyButton.center
        gameDisplay.blit(heavyText, heavyTextRect)

        smokeText = Font.render("Smoke", 1, (0, 0, 0))
        smokeTextRect = smokeText.get_rect()
        smokeTextRect.center = self.smokeButton.center
        gameDisplay.blit(smokeText, smokeTextRect)

        # Draw the dialog box
        self.gameCharacters.dialogBox.blitme(gameDisplay)

        # Update the display
        pygame.display.update()

    def blit_battle_end(self, gameDisplay, hero_image, heroRect, monster_image, monsterRect, backGroundImage,
                        windowSize,
                        buttonImage, Font):
        # Draw white background
        backGroundRect = backGroundImage.get_rect()
        backGroundRect.top, backGroundRect.left = 0, 0
        gameDisplay.blit(backGroundImage, backGroundRect)

        # Draw hero and monster
        gameDisplay.blit(hero_image, heroRect)
        gameDisplay.blit(monster_image, monsterRect)

        # Draw hero and monster health
        gameDisplay.blit((Font.render("Monster Health: " + str(self.monster.health), 1, (255, 0, 0))),
                         (monsterRect.left - 15, monsterRect.top - 10))  # Monster
        gameDisplay.blit((Font.render("Hero Health: " + str(self.hero.health), 1, (0, 255, 0))),
                         (heroRect.left, heroRect.top - 30))

        # Draw the dialog box
        self.gameCharacters.dialogBox.blitme(gameDisplay)

        # Draw a button for the user to click (confirming the end of the battle)
        buttonRect = buttonImage.get_rect()
        buttonRect.bottom = windowSize[1] * 0.95
        buttonRect.left = (windowSize[0] - buttonImage.get_width()) / 2

        Text = Font.render("Continue", 1, (0, 0, 0))
        TextRect = Text.get_rect()
        TextRect.center = buttonRect.center

        gameDisplay.blit(buttonImage, buttonRect)
        gameDisplay.blit(Text, TextRect)

        # Update the display
        pygame.display.update()

        pressed = False
        while not pressed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if buttonRect.top <= event.pos[1] <= buttonRect.bottom:
                        if buttonRect.left <= event.pos[0] <= buttonRect.right:
                            pressed = True

    def battle(self, gameDisplay, hero_image, heroRect, monster_image, monsterRect, backGroundImage, windowSize,
               buttonImage, Font):

        self.gameCharacters.dialogBox.set_text("The Monster Confronts you!")
        self.blit_battle(gameDisplay, hero_image, heroRect, monster_image, monsterRect,
                                                 backGroundImage, windowSize, buttonImage, Font)

        while self.monster.alive and self.hero.alive:
            # Wait until a button is selected
            chosen = False
            while not chosen:
                for event in pygame.event.get():
                    # Check if game is being Quit
                    if event.type == pygame.QUIT:
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONUP:
                        if self.lightButton.collidepoint(event.pos):
                            damage = self.hero.lightAttack()
                            if damage > 0:
                                self.gameCharacters.dialogBox.set_text(
                                    "Your Light Attack was successful!\n %d Damage dealt to the monster" % damage)
                                self.monster.takeDamage(damage)
                            else:
                                self.gameCharacters.dialogBox.set_text(
                                    "Your Light Attack was unsuccessful!")
                            chosen = True
                        elif self.heavyButton.collidepoint(event.pos):
                            damage = self.hero.heavyAttack()
                            if damage > 0:
                                self.gameCharacters.dialogBox.set_text(
                                    "Your Heavy Attack was successful!\n %d Damage dealt to the monster" % damage)
                                self.monster.takeDamage(damage)
                            else:
                                self.gameCharacters.dialogBox.set_text(
                                    "Your Heavy Attack was unsuccessful!")
                            chosen = True
                        elif self.smokeButton.collidepoint(event.pos):
                            if self.hero.checkSmokeBombs() > 0:
                                self.gameCharacters.dialogBox.set_text(
                                    "You use a smoke bomb to escape the monster!\n RUN!")
                                chosen = True
                                self.outcome = "Smoke"
                                self.hero.useSmokeBomb()
                                break
                            else:
                                self.gameCharacters.dialogBox.set_text(
                                    "You have no smoke bombs left to use!")
                                self.blit_battle(gameDisplay, hero_image, heroRect, monster_image, monsterRect,
                                                 backGroundImage, windowSize,
                                                 buttonImage, Font)
                                pygame.display.update()

            # Display health of monster and hero
            self.blit_battle(gameDisplay, hero_image, heroRect, monster_image, monsterRect, backGroundImage, windowSize,
                             buttonImage, Font)
            pygame.display.update()
            if self.outcome == "Smoke":
                break

            if self.monster.alive:
                self.gameCharacters.wait(1)
                damage = self.monster.battle_turn()
                if damage > self.monster.damage:
                    self.gameCharacters.dialogBox.set_text(
                        "The Monster lands a critical hit!\n %d Damage dealt " % damage)
                else:
                    self.gameCharacters.dialogBox.set_text(
                        "The Monster lands a powerful hit!\n %d Damage dealt " % damage)
                self.hero.take_damage(damage)
            self.blit_battle(gameDisplay, hero_image, heroRect, monster_image, monsterRect, backGroundImage, windowSize,
                             buttonImage, Font)
            pygame.display.update()
        # End of battle
        # Check who won the battle
        # Display the winner in the dialog box
        # User can press button to continue
        if self.outcome == "":
            if self.hero.alive:
                self.outcome = "Hero"
                self.gameCharacters.dialogBox.set_text(
                    "You triumph over the monster!")
            else:
                self.outcome = "Monster"
                self.gameCharacters.dialogBox.set_text(
                    "You were no match for the monsters wrath!")
        self.blit_battle_end(gameDisplay, hero_image, heroRect, monster_image, monsterRect, backGroundImage, windowSize,
                         buttonImage, Font)
        pygame.display.update()
