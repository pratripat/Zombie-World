from settings import *
from scripts.functions.button import Button
import sys

class Restart_Menu:
    def __init__(self, game):
        self.game = game

        self.cursor_image = pygame.image.load('data/graphics/images/cursor.png')
        self.cursor_image = pygame.transform.scale2x(self.cursor_image)

        self.restart_button = Button({'x':screen.get_width()/2, 'y':screen.get_height()/2, 'w':120, 'h':50},
        {'color':colors['yellow'], 'hover_color':colors['green'], 'font_color':(0,0,1), 'alpha':30},
        {'text':'restart', 'font_renderer':font})
        self.menu_button = Button({'x':screen.get_width()/2, 'y':screen.get_height()/2+70, 'w':120, 'h':50},
        {'color':colors['yellow'], 'hover_color':colors['green'], 'font_color':(0,0,1), 'alpha':30},
        {'text':'menu', 'font_renderer':font})

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
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.restart_button.on_click(self.game.restart_level)
                    self.menu_button.on_click(self.game.run_start_menu)

    #Renders the background, the buttons and the cursor image
    def render_screen(self):
        surface = pygame.Surface(screen.get_size())
        surface.fill(colors['red'])
        surface.set_alpha(10)

        screen.blit(surface, (0,0))

        font.render(screen, 'you died...', [screen.get_width()/2, 200], center=(True, False), scale=2, color=(0,0,1))

        screen.blit(self.cursor_image, (pygame.mouse.get_pos()[0]-self.cursor_image.get_width()/2, pygame.mouse.get_pos()[1]-self.cursor_image.get_height()/2))

    #Runs the event loop and renders the screen
    def run(self):
        self.event_loop()
        self.render_screen()

        self.restart_button.show(border_radius=10)
        self.menu_button.show(border_radius=10)
        self.restart_button.update()
        self.menu_button.update()

        pygame.display.update()

    #Runs the "run" function continuously
    def main_loop(self):
        pygame.mixer.music.load('data/music/restart_menu_music.wav')
        pygame.mixer.music.play(1)
        self.running = True
        while self.running:
            self.run()
