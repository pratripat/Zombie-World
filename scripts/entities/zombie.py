from settings import *
from scripts.functions.funcs import *
from scripts.functions.entity import Entity

class Zombie(Entity):
    def __init__(self, animations, position):
        super().__init__(animations, 'zombie', position, False, 'idle')
        self.directions = {k : False for k in ['up', 'right', 'down', 'left']}
        self.speed = 2
        self.health = 100
        self.attack_damage = 20
        self.invincible_timer = 0

    def run(self, dt, player):
        self.directions['down'] = True
        self.move_towards_player(player)
        self.movement()
        self.update(dt)
        self.render(screen, scroll, colors['black'])

        if self.invincible_timer > 0:
            self.invincible_timer -= 1

        if player.position[0] < self.position[0]:
            self.flip(True)
        else:
            self.flip(False)

    def movement(self):
        animation_state = 'idle'

        if self.directions['left']:
            self.velocity[0] -= 1
            self.velocity[0] = max(-self.speed, self.velocity[0])
            self.flip(True)
            animation_state = 'run'
        elif self.directions['right']:
            self.velocity[0] += 1
            self.velocity[0] = min(self.velocity[0], self.speed)
            self.flip(False)
            animation_state = 'run'
        else:
            self.velocity[0] = 0

        if self.directions['down']:
            self.velocity[1] += gravity

        self.velocity[1] = min(8, self.velocity[1])
        self.directions = {k : False for k in ['up', 'right', 'down', 'left']}

        self.update_animations(animation_state)

    def update_animations(self, animation_state):
        if self.invincible_timer > 0:
            animation_state = 'damage'

        self.set_animation(animation_state)

    def move_towards_player(self, player):
        if not self.invincible_timer > 0:
            if player.position[0] < self.position[0]:
                self.directions['left'] = True
            elif player.position[0] > self.position[0]:
                self.directions['right'] = True

    def damage(self, damage, invincible_timer, knockback):
        if self.invincible_timer == 0:
            self.health -= damage
            self.invincible_timer = invincible_timer*2
            self.velocity[0] += knockback

    def attacks(self, player):
        zombie_mask = pygame.mask.from_surface(self.current_animation.current_image)
        player_mask = pygame.mask.from_surface(player.current_animation.current_image)
        offset = [round(player.position[0]-self.position[0]), round(player.position[1]-self.position[1])]

        if mask_mask_collision(zombie_mask, player_mask, offset):
            knockback = self.current_animation.current_image.get_width()*2
            if self.flipped:
                knockback = -self.current_animation.current_image.get_width()*2

            player.damage(self.attack_damage, knockback)
            self.invincible_timer = 12

    def dead(self):
        return self.health <= 0
