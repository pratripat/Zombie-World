import sys

from settings import *
from .functions.funcs import *
from .functions.tilemap import TileMap
from .functions.animation_handler import Animation_Handler
from .functions.background import Background
from .functions.particle import Particle_System
from .entities.player import Player
from .entities.zombie import Zombie
from .entities.coin import Coin
from .entities.door import Door

class World:
    def __init__(self, game):
        self.game = game
        self.world_max_height = 2500

        self.animation_handler = Animation_Handler()
        self.background = Background()
        self.particle_system = Particle_System()

        self.cursor_image = pygame.image.load('data/graphics/images/cursor.png')
        self.cursor_image = pygame.transform.scale2x(self.cursor_image)

        self.zombie_kill_sound_effect = pygame.mixer.Sound('data/sfx/zombie_kill.wav')
        self.coin_pickup_sound_effect = pygame.mixer.Sound('data/sfx/coin.wav')

    @property
    def dt(self):
        fps = clock.get_fps()

        if fps != 0:
            return 1/fps

        return 0

    #Renders all the times from tilemap
    def render_tiles(self):
        for tile in self.tilemap.tiles:
            if tile['id'] == 'grass' or tile['id'] == 'tree' or tile['id'] == 'bush':
                x,y = tile['position'][0]-scroll[0],tile['position'][1]-scroll[1]
                image = tile['image']

                screen.blit(image, (x,y))

    #Event loop
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.player.attack()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    self.load_level(False)
                if event.key == pygame.K_m:
                    self.game.run_start_menu()

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

    #Runs all the entities and collision with the projectiles and particles and renders the screen
    def run(self):
        scroll[0] += int((self.player.center[0]-scroll[0]-screen.get_width()/2)*self.dt*2)
        scroll[1] += int((self.player.center[1]-scroll[1]-screen.get_height()/2)*self.dt*2)

        clock.tick(80)

        self.background.show(screen, scroll)
        self.render_tiles()

        if self.door:
            self.door.show()

            if rect_rect_collision(self.player.rect, self.door.rect):
                self.level += 1
                self.fade_out()
                self.load_level()

        for coin in self.coins[:]:
            coin.run(self.dt)

            if rect_rect_collision(coin.rect, self.player.rect):
                self.coins.remove(coin)
                self.player.add_coin()
                self.particle_system.add_particles(coin.position, [0,-1], 10, 1, colors['yellow'], 255, 1, 5)

                self.coin_pickup_sound_effect.play()

        for zombie in self.zombies[:]:
            zombie.move(self.collidables, self.dt)
            zombie.run(self.dt, self.player)
            zombie.attacks(self.player)

            if zombie.position[1] > self.world_max_height:
                zombie.health = 0

            if zombie.dead():
                self.zombies.remove(zombie)
                self.particle_system.add_particles(zombie.center, [0,1], 10, 0.3, colors['green'], 255, 1, 5)
                self.particle_system.add_particles(zombie.center, [0,1], 10, 0.3, colors['red'], 255, 1, 10)
                self.player.coin_counter += 10

                self.zombie_kill_sound_effect.play()

        if self.player.position[1] > self.world_max_height:
            self.player.health = 0

        self.player.move(self.collidables, self.dt)
        self.player.run(self.dt, self.particle_system)
        self.player.attacks(self.zombies)

        self.particle_system.run(screen, scroll, 0.1)

        self.render_ui()

        for projectile in projectiles[:]:
            projectile.update()

            if projectile.destroyed:
                projectiles.remove(projectile)

        screen.blit(self.cursor_image, (pygame.mouse.get_pos()[0]-self.cursor_image.get_width()/2, pygame.mouse.get_pos()[1]-self.cursor_image.get_height()/2))

        pygame.display.update()

        if self.game_over():
            self.finished = True
            self.game.run_restart_menu()

    #Renders the ui
    def render_ui(self):
        for word in self.text:
            text, position = word
            font.render(screen, text, [position[0]-scroll[0]+2, position[1]-scroll[1]+2], center=[True, True], scale=2, color=colors['red'])
            font.render(screen, text, [position[0]-scroll[0], position[1]-scroll[1]], center=[True, True], scale=2, color=colors['light_red'])

        position = [10, 30]
        offset = [0,0]
        #Level number
        font.render(screen, 'Level: '+str(self.level), position, scale=1.3, color=colors['dark_yellow'])
        font.render(screen, 'Level: '+str(self.level), [position[0]-2, position[1]-2], scale=1.3, color=colors['yellow'])
        offset[1] += 50

        #Health bar
        screen.blit(self.player.health_bar_image, (position[0]+offset[0]-2, position[1]+offset[1]-2))
        pygame.draw.rect(screen, colors['light_red'], (position[0]+offset[0], position[1]+offset[1], 100, 20))
        pygame.draw.rect(screen, colors['light_green'], (position[0]+offset[0], position[1]+offset[1], self.player.health, 20))
        offset[1] += 40

        #Coins collected
        screen.blit(self.player.coin_image, (position[0]+offset[0], position[1]+offset[1]))
        offset[0] += self.player.coin_image.get_width()+5
        offset[1] += self.player.coin_image.get_height()/2
        font.render(screen, f': {self.player.coin_counter}', (position[0]+offset[0]+2, position[1]+offset[1]+2), scale=1.25, center=(False, True), color=colors['dark_yellow'])
        font.render(screen, f': {self.player.coin_counter}', (position[0]+offset[0], position[1]+offset[1]), scale=1.25, center=(False, True), color=colors['yellow'])

        position = [10, height-80]
        font.render(screen, 'r: restart level', [position[0]+2, position[1]+2], center=[False, True], color=colors['dark_yellow'])
        font.render(screen, 'r: restart level', position, center=[False, True], color=colors['yellow'])

        offset = [0, 40]
        font.render(screen, 'm: menu', [position[0]+offset[0]+2, position[1]+offset[1]+2], center=[False, True], color=colors['dark_yellow'])
        font.render(screen, 'm: menu', [position[0]+offset[0], position[1]+offset[1]], center=[False, True], color=colors['yellow'])

    #Starts the game
    def main_loop(self, level):
        self.level = level
        self.finished = False
        pygame.mixer.music.load('data/music/game_music.wav')
        pygame.mixer.music.play(-1)
        self.load_level()

        while not self.finished:
            self.event_loop()
            self.run()

    #Returns if the player is dead
    def game_over(self):
        return self.player.dead()

    #Fading of the screen (level transition)
    def fade_out(self):
        n = 0
        surface = screen.copy()

        while n < 255:
            surface.fill((0,0,0))
            surface.set_alpha(n)
            screen.blit(surface, (0,0))
            pygame.display.update()
            n += 1

    #Respawns the player in the level
    def respawn_player(self):
        player_tile = self.tilemap.get_tiles('player')[0]
        self.player = Player(self.animation_handler, [player_tile.x, player_tile.y])
        self.player.health = self.player_data['health']
        self.player.coin_counter = self.player_data['coin']
        self.player.healing_timer = self.player_data['healing_timer']

    #Loads the level and all the necessary entities
    def load_level(self, update_player_data=True):
        if self.level == 1:
            self.text = [['arrow keys or w, a, d keys to move.', [600, 100]],
                         ['click to attack.', [3800, -200]]]
            self.player_data = {'health':100, 'coin':0, 'healing_timer': 60}
        else:
            self.text = [['', [0,0]]]

            if update_player_data:
                self.player_data = {'health':self.player.health, 'coin':self.player.coin_counter, 'healing_timer': self.player.healing_timer}

        try:
            data = open(f'data/levels/level{self.level}.json', 'r')
            self.tilemap = TileMap(f'data/levels/level{self.level}.json')
            self.tilemap.load_map()
        except:
            self.tilemap = TileMap(f'data/levels/final_level.json')
            self.tilemap.load_map()
            self.text = [['thank you for playing!', [1000, 300]]]

            pygame.mixer.music.load('data/music/end.wav')
            pygame.mixer.music.play(-1)

        self.particle_system.clear()

        directions['left'] = directions['right'] = directions['up'] = False
        directions['down'] = True

        coin_tiles = self.tilemap.get_tiles('coin')
        zombie_tiles = self.tilemap.get_tiles('zombie')
        player_tile = self.tilemap.get_tiles('player')[0]
        self.coins = [Coin([tile.x, tile.y], self.animation_handler.get_animation('coin')) for tile in coin_tiles]
        self.zombies = [Zombie(self.animation_handler, [tile.x, tile.y]) for tile in zombie_tiles]
        self.player = Player(self.animation_handler, [player_tile.x, player_tile.y])
        self.player.health = self.player_data['health']
        self.player.coin_counter = self.player_data['coin']
        self.player.healing_timer = self.player_data['healing_timer']

        self.collidables = self.tilemap.get_tiles('grass', 0)

        door_tile = self.tilemap.get_tiles('door')
        if len(door_tile):
            door_tile = door_tile[0]
            self.door = Door([door_tile.x, door_tile.y], [door_tile.w, door_tile.h])
        else:
            self.door = None

        scroll[0] = self.player.center[0]-screen.get_width()/2
        scroll[1] = self.player.center[1]-screen.get_height()/2
