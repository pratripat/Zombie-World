from settings import *

class Coin:
    def __init__(self, position, animation):
        self.position = position
        self.animation = animation

    def run(self, dt):
        self.animation.render(screen, [self.position[0]-scroll[0], self.position[1]-scroll[1]], False, (0,0,0))
        self.animation.run(dt)

    @property
    def rect(self):
        return pygame.Rect(*self.position, *self.animation.current_image.get_size())
