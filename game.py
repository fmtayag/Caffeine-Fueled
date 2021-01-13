# Final Frontier
# An adventure into the cosmos
# Programming by: zyenapz
    # E-maiL: zyenapz@gmail.com
    # Website: zyenapz.github.io
# Pygame version: Pygame 2.0.0 (SDL 2.0.12, python 3.7.9)

# Metadata
TITLE = "Final Frontier"
AUTHOR = "zyenapz"
EMAIL = "zyenapz@gmail.com"
WEBSITE = "zyenapz.github.io"

import pygame, os, sys
from pygame.locals import *
from random import randrange, choice, choices
from itertools import repeat
from data.scripts.scene import Scene, SceneManager
from data.scripts.actors import Crew, Ship
from data.scripts.config import *

pygame.init()

# Directories
GAME_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(GAME_DIR, "data")

class GameScene(Scene):
    def __init__(self):
        self.STATES = ("PAUSED", "UNPAUSED")
        self.crews_alive = list()
        self.crews_dead = list()
        self.the_ship = Ship("IMG_NOT_AVAILABLE")
        self.day = 1

        # Test adding
        c1 = Crew("IMG_NOT_AVAILABLE", {"name": "francis", "gender": "male", "personality": "greedy", "role": "medic"})
        self.crews_alive.append(c1)

    def handle_events(self, events):
        pass

    def update(self):
        pass

    def draw(self, windows):
        pass

# Application loop
def main():

    # Initialize the window
    window = pygame.display.set_mode(WIN_SZ, HWSURFACE|DOUBLEBUF)
    pygame.display.set_caption(TITLE)
    pygame.mouse.set_cursor(*pygame.cursors.tri_left)

    # Loop
    running = True
    manager = SceneManager(GameScene())
    clock = pygame.time.Clock()
    FPS = 60

    while running:
        
        clock.tick(FPS)
        
        if pygame.event.get(QUIT):
            running = False

        manager.scene.handle_events(pygame.event.get())
        manager.scene.update()
        manager.scene.draw(window)

        pygame.display.flip()
    
# Run the application loop
main()

# Exit pygame and application
pygame.quit()
sys.exit()
