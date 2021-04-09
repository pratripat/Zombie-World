import pygame

PATH = 'data/graphics/images/'

class Background:
    def __init__(self):
        self.mountain_image = pygame.transform.scale2x(pygame.image.load(PATH+'mountain.png')).convert()
        self.cloud_image = pygame.transform.scale2x(pygame.image.load(PATH+'cloud.png')).convert_alpha()

    #Renders the same images until they fill the screen
    def render_image(self, x, y, amount, image, screen, scroll):
        image.set_colorkey((0,0,0))

        x -= scroll[0]*amount
        y -= scroll[1]*amount

        screen.blit(image, (x,y))

        while x+image.get_width() > 0:
            x -= image.get_width()
            screen.blit(image, (x, y))

        while x < screen.get_width():
            x += image.get_width()
            screen.blit(image, (x, y))

    #Draws the mountain and cloud image on the screen
    def show(self, screen, scroll):
        screen.fill((44,232,245))
        pygame.draw.rect(screen, (38, 43, 68), (0, (400-scroll[1]*0.2)+self.mountain_image.get_height(), screen.get_width(), screen.get_height()-(400-scroll[1]*0.2)+self.mountain_image.get_height()))

        self.render_image(0, 400, 0.2, self.mountain_image, screen, scroll)
        self.render_image(0, 70, 0.4, self.cloud_image, screen, scroll)
