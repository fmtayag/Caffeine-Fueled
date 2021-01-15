# Jetpack Game
# An adventure into the cosmos
# Programming by: zyenapz
    # E-maiL: zyenapz@gmail.com
    # Website: zyenapz.github.io
# Pygame version: Pygame 2.0.0 (SDL 2.0.12, python 3.7.9)

# Metadata
TITLE = "Jetpack Game"
AUTHOR = "zyenapz"
EMAIL = "zyenapz@gmail.com"
WEBSITE = "zyenapz.github.io"

import pygame, os, sys
from pygame.locals import *
from random import randrange, choice, choices
from itertools import repeat
from data.scripts.sprites import Player, Obstacle, Hat, Pet
from data.scripts.scene import Scene, SceneManager
from data.scripts.config import *

pygame.init()

# Directories
GAME_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(GAME_DIR, "data")
FONT_DIR = os.path.join(DATA_DIR, "fonts")
GAME_FONT = os.path.join(FONT_DIR, "prstartk.ttf")

# Functions
def load_png(file, directory, scale, convert_alpha=False):
    try:
        path = os.path.join(directory, file)
        if not convert_alpha:
            img = pygame.image.load(path).convert_alpha()
        else:
            img = pygame.image.load(path).convert()
            transColor = img.get_at((0,0))
            img.set_colorkey(transColor)
        img_w = img.get_width()
        img_h = img.get_height()
        img = pygame.transform.scale(img, (img_w*scale, img_h*scale))
        return img
    except Exception as e:
        print(e)
        exit()

class GameScene(Scene):
    def __init__(self):
        # Settings
        self.global_xspeed = 3
        self.background_x = 0
        self.parallax_x = 0
        img_sc = 4

        # Load Images
        self.play_area = pygame.Surface((536, 448))
        self.background_img = load_png("background.png", GAME_DIR, img_sc)
        self.background_rect = self.background_img.get_rect()
        self.parallax_img = load_png("parallax.png", GAME_DIR, img_sc)
        self.parallax_rect = self.parallax_img.get_rect()
        #self.sun_img = load_png("sun.png", GAME_DIR, img_sc)
        player_imgs = {
            "MOVRIGHT": load_png("player1.png", GAME_DIR, img_sc),
            "IDLE": load_png("player2.png", GAME_DIR, img_sc),
            "MOVLEFT": load_png("player3.png", GAME_DIR, img_sc)
        }
        hat_img = load_png("dimadome_hat.png", GAME_DIR, img_sc)
        pet_ing = load_png("copyright_pet.png", GAME_DIR, 3) # Testing
        kid_obstacle_imgs = [
            load_png("obstacle_kid1.png", GAME_DIR, img_sc),
            load_png("obstacle_kid2.png", GAME_DIR, img_sc)
        ]
        heli_obstacle_imgs = [
            load_png("obstacle_heli1.png", GAME_DIR, img_sc),
            load_png("obstacle_heli2.png", GAME_DIR, img_sc)
        ]
        obstacle_bird_imgs = [
            load_png("obstacle_bird1.png", GAME_DIR, img_sc),
            load_png("obstacle_bird2.png", GAME_DIR, img_sc)
        ]
        barry_obstacle_imgs = [
            load_png("obstacle_barry1.png", GAME_DIR, img_sc),
            load_png("obstacle_barry2.png", GAME_DIR, img_sc)
        ]
        crate_obstacle_imgs = [
            load_png("obstacle_crate1.png", GAME_DIR, img_sc),
            load_png("obstacle_crate2.png", GAME_DIR, img_sc)
        ]
        parasol_obstacle_img = [load_png("obstacle_parasol1.png", GAME_DIR, img_sc)]
        self.obstacle_imgs = [kid_obstacle_imgs, heli_obstacle_imgs, obstacle_bird_imgs, barry_obstacle_imgs, parasol_obstacle_img, crate_obstacle_imgs]
        self.player = Player(player_imgs)
        self.hat = Hat(hat_img, self.player, img_sc, img_sc * 2)
        self.pet = Pet(pet_ing, self.player)

        # Sprite groups
        self.sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Debug only
                if event.key == pygame.K_e:
                    self.global_xspeed += 1
                    print(self.global_xspeed)
                if event.key == pygame.K_q:
                    self.spawn_enemies()

    def update(self):
        
        # Update background and parallax x position
        self.background_x -= self.global_xspeed / 3
        self.parallax_x -= self.global_xspeed

        # Spawn enemies
        if len(self.enemies) < 5:
            self.spawn_enemies()

        # Move enemies
        for sprite in self.enemies:
            sprite.rect.x -= self.global_xspeed

        # Check for boundary collision
        if self.player.rect.top < 0:
            self.player.speedy = 1
        if self.player.rect.left < 0:
            self.player.rect.left = 0
        if self.player.rect.right > self.play_area.get_width():
            self.player.rect.right = self.play_area.get_width()

        self.sprites.update()
        self.player.update()
        self.hat.update()
        self.pet.update()

    def draw(self, window):
        window.fill('black')
        window.blit(self.play_area, (32,32))
        self.play_area.fill('black')
        #self.play_area.blit(self.sun_img, (0,0))
        self.draw_background(self.play_area, self.background_img, self.background_rect, self.background_x, "horizontal")
        self.draw_background(self.play_area, self.parallax_img, self.parallax_rect, self.parallax_x, "horizontal")
        self.sprites.draw(self.play_area)
        self.player.draw(self.play_area)
        self.hat.draw(self.play_area)
        self.pet.draw(self.play_area)
        pygame.draw.rect(self.play_area, 'white', (0,0,self.play_area.get_width(), self.play_area.get_height()), 16)

    def spawn_enemies(self):
        o = Obstacle(choice(self.obstacle_imgs), self.play_area)
        # Spawn only non-overlapping sprites
        if not pygame.sprite.spritecollide(o, self.enemies, False, pygame.sprite.collide_rect_ratio(2.5)):
            self.sprites.add(o)
            self.enemies.add(o)
        else:
            del o

    def draw_background(self, surf, img, img_rect, pos, direction="vertical"):
        if direction == "vertical":
            surf_h = surf.get_height()
            rel_y = pos % img_rect.height
            surf.blit(img, (0, rel_y - img_rect.height))

            if rel_y < surf_h:
                surf.blit(img, (0, rel_y))

        elif direction == "horizontal":
            surf_w = surf.get_width()
            rel_x = pos % img_rect.width
            surf.blit(img, (rel_x - img_rect.width, 0))

            if rel_x < surf_w:
                surf.blit(img, (rel_x, 0))

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
