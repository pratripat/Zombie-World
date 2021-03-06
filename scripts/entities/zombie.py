from settings import *
from scripts.functions.funcs import *
from scripts.functions.entity import Entity
from scripts.functions.projectile import Projectile

class Zombie(Entity):
    def __init__(self, animations, position):
        super().__init__(animations, 'zombie', position, False, 'idle')
        self.directions = {k : False for k in ['up', 'right', 'down', 'left']}
        self.speed = 2
        self.health = 100
        self.attack_damage = 10
        self.movement_timer = 30
        self.invincible_timer = 0
        self.attack_timer = 30

        self.damage_sound_effect = pygame.mixer.Sound('data/sfx/damage.wav')
        self.damage_sound_effect.set_volume(0.7)

    #Updates and moves the zombie towards the player
    def run(self, dt, player):
        self.directions['down'] = True
        if self.movement_timer <= 0:
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

        if self.movement_timer > 0:
            self.movement_timer -= 1

    #Moves the zombie
    def movement(self):
        animation_state = 'idle'

        #Horizontal movement
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

        #Gravity only (zombies do not jump in this game)
        if self.directions['down']:
            self.velocity[1] += gravity

        #Limiting velocity
        self.velocity[1] = min(8, self.velocity[1])

        self.directions = {k : False for k in ['up', 'right', 'down', 'left']}

        self.update_animations(animation_state)

    #Sets animation of the zombie
    def update_animations(self, animation_state):
        if self.invincible_timer > 0:
            animation_state = 'damage'

        self.set_animation(animation_state)

    #Sets movement towards the player if the zombie is on screen
    def move_towards_player(self, player):
        if not self.invincible_timer > 0 and self.on_screen(player):
            if player.position[0] < self.position[0]:
                self.directions['left'] = True
            elif player.position[0] > self.position[0]:
                self.directions['right'] = True

    #Reduces health
    def damage(self, damage):
        if self.invincible_timer == 0:
            self.damage_sound_effect.play()
            self.health -= damage
            self.invincible_timer = 24

    #Adds projectile against the player
    def attacks(self, player):
        self.attack_timer -= 1

        if self.attack_timer == 0:
            zombie_image = self.current_animation.image
            projectiles.append(Projectile([player], self.position, zombie_image.get_size(), self.attack_damage, 5))
            self.attack_timer = 30

    #Returns if the zombie's health is 0
    def dead(self):
        return self.health <= 0

    #Returns if zombie can be seen by the player
    def on_screen(self, player):
        return (
            abs(self.center[0]-player.center[0]) < 900 and
            abs(self.center[1]-player.center[1]) < 900 and
            self.center[0]-scroll[0] > 0 and self.center[0]-scroll[0] < screen.get_width() and
            self.center[1]-scroll[1] > 0 and self.center[1]-scroll[1] < screen.get_height()
        )
