from settings import *

ICONS_PATH = 'data/graphics/icons/'

class Inventory:
    def __init__(self, position, size, n):
        self.position = position
        self.size = size
        self.n = n
        self.items = [None for i in range(self.n)]
        self.current_item_index = 0
        self.current_item = self.items[self.current_item_index]
        self.alpha = 128

    def render(self, scale=1):
        for i in range(self.n):
            size = [self.size[0]*scale, self.size[1]*scale]
            x, y = [self.position[0]+(size[0]*i)+(10*i), self.position[1]]

            surface = pygame.Surface(size)
            surface.set_colorkey(colors['black'])
            surface.set_alpha(self.alpha)

            if self.current_item_index == i:
                pygame.draw.rect(surface, colors['yellow'], (0, 0, size[0], size[1]), border_radius=4)
            else:
                pygame.draw.rect(surface, (90, 105, 136), (0, 0, size[0], size[1]), border_radius=4)

            screen.blit(surface, (x, y))

            if self.items[i]:
                image = pygame.image.load(ICONS_PATH+self.items[i]+'.png')
                image = pygame.transform.scale(image, (image.get_width()*scale, image.get_height()*scale))
                screen.blit(image, [x+size[0]/2-image.get_width()/2, y+size[1]/2-image.get_height()/2])

    def add_item(self, filename):
        done = False
        index = 0
        while not done:
            if not self.items[index]:
                self.items[index] = filename
                if self.current_item_index == index:
                    self.current_item = filename
                done = True
            else:
                index += 1

                if index >= self.n:
                    done = True
