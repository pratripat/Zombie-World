from scripts.functions.entity import Entity
from scripts.functions.funcs import *
from .inventory import Inventory
from settings import *
import json

class Player(Entity):
    def __init__(self, animations, position):
        super().__init__(animations, 'player', position, False, 'idle')
        self.speed = 6
        self.health = 100
        self.airtimer = 0
        self.coin_counter = 0
        self.invincible_timer = 0
        self.animations = animations
        self.inventory = Inventory([10, 10], [20, 20], 5)
        self.inventory.add_item('stick')
        self.inventory.add_item('hammer')
        self.inventory.add_item('sword')
        self.attacking = False

    def run(self, dt):
        self.movement()
        self.update(dt)
        self.render(screen, scroll, colors['black'])

        if self.invincible_timer > 0:
            self.invincible_timer -= 1

        self.inventory.render(3)

        if self.attacking:
            offset = [0,0]

            if self.flipped:
                offset[0] += self.image.get_width()

            self.attack_animation.render(screen, [self.position[0]-scroll[0]-offset[0], self.position[1]-scroll[1]-offset[1]], self.flipped, (0,0,0))
            self.attack_animation.run(dt)

            if self.attack_animation.frame == self.attack_animation.animation_data.duration():
                self.attack_animation.frame = 0
                self.attacking = False

    def movement(self):
        animation_state = 'idle'

        if self.collisions['bottom']:
            self.airtimer = 0
            self.velocity[1] = 0
        elif self.airtimer == 0:
            self.airtimer = 6

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

        if directions['down']:
            self.velocity[1] += gravity
        elif directions['up'] and not self.attacking and not self.invincible_timer > 0:
            if self.airtimer < 6:
                self.velocity[1] -= 3
                self.airtimer += 1
            else:
                directions['up'] = False
                directions['down'] = True

        self.velocity[1] = min(8, self.velocity[1])

        self.update_animations(animation_state)

    def update_animations(self, animation_state):
        if self.airtimer > 3:
            animation_state = 'jump'

        self.set_animation(animation_state)

    def render_ui(self):
        coin_image = pygame.image.load('data/graphics/animations/coin/0.png').convert()
        coin_image = pygame.transform.scale(coin_image, (coin_image.get_width()*3, coin_image.get_height()*3))
        coin_image.set_colorkey((0,0,0))
        screen.blit(coin_image, (10, 80))
        font.render(screen, f': {self.coin_counter}', (15+coin_image.get_width(), 80+coin_image.get_height()/2), scale=1.25, center=(False, True), color=colors['yellow'])

    def attack(self):
        if self.inventory.current_item:
            if not self.attacking:
                self.attacking = True
                self.attack_animation = self.animations.get_animation(self.inventory.current_item)
        else:
            self.attacking = False

    def add_coin(self):
        self.coin_counter += 1

    def shift_current_item(self, i):
        self.inventory.current_item_index = i-1
        self.inventory.current_item = self.inventory.items[self.inventory.current_item_index]

    def attacks(self, enemies):
        if self.attacking:
            weapon_mask = self.attack_animation.mask

            for enemy in enemies:
                enemy_mask = enemy.current_animation.mask
                offset = [round(enemy.position[0]-self.position[0]), round(enemy.position[1]-self.position[1])]

                collision = mask_mask_collision(weapon_mask, enemy_mask, offset)

                if collision:
                    path = self.attack_animation.animation_data.path
                    id = (path.split('.png')[0]).split('/')[-1]
                    damage = json.load(open('data/configs/weapons_config.json', 'r'))[id]

                    invincible_timer = self.attack_animation.animation_data.duration()

                    knockback = -self.attack_animation.current_image.get_width()*2
                    if enemy.flipped:
                        knockback = self.attack_animation.current_image.get_width()*2

                    enemy.damage(damage, invincible_timer, knockback)

    def damage(self, damage, knockback):
        if self.invincible_timer == 0:
            self.health -= damage
            self.invincible_timer = 12
            self.velocity[0] += knockback
