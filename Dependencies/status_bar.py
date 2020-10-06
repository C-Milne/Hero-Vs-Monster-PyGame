import pygame


class StatusPanel(pygame.sprite.Sprite):
    whiteLine = pygame.image.load('Dependencies/Images/WhiteBackground.png')

    def __init__(self, top, scaler, gameDisplay, Settings, Hero, windowSize):
        """Called from """
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('Dependencies/Images/Status_bar.png')
        
        self.image = pygame.transform.scale(self.image, (int(1240*scaler), int(100*scaler)-5))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = 0, top

        # The bottom row of black grid block can also be used
        self.top = self.rect.top - Settings.blockSize

        fontSize = 20
        self.Font = pygame.font.SysFont("Segoe UI", fontSize, bold=True)

        self.gameDisplay = gameDisplay
        self.settings = Settings
        self.Hero = Hero

        self.size = self.image.get_height() + Settings.blockSize
        self.Divider = pygame.transform.scale(self.whiteLine, (5, self.size))

        # Set rects for the text
        # Set font fo biggest size possible
        while True:
            self.get_values()

            self.HeroHealthRect = self.HeroHealth.get_rect()
            self.HeroHealthRect.top, self.HeroHealthRect.left = self.top, 0

            self.HeroHitRect = self.HeroHit.get_rect()
            self.HeroHitRect.top, self.HeroHitRect.left = self.HeroHealthRect.bottom, 0

            self.HeroDamageRect = self.HeroDamage.get_rect()
            self.HeroDamageRect.top, self.HeroDamageRect.left = self.HeroHitRect.bottom, 0

            self.DividerRect1 = self.Divider.get_rect()
            self.DividerRect1.left, self.DividerRect1.top = self.HeroHitRect.right, self.HeroHealthRect.top

            # ////////////////////////////////////////////////////////////////////////////////////////////////////////
            self.levelRect = self.level.get_rect()
            self.levelRect.top, self.levelRect.left = self.HeroHealthRect.top, self.DividerRect1.right

            self.dayRect = self.day.get_rect()
            self.dayRect.top, self.dayRect.left = self.levelRect.bottom, self.DividerRect1.right

            self.movesRect = self.moves.get_rect()
            self.movesRect.top, self.movesRect.left = self.dayRect.bottom, self.DividerRect1.right

            self.DividerRect2 = self.Divider.get_rect()
            self.DividerRect2.left, self.DividerRect2.top = self.movesRect.right, self.HeroHealthRect.top

            # ////////////////////////////////////////////////////////////////////////////////////////////////////////

            self.smokeRect = self.smoke.get_rect()
            self.smokeRect.bottom, self.smokeRect.left = self.top + self.size / 2, self.DividerRect2.right

            self.remainingRect = self.remaining.get_rect()
            self.remainingRect.center, self.remainingRect.top = self.smokeRect.center, self.smokeRect.bottom

            self.DividerRect3 = self.Divider.get_rect()
            self.DividerRect3.left, self.DividerRect3.top = self.smokeRect.right, self.HeroHealthRect.top

            # ////////////////////////////////////////////////////////////////////////////////////////////////////////
            self.monsterHealthRect = self.monsterHealth.get_rect()
            self.monsterHealthRect.top, self.monsterHealthRect.left = self.HeroHealthRect.top, self.DividerRect3.right

            self.monsterDamageRect = self.monsterDamage.get_rect()
            self.monsterDamageRect.top, self.monsterDamageRect.left = self.monsterHealthRect.bottom, self.DividerRect3.right

            self.monsterMovesRect = self.monsterMoves.get_rect()
            self.monsterMovesRect.top, self.monsterMovesRect.left = self.monsterDamageRect.bottom, self.DividerRect3.right

            # Check for gap at bottom of the panel
            # Check that text does not go off the right side of the screen
            if (self.HeroDamageRect.bottom <= windowSize[1]) and (self.monsterMovesRect.right < windowSize[0]):
                fontSize += 1
                self.Font = pygame.font.SysFont("Segoe UI", fontSize, bold=True)
            else:
                fontSize -= 3
                self.Font = pygame.font.SysFont("Segoe UI", fontSize, bold=True)
                break

    def get_values(self):
        """Create string and rects for all the values"""
        self.HeroHealth = self.Font.render("Hero Health: " + str(self.Hero.health), 1, (255, 255, 255))
        self.HeroHit = self.Font.render("Hero Hit Chance: " + str(self.Hero.hitChance), 1, (255, 255, 255))
        self.HeroDamage = self.Font.render("Hero Damage: " + str(self.Hero.damage), 1, (255, 255, 255))

        # ////////////////////////////////////////////////////////////////////////////////////////////////////////
        self.level = self.Font.render("Level: " + str(self.settings.level), 1, (255, 255, 255))
        self.day = self.Font.render("Day: " + str(self.settings.day), 1, (255, 255, 255))
        self.moves = self.Font.render("Moves Left Today: " + str(self.settings.hero.moves), 1, (255, 255, 255))

        # ///////////////////////////////////////////////////////////////////////////////////////////////////////
        self.smoke = self.Font.render("Smoke Bombs", 1, (255, 255, 255))
        self.remaining = self.Font.render("Remaining: " + str(self.Hero.smokeBombs), 1, (255, 255, 255))

        # ///////////////////////////////////////////////////////////////////////////////////////////////////////
        monster = self.settings.gameCharacters.getMonster()
        if monster:
            # Monster info
            self.monsterHealth = self.Font.render("Monster Health: " + str(monster.health), 1, (255, 255, 255))
            self.monsterDamage = self.Font.render("Monster Damage: " + str(monster.damage), 1, (255, 255, 255))
            self.monsterMoves = self.Font.render("Monster Moves Left: " + str(monster.moves), 1, (255, 255, 255))
        else:
            self.monsterHealth = self.Font.render("Monster Health: 0", 1, (255, 255, 255))
            self.monsterDamage = self.Font.render("Monster Damage: 0", 1, (255, 255, 255))
            self.monsterMoves = self.Font.render("Monster Moves Left: 0", 1, (255, 255, 255))

    def blitme(self):
        self.gameDisplay.blit(self.image, self.rect)
        self.get_values()

        self.gameDisplay.blit(self.HeroHealth, self.HeroHealthRect)
        self.gameDisplay.blit(self.HeroHit, self.HeroHitRect)
        self.gameDisplay.blit(self.HeroDamage, self.HeroDamageRect)
        self.gameDisplay.blit(self.Divider, self.DividerRect1)
        #///////////////////////////////////////////////////////////////////////////////////////////////////////

        self.gameDisplay.blit(self.level, self.levelRect)
        self.gameDisplay.blit(self.day, self.dayRect)
        self.gameDisplay.blit(self.moves, self.movesRect)
        self.gameDisplay.blit(self.Divider, self.DividerRect2)
        # ///////////////////////////////////////////////////////////////////////////////////////////////////////

        self.gameDisplay.blit(self.smoke, self.smokeRect)
        self.gameDisplay.blit(self.remaining, self.remainingRect)
        self.gameDisplay.blit(self.Divider, self.DividerRect3)
        # ///////////////////////////////////////////////////////////////////////////////////////////////////////

        self.gameDisplay.blit(self.monsterHealth, self.monsterHealthRect)
        self.gameDisplay.blit(self.monsterDamage, self.monsterDamageRect)
        self.gameDisplay.blit(self.monsterMoves, self.monsterMovesRect)
