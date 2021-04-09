from settings import *
from .funcs import *

class Projectile:
    def __init__(self, targets, position, size, damage, timer):
        self.targets = targets
        self.rect = pygame.Rect(*position, *size)
        self.damage = damage
        self.timer = timer
        self.destroyed = False

    #Checks for collision with the targets
    def update(self):
        self.timer -= 1

        if self.timer <= 0:
            self.destroyed = True
            return

        for target in self.targets:
            if rect_rect_collision(self.rect, target.rect):
                target.damage(self.damage)
                self.destroyed = True
