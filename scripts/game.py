from .world import *
from .menus.restart import Restart_Menu
from .menus.start import Start_Menu

class Game:
    def __init__(self):
        self.world = World(self)
        self.start_menu = Start_Menu(self)
        self.restart_menu = Restart_Menu(self)
        pygame.mouse.set_visible(False)

    #Restarts the level
    def restart_level(self):
        self.world.respawn_player()
        self.run_game(self.world.level)

    #Runs the start menu
    def run_start_menu(self):
        self.start_menu.main_loop()

    #Runs the restart level menu
    def run_restart_menu(self):
        self.restart_menu.main_loop()

    #Runs the game itself
    def run_game(self, level=1):
        self.world.main_loop(level)

    #Runs the start menu at the beginning
    def main_loop(self):
        self.run_start_menu()
