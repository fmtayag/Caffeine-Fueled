# Caffeine Fueled
# An adventure into the cosmos
# Programming by: zyenapz
    # E-maiL: zyenapz@gmail.com
    # Website: zyenapz.github.io
# Pygame version: Pygame 2.0.0 (SDL 2.0.12, python 3.7.9)

# Metadata
TITLE = "Caffeine Fueled"
AUTHOR = "zyenapz"
EMAIL = "zyenapz@gmail.com"
WEBSITE = "zyenapz.github.io"

import pygame, os, sys
from pygame.locals import *
from random import randrange, choice, choices
from itertools import repeat
from data.scripts.sprites import Player, Obstacle, Hat, Pet, CoffeeOMeter, Text, Powerup, Particle, Shockwave
from data.scripts.scene import Scene, SceneManager
from data.scripts.config import *

pygame.init()

# Directories
GAME_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(GAME_DIR, "data")
FONT_DIR = os.path.join(DATA_DIR, "fonts")
IMG_DIR = os.path.join(DATA_DIR, "img")
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
        self.offset = repeat((0,0)) # For screen shake
        self.orig_gxspeed = 0
        self.global_xspeed = 3
        self.bg_layer1_x = 0
        self.bg_layer2_x = 0
        self.bg_layer3_x = 0
        self.moon_x = 0
        self.score = 0
        self.max_enemies = 2
        self.max_powerups = 1
        self.difficulty_ticks = 0
        self.difficulty_increase_delay = 7500
        self.difficulty_level = 0
        img_sc = 4    

        # Load Images =============================
        # Play area and stats area and other crap
        self.play_area = pygame.Surface((536, 440))
        self.stats_area = pygame.Surface((156, 440))
        self.color_correction = pygame.Surface((self.play_area.get_width(), self.play_area.get_height()))
        self.color_correction.set_alpha(10)
        self.border_img = load_png("border.png", IMG_DIR, img_sc)

        # Background
        self.bg_layer1_img = load_png("bg_layer1.png", IMG_DIR, img_sc)
        self.bg_layer1_rect = self.bg_layer1_img.get_rect()
        self.bg_layer2_img = load_png("bg_layer2.png", IMG_DIR, img_sc)
        self.bg_layer2_rect = self.bg_layer2_img.get_rect()
        self.bg_layer3_img = load_png("bg_layer3.png", IMG_DIR, img_sc)
        self.bg_layer3_rect = self.bg_layer3_img.get_rect()

        # Player
        player_imgs = {
            "NORMAL": {
                "MOVRIGHT": load_png("player1.png", IMG_DIR, img_sc),
                "IDLE": load_png("player2.png", IMG_DIR, img_sc),
                "MOVLEFT": load_png("player3.png", IMG_DIR, img_sc)
            },
            "SHIELDED": {
                "MOVRIGHT": load_png("player_shielded1.png", IMG_DIR, img_sc),
                "IDLE": load_png("player_shielded2.png", IMG_DIR, img_sc),
                "MOVLEFT": load_png("player_shielded3.png", IMG_DIR, img_sc)
            }    
        }
        hat_img = load_png("hat_phony.png", IMG_DIR, img_sc)
        pet_ing = load_png("pet_chiki.png", IMG_DIR, 3) # Testing

        # Obstacles
        kid_obstacle_imgs = [
            load_png("obstacle_kid1.png", IMG_DIR, img_sc),
            load_png("obstacle_kid2.png", IMG_DIR, img_sc)
        ]
        heli_obstacle_imgs = [
            load_png("obstacle_heli1.png", IMG_DIR, img_sc),
            load_png("obstacle_heli2.png", IMG_DIR, img_sc)
        ]
        obstacle_bird_imgs = [
            load_png("obstacle_bird1.png", IMG_DIR, img_sc),
            load_png("obstacle_bird2.png", IMG_DIR, img_sc)
        ]
        barry_obstacle_imgs = [
            load_png("obstacle_barry1.png", IMG_DIR, img_sc),
            load_png("obstacle_barry2.png", IMG_DIR, img_sc)
        ]
        crate_obstacle_imgs = [
            load_png("obstacle_crate1.png", IMG_DIR, img_sc),
            load_png("obstacle_crate2.png", IMG_DIR, img_sc)
        ]
        parasol_obstacle_img = [load_png("obstacle_parasol1.png", IMG_DIR, img_sc)]
        self.obstacle_imgs = [kid_obstacle_imgs, heli_obstacle_imgs, obstacle_bird_imgs, barry_obstacle_imgs, parasol_obstacle_img, crate_obstacle_imgs]

        # CoffeeOMeter
        coffee_meter_imgs = {
            "100": load_png("CoffeeOMeter1.png", IMG_DIR, img_sc),
            "90": load_png("CoffeeOMeter2.png", IMG_DIR, img_sc),
            "80": load_png("CoffeeOMeter3.png", IMG_DIR, img_sc),
            "70": load_png("CoffeeOMeter4.png", IMG_DIR, img_sc),
            "60": load_png("CoffeeOMeter5.png", IMG_DIR, img_sc),
            "50": load_png("CoffeeOMeter6.png", IMG_DIR, img_sc),
            "40": load_png("CoffeeOMeter7.png", IMG_DIR, img_sc),
            "30": load_png("CoffeeOMeter8.png", IMG_DIR, img_sc),
            "20": load_png("CoffeeOMeter9.png", IMG_DIR, img_sc),
            "10": load_png("CoffeeOMeter10.png", IMG_DIR, img_sc),
        }

        # ShieldOMeter
        shield_meter_imgs = {
            "2": load_png("ShieldOMeter1.png", IMG_DIR, img_sc),
            "1": load_png("ShieldOMeter2.png", IMG_DIR, img_sc),
            "0": load_png("ShieldOMeter3.png", IMG_DIR, img_sc)
        }

        # Powerup
        self.powerup_imgs = {
            "fuel": load_png("powerup_fuel.png", IMG_DIR, img_sc),
            "shield": load_png("powerup_shield.png", IMG_DIR, img_sc)
        }
        
        # Sprite groups
        self.sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.texts = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()
        self.moving_stuff = pygame.sprite.Group() # this group is just for detecting overlapping sprites in the spawning functions

        # Player
        self.player = Player(player_imgs)
        self.hat = Hat(hat_img, self.player, img_sc, img_sc * 6) # normal y-offset is: img_sc * 2, phony hat is img_sc * 6, howl hat is img_sc * 3
        self.pet = Pet(pet_ing, self.player)
        self.coffee_o_meter = CoffeeOMeter(coffee_meter_imgs, (16, 32), "100", "10")
        self.shield_o_meter = CoffeeOMeter(shield_meter_imgs, (16, WIN_SZ[1] / 2), "2", "0", False)

        self.text_stats = Text(self.stats_area.get_width() / 2, 16, "Stats", GAME_FONT, 28, 'white')
        self.text_scorelabel = Text(self.stats_area.get_width() / 2, self.stats_area.get_height() / 2.6, "Score", GAME_FONT, 28, 'white')
        self.text_score = Text(self.stats_area.get_width() / 2, self.stats_area.get_height() / 2.2, f"{str(self.score).zfill(5)}", GAME_FONT, 28, 'white')
        self.texts.add(self.text_stats)
        self.texts.add(self.text_scorelabel)
        self.texts.add(self.text_score)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Debug only
                if event.key == pygame.K_e:
                    self.global_xspeed += 0.25
                    #self.player.speedx = self.global_xspeed + 1
                    print(self.global_xspeed)
                if event.key == pygame.K_q:
                    self.orig_gxspeed = self.global_xspeed
                    self.global_xspeed = 1

    def update(self):
        
        # Update crap
        self.update_difficulty()
        self.score += 0.1
        self.player.fuel -= 0.1 + (self.global_xspeed // 15)
        self.text_score.text = f"{str(round(self.score)).zfill(5)}"

        if self.player.fuel > 0 and not self.player.is_dead:
            hits = pygame.sprite.spritecollide(self.player, self.enemies, False, pygame.sprite.collide_rect_ratio(0.7))
            for hit in hits:
                self.offset = self.shake(10,5)
                self.spawn_particles(self.sprites, self.particles, hit.rect.centerx, hit.rect.centery, ['white'], 10)
                self.spawn_shockwave(hit.rect.centerx, hit.rect.centery, 'white')
                if self.player.shield <= 0:
                    self.player.is_dead = True
                else:
                    self.player.shield -= 1
                
                hit.kill()

        # Check for powerup collisions
        if not self.player.is_dead:
            hits = pygame.sprite.spritecollide(self.player, self.powerups, False, pygame.sprite.collide_rect_ratio(1))
            for hit in hits:

                self.spawn_particles(self.sprites, self.particles, self.player.rect.centerx, self.player.rect.centery, ['green'], 10)
                self.spawn_shockwave(self.player.rect.centerx, self.player.rect.centery, 'green')

                if hit.type == "fuel":
                    self.player.fuel += 20
                    if self.player.fuel > 100:
                        self.player.fuel = 100
                elif hit.type == "shield":
                    self.player.shield += 1
                    if self.player.shield > 2:
                        self.player.shield = 2
                hit.kill()

        # Update background and parallax x position
        self.bg_layer1_x -= self.global_xspeed / 4
        self.bg_layer2_x -= self.global_xspeed / 2
        self.bg_layer3_x -= self.global_xspeed

        # Spawn enemies
        if len(self.enemies) < self.max_enemies:
            self.spawn_enemies()

        # Spawn powerups
        if len(self.powerups) < self.max_powerups:
            self.spawn_powerup()
        
        # Move enemies
        for sprite in self.enemies:
            sprite.rect.x -= self.global_xspeed

        # Move powerups
        for sprite in self.powerups:
            sprite.rect.x -= self.global_xspeed

        # Check for boundary collision
        if self.player.rect.top < 0:
            self.player.rect.top = 0
            self.player.speedy = 1
        if self.player.rect.top > self.play_area.get_height() and self.player.fuel > 0 and not self.player.is_dead:
            self.player.is_dead = True
        if self.player.rect.left < 0:
            self.player.rect.left = 0
        if self.player.rect.right > self.play_area.get_width():
            self.player.rect.right = self.play_area.get_width()

        self.sprites.update()
        self.player.update()
        self.texts.update()
        self.hat.update()
        self.pet.update()
        self.coffee_o_meter.update(self.player.fuel)
        self.shield_o_meter.update(self.player.shield)

    def draw(self, window):
        window.fill('black')
        window.blit(self.play_area, (32,32))
        window.blit(self.stats_area, (WIN_SZ[0] / 1.3, 32))
        self.stats_area.fill('black')
        self.play_area.fill('black')
        window.blit(window, next(self.offset))

        self.draw_background(self.play_area, self.bg_layer1_img, self.bg_layer1_rect, self.bg_layer1_x, "horizontal")
        self.draw_background(self.play_area, self.bg_layer2_img, self.bg_layer2_rect, self.bg_layer2_x, "horizontal")
        self.draw_background(self.play_area, self.bg_layer3_img, self.bg_layer3_rect, self.bg_layer3_x, "horizontal")

        self.sprites.draw(self.play_area)
        self.player.draw(self.play_area)
        self.hat.draw(self.play_area)
        self.pet.draw(self.play_area)
        self.play_area.blit(self.border_img, (0,0))
        self.play_area.blit(self.color_correction, (0,0))

        self.coffee_o_meter.draw(self.stats_area)
        self.shield_o_meter.draw(self.stats_area)
        self.texts.draw(self.stats_area)
        pygame.draw.rect(self.color_correction, (0,0,255), (0,0,self.play_area.get_width(), self.play_area.get_height()))

    def spawn_enemies(self):
        o = Obstacle(choice(self.obstacle_imgs), self.play_area)
        # Spawn only non-overlapping sprites
        if not pygame.sprite.spritecollide(o, self.moving_stuff, False, pygame.sprite.collide_rect_ratio(2)):
            self.sprites.add(o)
            self.enemies.add(o)
            self.moving_stuff.add(o)
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

    def spawn_powerup(self):
        p = Powerup(self.powerup_imgs, self.play_area)
        # Spawn only non-overlapping sprites
        if not pygame.sprite.spritecollide(p, self.moving_stuff, False, pygame.sprite.collide_rect_ratio(2)):
            self.sprites.add(p)
            self.powerups.add(p)
            self.moving_stuff.add(p)
        else:
            del p

    def spawn_particles(self, sprites, particles, x, y, colors, amount):
        for _ in range(amount):
            p = Particle(x, y, colors)
            particles.add(p)
            sprites.add(p)

    def spawn_shockwave(self, x, y, color):
        s = Shockwave(x, y, color, 128)
        self.sprites.add(s)

    def shake(self, intensity, n):
        # Credits to sloth from StackOverflow, thanks buddy!
        shake = -1
        for _ in range(n):
            for x in range(0, intensity, 5):
                yield (x*shake, 0)
            for x in range(intensity, 0, 5):
                yield (x*shake, 0)
            shake *= -1
        while True:
            yield (0, 0)

    def update_difficulty(self):
        self.difficulty_ticks += 10
        if self.difficulty_ticks >= self.difficulty_increase_delay and self.difficulty_level != 10:
            self.difficulty_ticks = 0
            if self.difficulty_level < 5:
                self.max_enemies += 1
            if self.difficulty_level < 1:
                self.max_powerups += 1
            self.global_xspeed += 0.10
            self.player.speedx = self.global_xspeed
            self.difficulty_level += 1

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
