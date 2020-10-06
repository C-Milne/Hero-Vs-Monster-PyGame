import pygame


class DialogBox(pygame.sprite.Sprite):
    stockImage = pygame.image.load('Dependencies/Images/Text_Bar.png')

    def __init__(self, windowSize):
        pygame.sprite.Sprite.__init__(self)

        # Scale image
        self.image = pygame.transform.scale(self.stockImage, (int(windowSize[0] * 0.5), int(windowSize[1] * 0.2)))
        self.Rect = self.image.get_rect()
        self.font = pygame.font.SysFont('Arial', 20)
        self.image_width, self.image_height = self.Rect.size

        # Get usable width (so text is inside the inner section)
        self.usableWidth = self.image_width * 0.95

    def blitme(self, gameDisplay):
        # Blit the image in the top left corner of the screen
        gameDisplay.blit(self.image, self.Rect)

        # Blit the text ontop of the image
        text_lines = self.text.split("\n")
        if len(text_lines) == 1:
            line_val = 1/2
        else:
            line_val = 1/4
        for line in text_lines:
            text_width, text_height = self.font.size(line)
            text = self.font.render(line, True, (0, 0, 0))

            text_rect = text.get_rect()
            text_rect.left = self.Rect.left + (self.image_width - text_width)/2
            text_rect.top = self.Rect.top + (self.image_height - text_height) * line_val

            line_val *= 3
            gameDisplay.blit(text, text_rect)

    def set_text(self, text):
        self.text = text

    def set_rect_left(self, coord):
        self.Rect.left = coord

    def set_rect_top(self, coord):
        self.Rect.top = coord

    def set_rect_right(self, coord):
        self.Rect.right = coord

    def set_rect_bottom(self, coord):
        self.Rect.bottom = coord
