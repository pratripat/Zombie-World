from settings import *
from scripts.functions.button import Button
from scripts.functions.background import Background
import sys

class Start_Menu:
    def __init__(self, game):
        self.game = game

        self.cursor_image = pygame.image.load('data/graphics/images/cursor.png')
        self.background_image = pygame.image.load('data/graphics/images/background_image.png')
        self.cursor_image = pygame.transform.scale2x(self.cursor_image)
        self.background_image.set_colorkey(colors['black'])

        self.background = Background()
        self.play_button = Button({'x':screen.get_width()/2, 'y':screen.get_height()/2, 'w':120, 'h':50},
        {'color':colors['red'], 'hover_color':colors['green'], 'font_color':(0,0,1), 'alpha':200},
        {'text':'play', 'font_renderer':font})

    #Event loop
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_RETURN:
                    self.game.run_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.play_button.on_click(self.game.run_game)

    #Runs all the functions and renders the screen
    def run(self):
        self.background.show(screen, [0,0])
        screen.blit(self.background_image, (screen.get_width()/2-self.background_image.get_width()/2, screen.get_height()/2-self.background_image.get_height()/2))

        font.render(screen, 'zombie world', [screen.get_width()/2+2,102], center=[True, True], scale=3, color=colors['red'])
        font.render(screen, 'zombie world', [screen.get_width()/2+1,101], center=[True, True], scale=3, color=colors['green'])
        font.render(screen, 'zombie world', [screen.get_width()/2,100], center=[True, True], scale=3, color=colors['light_red'])

        self.play_button.hover()
        self.play_button.show(border_radius=10)

        screen.blit(self.cursor_image, (pygame.mouse.get_pos()[0]-self.cursor_image.get_width()/2, pygame.mouse.get_pos()[1]-self.cursor_image.get_height()/2))

        pygame.display.update()

    #Runs the "run" function continuously
    def main_loop(self):
        pygame.mixer.music.load('data/music/start_menu_music.wav')
        pygame.mixer.music.play(-1)
        self.running = True
        while self.running:
            self.event_loop()
            self.run()
