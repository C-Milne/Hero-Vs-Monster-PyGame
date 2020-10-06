import pygame
import sys
import pickle
import os
import tkinter as tk

if __name__ == "__main__":
    os.chdir(os.getcwd()[:-26])

class GameOver:

    class leaderboard():

        def __init__(self, windowSize, titleRect):
            self.ranking = []
            self.Oimage = pygame.image.load('Dependencies/Images/GreyBackground.png')

            self.rect = None
            self.scoreFontSize = 30
            self.messageFontSize = 40
            self.titleRect = titleRect

            self.scoreFont = pygame.font.SysFont("Segoe UI", self.scoreFontSize, bold=True)
            self.messageFont = pygame.font.SysFont("Segoe UI", self.messageFontSize, bold=True)

            self.emptyMessage = self.messageFont.render("Looks like your the only one here!", 1, (0, 0, 0))
            self.emptyMessageRect = self.emptyMessage.get_rect()

            self.load(windowSize)

        def load(self, windowSize):
            self.Y_multiplier = 0.95
            self.rect = self.Oimage.get_rect()
            self.rect.center, self.rect.top = self.titleRect.center, self.titleRect.bottom

            while self.rect.bottom > int(windowSize[1] - windowSize[1] * 0.05):
                self.Y_multiplier -= 0.05
                self.image = pygame.transform.scale(self.Oimage, (int(windowSize[0] * 0.3), int(windowSize[1] * self.Y_multiplier)))
                self.rect = self.image.get_rect()
                self.rect.center, self.rect.top = self.titleRect.center, self.titleRect.bottom

            # Adjust font sizes
            self.emptyMessageRect.center = self.rect.center
            while self.emptyMessageRect.right > self.rect.right:
                # Make font smaller
                self.messageFontSize -= 1
                self.messageFont = pygame.font.SysFont("Segoe UI", self.messageFontSize, bold=True)
                self.emptyMessage = self.messageFont.render("Looks like your the only one here!", 1, (0, 0, 0))
                self.emptyMessageRect = self.emptyMessage.get_rect()
                self.emptyMessageRect.center = self.rect.center

        def check_entry(self, score):
            added = False
            if len(self.ranking) == 0:
                self.ranking.append((self.get_name(), score))
                added = True
            else:
                """iterate over self.ranking
                Check if current score is greater than index
                If so insert the current score"""
                for index in range(len(self.ranking)):
                    if score > self.ranking[index][1]:
                        self.ranking.insert(index, (self.get_name(), score))
                        self.check_leaderboard()
                        added = True
                        break

            if len(self.ranking) <= 10 and not added:
                self.ranking.append((self.get_name(), score))

        def check_leaderboard(self):
            if len(self.ranking) > 10:
                self.ranking = self.ranking[:10]

        def get_name(self):
            self.root = tk.Tk()
            self.root.geometry("400x300")
            self.root.title("Enter name")
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.root.resizable(0,0)
            #self.root.overrideredirect(1)
            self.root.attributes("-toolwindow", 1)

            self.form = tk.Canvas(self.root, width=400, height=300)
            self.form.pack()

            self.nameEntry = tk.Entry(self.root)
            self.form.create_window(200, 140, window=self.nameEntry)

            self.submitButton = tk.Button(text="Submit", command=self.readForm)
            self.form.create_window(200, 180, window=self.submitButton)

            self.instructionLabel = tk.Label(self.root, text="Enter your name below (MAX 4 characters)")
            self.form.create_window(200, 100, window=self.instructionLabel)

            self.messgaeLabel = tk.Label(self.root, text="CONGRATULATIONS you made it onto the leader board!")
            self.form.create_window(200, 50, window=self.messgaeLabel)

            self.root.mainloop()

            return self.name

        def readForm(self):
            user_input = self.nameEntry.get()
            if len(user_input) == 0 or len(user_input) > 4:
                # Show error label
                self.errorLabel = tk.Label(self.root, text="Input must be less than 4 characters and cannot be empty!")
                self.errorLabel.config(fg="red")
                self.form.create_window(200, 5, window=self.errorLabel)
            else:
                # Accept input
                self.name = user_input
                self.root.destroy()

        def on_closing(self, event=None):
            pass

        def blitme(self, gameDisplay):
            gameDisplay.blit(self.image, self.rect)

            # Draw names and scores
            # If leaderboard is empty display message
            if len(self.ranking) == 0:
                # Display message
                gameDisplay.blit(self.emptyMessage, self.emptyMessageRect)
            else:
                # Draw headers
                headerName = self.scoreFont.render("Name", 1, (0, 0, 0))
                headerLevel = self.scoreFont.render("Level", 1, (0, 0, 0))

                headerNameRect = headerName.get_rect()
                headerLevelRect = headerLevel.get_rect()

                headerNameRect.top, headerNameRect.left = self.rect.top, self.rect.left
                headerLevelRect.top, headerLevelRect.right = self.rect.top, self.rect.right

                gameDisplay.blit(headerName, headerNameRect)
                gameDisplay.blit(headerLevel, headerLevelRect)

                previousY = headerNameRect.bottom
                r = 1
                for i in self.ranking:
                    rank = self.scoreFont.render(str(r)+". ", 1, (0, 0, 0))
                    self.nameText = self.scoreFont.render(i[0], 1, (0, 0, 0))
                    self.scoreText = self.scoreFont.render(str(i[1]), 1, (0, 0, 0))

                    rankRect = rank.get_rect()
                    self.nameTextRect = self.nameText.get_rect()
                    self.scoreTextRect = self.scoreText.get_rect()

                    rankRect.left, rankRect.top = self.rect.left, previousY
                    self.nameTextRect.top, self.nameTextRect.left = previousY, rankRect.right
                    self.scoreTextRect.top, self.scoreTextRect.right = previousY, self.rect.right
                    previousY = self.nameTextRect.bottom

                    gameDisplay.blit(rank, rankRect)
                    gameDisplay.blit(self.nameText, self.nameTextRect)
                    gameDisplay.blit(self.scoreText, self.scoreTextRect)
                    r += 1

    backGround = pygame.image.load('Dependencies/Images/WhiteBackground.png')

    heroImage = pygame.image.load('Dependencies/Images/battleHero.png')

    monsterImage = pygame.image.load('Dependencies/Images/battleMonster.jpg')

    def __init__(self, gameDisplay, windowSize, score):
        self.gameDisplay = gameDisplay
        self.windowSize = windowSize

        self.backGround = pygame.transform.scale(self.backGround, self.windowSize)
        self.backGroundRect = self.backGround.get_rect()
        self.backGroundRect.left, self.backGroundRect.top = 0, 0

        self.Font = pygame.font.SysFont("Segoe UI", 90, bold=True)

        self.gameOverText = self.Font.render("GAME OVER", 1, (255, 0, 0))
        self.gameOverTextRect = self.gameOverText.get_rect()
        self.gameOverTextRect.top, self.gameOverTextRect.centerx = int(self.windowSize[1] * 0.1), int(self.windowSize[0]/2)


        # Check for leaderboard.pickle
        if os.path.isfile('Dependencies/Interactions/leaderboard.pickle'):
            self.LBoard = self.leaderboard(self.windowSize, self.gameOverTextRect)
            self.LBoard.ranking = pickle.load(open('Dependencies/Interactions/leaderboard.pickle', 'rb'))
        else:
            # Create leaderboard
            self.LBoard = self.leaderboard(self.windowSize, self.gameOverTextRect)

        self.monster = pygame.transform.scale(self.monsterImage,
                                              (int(windowSize[0] * 0.3), int(windowSize[1] * self.LBoard.Y_multiplier)))

        self.monsterRect = self.monster.get_rect()
        self.monsterRect.left, self.monsterRect.top = 0, self.LBoard.rect.top

        self.hero = pygame.transform.scale(self.heroImage,
                                           (int(windowSize[0] * 0.3), int(windowSize[1] * self.LBoard.Y_multiplier)))
        self.heroRect = self.hero.get_rect()
        self.heroRect.right, self.heroRect.top = windowSize[0], self.LBoard.rect.top

        self.blit_gameOver()
        self.LBoard.blitme(self.gameDisplay)

        pygame.display.update()

        self.LBoard.check_entry(score)

        # Save leaderboard
        self.saveLeaderBoard()

        self.LBoard.blitme(self.gameDisplay)

        pygame.display.update()
        self.wait_for_exit()

    def blit_gameOver(self):
        # Draw white background with game over written on it
        self.gameDisplay.blit(self.backGround, self.backGroundRect)
        self.gameDisplay.blit(self.gameOverText, self.gameOverTextRect)
        self.gameDisplay.blit(self.monster, self.monsterRect)
        self.gameDisplay.blit(self.hero, self.heroRect)

    def saveLeaderBoard(self):
        pickle.dump(self.LBoard.ranking, open("Dependencies/Interactions/leaderboard.pickle", "wb"))

    def wait_for_exit(self):
        while True:
            for event in pygame.event.get():
                # Check if game is being Quit
                if event.type == pygame.QUIT:
                    sys.exit()

if __name__ == "__main__":
    def set_windowSize():
        import ctypes
        # Get the screen resolution
        user32 = ctypes.windll.user32
        screenResolution = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        height = screenResolution[1]

        # Round height values down to the nearest multiple of 10
        height *= 0.9
        height = (int(height / 10)) * 10

        # Store the final window size
        if height >= 940:
            # Store the final window size
            windowSize = (1240, 940)  # (Width, Height)
            blockSize = 40
            status_panel_space = 100
        else:
            # Assign space for grid and space for status panel
            grid_space = height * 0.9
            status_panel_space = height - grid_space

            # Calculate the size that each grid block should be
            blockSize = int(grid_space / 21)
            width = blockSize * 31
            windowSize = (width, height)
        return windowSize

    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (10, 40)
    # Initialize pygame
    pygame.init()
    windowSize = set_windowSize()
    gameDisplay = pygame.display.set_mode(windowSize)
    gameDisplay.fill([255, 255, 255])  # Fill game display white
    GameOver(gameDisplay, windowSize, 2)
