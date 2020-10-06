from Dependencies.maze_gen_recursive import make_maze_recursion
import pygame
import copy


class maze(pygame.sprite.Sprite):
    def __init__(self, blockSize, gameDisplay, backGround):
        pygame.sprite.Sprite.__init__(self)
        self.grid = make_maze_recursion(31,21)

        self.blockSize = blockSize
        self.gameDisplay = gameDisplay
        self.backGround = backGround

        self.image = pygame.image.load('Dependencies/Images/gridBlock.png')
        self.image = pygame.transform.scale(self.image, (self.blockSize,self.blockSize))
        self.wall_image = pygame.image.load('Dependencies/Images/wallBlock.png')
        self.wall_image = pygame.transform.scale(self.wall_image, (self.blockSize, self.blockSize))
        self.hero_image = pygame.image.load('Dependencies/Images/hero.png')
        self.hero_image = pygame.transform.scale(self.hero_image, (self.blockSize, self.blockSize))
        self.monster_image = pygame.image.load('Dependencies/Images/monster.png')
        self.monster_image = pygame.transform.scale(self.monster_image, (self.blockSize, self.blockSize))
        self.goblin_image = pygame.image.load('Dependencies/Images/goblin.png')
        self.goblin_image = pygame.transform.scale(self.goblin_image, (self.blockSize, self.blockSize))
        self.chest_image = pygame.image.load('Dependencies/Images/chest.png')
        self.chest_image = pygame.transform.scale(self.chest_image, (self.blockSize, self.blockSize))
        self.rect = self.image.get_rect()

    def drawGrid(self):
        self.gameDisplay.blit(self.backGround.image, self.backGround.rect)
        self.rect.left, self.rect.top = [0, self.blockSize * -1]
        for index in self.grid:
            self.rect.top += self.blockSize
            self.rect.right = 0
            for i in index:
                self.rect.left += self.blockSize
                if i == 0:
                    self.gameDisplay.blit(self.image, self.rect)  # Draw onto the window
                elif i == "H" or i == "H/M":
                    self.gameDisplay.blit(self.hero_image, self.rect)
                elif i == "M" or i == "G/M" or i == "C/M":
                    self.gameDisplay.blit(self.monster_image, self.rect)
                elif i == "G":
                    self.gameDisplay.blit(self.goblin_image, self.rect)
                elif i == "C":
                    self.gameDisplay.blit(self.chest_image, self.rect)
                else:
                    self.gameDisplay.blit(self.wall_image, self.rect)  # Draw onto the window

    def copyGrid(self):
        self.grid_copy = copy.deepcopy(self.grid)
        row = -1
        for index in self.grid_copy:
            row += 1
            column = 0
            for i in index:
                if i == 'G':
                    self.grid_copy[row][column] = 0
                column +=1

    def set_coord(self, x, y, v):
        self.grid[y][x] = v

    def count_free_spaces(self):
        """Called from gameCharacters.find_spawn_location
        Objective - Count 0's on the grid"""
        count = 0
        for row in self.grid:
            for i in row:
                if i == 0:
                    count += 1
        return count

    def __str__(self):
        for index in self.grid:
            print("\n", end = "")
            for i in index:
                print(i, end=" ")
        return ("")
