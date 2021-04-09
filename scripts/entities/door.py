from settings import *

class Door:
    def __init__(self, position, size):
        self.image = pygame.image.load('data/graphics/images/door.png')
        self.image = pygame.transform.scale(self.image, size)
        self.position = position
        self.rect = pygame.Rect(*self.position, *self.image.get_size())

    #Renders the door image at position
    def show(self):
        screen.blit(self.image, [self.position[0]-scroll[0], self.position[1]-scroll[1]])
