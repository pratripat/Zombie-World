from scripts.functions.entity import Entity
from scripts.functions.projectile import Projectile
from scripts.functions.funcs import *
from settings import *
import json

class Player(Entity):
    def __init__(self, animations, position):
        super().__init__(animations, 'player', position, False, 'idle')
        self.speed = 6
        self.airtimer = 0
        self.coin_counter = 0
        self.invincible_timer = 0
        self.movement_timer = 30
        self.healing_timer = 30
        self.health = self.max_health = 100

        self.animations = animations
        self.attack_animation = self.animations.get_animation('sword')
        self.attack_timer = self.attack_animation.animation_data.duration()
        self.attacking = False

        #UI elements
        self.health_bar_image = pygame.image.load('data/graphics/images/health_bar.png')
        self.coin_image = pygame.image.load('data/graphics/animations/coin/0.png')
        self.coin_image = pygame.transform.scale(self.coin_image, (self.coin_image.get_width()*3, self.coin_image.get_height()*3))
        self.coin_image.set_colorkey((0,0,0))

        #player sfx
        self.jump_sound_effect = pygame.mixer.Sound('data/sfx/jump.wav')
        self.attack_sound_effect = pygame.mixer.Sound('data/sfx/sword.wav')
        self.damage_sound_effect = pygame.mixer.Sound('data/sfx/damage.wav')

        self.attack_sound_effect.set_volume(0.7)

    def run(self, dt, particle_system):
        #Renders and updates itself, if the player is not dead
        if not self.dead():
            #Movement timer at the beginning of the level
            if self.movement_timer <= 0:
                self.movement(dt, particle_system)

            self.update(dt)
            self.render(screen, scroll, colors['black'])

            if self.invincible_timer > 0:
                self.invincible_timer -= 1

            #Renders the attack animation
            if self.attacking:
                offset = [0,0]

                if self.flipped:
                    offset[0] += self.image.get_width()

                self.attack_animation.render(screen, [self.position[0]-scroll[0]-offset[0], self.position[1]-scroll[1]-offset[1]], self.flipped, (0,0,0))
                self.attack_animation.run(dt)

                if self.attack_animation.frame == self.attack_animation.animation_data.duration():
                    self.attack_animation.frame = 0
                    self.attacking = False

        if self.movement_timer > 0:
            self.movement_timer -= 1

        if self.healing_timer > 0 and self.health < self.max_health:
            self.healing_timer -= dt

        #Heals the player at regular intervals
        if self.healing_timer <= 0:
            self.health += 20

            if self.health > self.max_health:
                self.health = self.max_health

            self.healing_timer = 30

    def movement(self, dt, particle_system):
        animation_state = 'idle'

        if self.collisions['bottom']:
            self.airtimer = 0
            self.velocity[1] = 0
        elif self.airtimer == 0:
            self.airtimer = 6

        #Sets the velocity of the player horizontally
        if directions['left'] and (not self.attacking or self.airtimer > 3) and not self.invincible_timer > 0:
            self.velocity[0] -= 1
            self.velocity[0] = max(-self.speed, self.velocity[0])
            self.flip(True)
            animation_state = 'run'
        elif directions['right'] and (not self.attacking or self.airtimer > 3) and not self.invincible_timer > 0:
            self.velocity[0] += 1
            self.velocity[0] = min(self.velocity[0], self.speed)
            self.flip(False)
            animation_state = 'run'
        else:
            self.velocity[0] = 0

        #Gravity
        if directions['down']:
            self.velocity[1] += gravity
        #Jump
        elif directions['up'] and not self.attacking and not self.invincible_timer > 0:
            if self.airtimer < 6:
                self.velocity[1] -= 3
                self.airtimer += 1
                particle_system.add_particles([self.center[0], self.position[1]+self.image.get_height()], [0,-1], 6, 3, colors['brown'], 255, 2, 5)

                if self.airtimer == 1:
                    self.jump_sound_effect.play()

            #If player is at max height, setting the upward movement false and allowing player to fall
            else:
                directions['up'] = False
                directions['down'] = True

        #Setting limit to player's velocity
        self.velocity[1] = min(8, self.velocity[1])

        self.update_animations(dt, animation_state)

    #Sets player animation
    def update_animations(self, dt, animation_state):
        if self.airtimer > 3:
            animation_state = 'jump'

        self.set_animation(animation_state)

    #Sets attacking attribute to true
    def attack(self):
        if not self.attacking:
            self.attacking = True
            self.attack_sound_effect.play()

    #Adds coin to counter
    def add_coin(self):
        self.coin_counter += 1

    #Adds projectile at position and sets the zombies as the enemies (the ones who will get hurt from the projectile)
    def attacks(self, enemies):
        if self.attack_timer > 0:
            self.attack_timer -= 1

        if self.attacking and self.attack_timer == 0:
            weapon_image = self.attack_animation.image

            if self.flipped:
                offset = self.image.get_width()
            else:
                offset = 0

            projectiles.append(Projectile(enemies, [self.position[0]-offset, self.position[1]], weapon_image.get_size(), 20, self.attack_animation.animation_data.duration()))
            self.attack_timer = self.attack_animation.animation_data.duration()

    #Reduces player health
    def damage(self, damage):
        if self.invincible_timer == 0:
            self.damage_sound_effect.play()
            self.health -= damage
            self.invincible_timer = 12

    #Returns if player health is 0
    def dead(self):
        return self.health <= 0
