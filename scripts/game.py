from settings import *
from .functions.funcs import *
from .functions.tilemap import TileMap
from .entities.player.player import Player
from .entities.zombie import Zombie
from .functions.animation_handler import Animation_Handler
from .functions.background import Background
from .functions.particle import Particle_System
from .coin import Coin
import sys

class Game:
    def __init__(self):
        self.level = 2
        self.tilemap = TileMap(f'data/levels/level{self.level}.json')
        self.tilemap.load_map()
        self.animation_handler = Animation_Handler()
        self.coins = [Coin([tile.x, tile.y], self.animation_handler.get_animation('coin')) for tile in self.tilemap.get_tiles('coin')]
        self.player = Player(self.animation_handler, [400, 100])
        self.zombies = [Zombie(self.animation_handler, [1200, 100])]
        self.background = Background()
        self.particle_system = Particle_System()

    @property
    def dt(self):
        fps = clock.get_fps()

        if fps:
            return 1/fps

        return 0

    def render_background(self):
        self.background.show()

    def render_tiles(self):
        for tile in self.tilemap.tiles:
            if tile['id'] == 'grass' or tile['id'] == 'tree' or tile['id'] == 'bush':
                x,y = tile['position'][0]-scroll[0],tile['position'][1]-scroll[1]
                image = tile['image']

                screen.blit(tile['image'], [x,y])

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.player.attack()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.player.shift_current_item(1)
                if event.key == pygame.K_2:
                    self.player.shift_current_item(2)
                if event.key == pygame.K_3:
                    self.player.shift_current_item(3)
                if event.key == pygame.K_4:
                    self.player.shift_current_item(4)
                if event.key == pygame.K_5:
                    self.player.shift_current_item(5)
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    directions['left'] = True
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    directions['right'] = True
                if event.key == pygame.K_w or event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                    directions['up'] = True
                    directions['down'] = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    directions['left'] = False
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    directions['right'] = False
                if event.key == pygame.K_w or event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                    directions['up'] = False
                    directions['down'] = True
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

    def run(self):
        scroll[0] += int((self.player.center[0]-scroll[0]-screen.get_width()/2)*self.dt*2)
        scroll[1] += int((self.player.center[1]-scroll[1]-screen.get_height()/2)*self.dt*2)

        collidables = self.tilemap.get_tiles('grass', 0)

        clock.tick(80)

        self.render_background()
        self.render_tiles()

        for coin in self.coins[:]:
            coin.run(self.dt)

            if rect_rect_collision(coin.rect, self.player.rect):
                self.coins.remove(coin)
                self.player.add_coin()
                self.particle_system.add_particles(coin.position, [0,-1], 10, 1, colors['yellow'], 255, 1, 5)

        for zombie in self.zombies[:]:
            zombie.move(collidables)
            zombie.run(self.dt, self.player)
            zombie.attacks(self.player)

            if zombie.dead():
                self.zombies.remove(zombie)
                self.particle_system.add_particles(zombie.center, [0,-1], 10, 0.3, colors['green'], 255, 1, 10)
                self.particle_system.add_particles(zombie.center, [0,-1], 10, 0.3, colors['red'], 255, 1, 20)

        self.player.move(collidables)
        self.player.run(self.dt)
        self.player.attacks(self.zombies)

        self.particle_system.run(screen, scroll, 0.1)
        self.player.render_ui()

    def main_loop(self):
        while True:
            self.event_loop()
            self.run()
            pygame.display.update()
