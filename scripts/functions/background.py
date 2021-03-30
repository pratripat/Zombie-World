from settings import *

class Background:
    def __init__(self):
        self.image = pygame.transform.scale2x(pygame.image.load('data/graphics/background.png')).convert()

    def show(self):
        x = -scroll[0]*0.25
        y = height-self.image.get_height()-100-scroll[1]*0.25

        screen.fill(colors['background'])
        pygame.draw.rect(screen, colors['mountain'], (0, y+self.image.get_height(), screen.get_width(), screen.get_height()-y+self.image.get_height()))

        screen.blit(self.image, (x, y))

        while x+self.image.get_width() > 0:
            x -= self.image.get_width()
            screen.blit(self.image, (x, y))

        while x < screen.get_width():
            x += self.image.get_width()
            screen.blit(self.image, (x, y))
