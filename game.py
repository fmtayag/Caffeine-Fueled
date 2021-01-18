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
from data.scripts.sprites import Player, Obstacle, Hat, Pet, CoffeeOMeter, Text, Powerup, Particle, Shockwave, JetpackTrail
from data.scripts.scene import Scene, SceneManager
from data.scripts.config import *

pygame.init()

# Directories
GAME_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(GAME_DIR, "data")
FONT_DIR = os.path.join(DATA_DIR, "fonts")
IMG_DIR = os.path.join(DATA_DIR, "img")
GAME_FONT = os.path.join(FONT_DIR, "prstartk.ttf")

# GameData

class GameData:
    equipped_pet = "none"
    owned_pets = [

    ]
    equipped_hat = "none"
    owned_hats = [
        
    ]
    coins = 1000
    highscore = 0

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

class TitleScene(Scene):
    def __init__(self):
        pass

    def handle_events(self, events):
        self.manager.go_to(ShopScene())

    def update(self):
        pass

    def draw(self, window):
        pass

class ShopScene(Scene):
    def __init__(self):
        print(GameData.highscore, GameData.coins)
        self.coins = 1000
        self.init_x = 16
        self.init_y = 16
        self.x_offset = 64 + self.init_x 
        self.y_offset = 64 + self.init_y
        self.pet_files = [
            'pet_cat.png', 
            'pet_chiki.png', 
            'pet_coffee.png', 
            'pet_copyright.png', 
            'pet_fish.png', 
            'pet_skull.png', 
            'pet_stealbucks.png'
        ]
        self.hat_files = [
            'hat_dimadome.png',
            'hat_howl.png',
            'hat_leprechaun.png',
            'hat_phony.png',
            'hat_santa.png',
            'hat_swag.png',
            'hat_ushanka.png'
        ]
        self.pet_imgs = self.load_items(self.pet_files)
        self.hat_imgs = self.load_items(self.hat_files)
        #print(self.hat_imgs)
        self.selector_x = 16
        self.selector_y = 16
        if GameData.equipped_pet != "none":
            self.pet_equipped_x = 16 + (80 * self.pet_files.index(GameData.equipped_pet))
            #self.row_break = len(self.all_pets) // 2
        if GameData.equipped_hat != "none":
            self.hat_equipped_x = 16 + (80 * self.hat_files.index(GameData.equipped_hat))
        self.cur_pet = 0
        self.cur_hat = 0
        self.item_cost = 30
        
        # Surfaces
        self.pets_area = pygame.Surface((WIN_SZ[0] / 1.33, 96))
        self.hats_area = pygame.Surface((WIN_SZ[0] / 1.33, 96))
        self.cur_shop = self.hats_area

        # Sprite groups
        self.texts = pygame.sprite.Group()

        # Texts
        self.text_shoplabel = Text(WIN_SZ[0] / 5, 64, "Shop", GAME_FONT, 48, 'white')
        self.text_coins = Text(WIN_SZ[0] / 1.4, 75, f"C{GameData.coins}", GAME_FONT, 32, 'yellow')
        self.text_isbought = Text(WIN_SZ[0] / 5, 400, "Bought", GAME_FONT, 32, 'white', False)
        self.text_cost = Text(WIN_SZ[0] / 5, 400, f"Cost {self.item_cost}", GAME_FONT, 32, 'white', False)
        self.texts.add(self.text_shoplabel)
        self.texts.add(self.text_coins)
        self.texts.add(self.text_isbought)
        self.texts.add(self.text_cost)

    def handle_events(self, events):
        # YandereDev-esque code here. Beware!
        for event in events:
            if event.type == pygame.KEYDOWN:

                if self.cur_shop == self.pets_area:
                    if event.key == pygame.K_d and self.cur_pet < len(self.pet_files) - 1:
                        self.selector_x += 64 + self.init_x
                        self.cur_pet += 1
                    if event.key == pygame.K_a and self.cur_pet > 0:
                        self.selector_x -= 64 + self.init_x
                        self.cur_pet -= 1
                elif self.cur_shop == self.hats_area:
                    if event.key == pygame.K_d and self.cur_hat < len(self.hat_files) - 1:
                        self.selector_x += 64 + self.init_x
                        self.cur_hat += 1
                    if event.key == pygame.K_a and self.cur_hat > 0:
                        self.selector_x -= 64 + self.init_x
                        self.cur_hat -= 1

                if event.key == pygame.K_RETURN:
                    if self.cur_shop == self.pets_area:
                        if self.pet_files[self.cur_pet] in GameData.owned_pets:
                            if GameData.equipped_pet == self.pet_files[self.cur_pet]:
                                GameData.equipped_pet = "none"
                            else:
                                GameData.equipped_pet = self.pet_files[self.cur_pet]
                                self.pet_equipped_x = self.selector_x
                        else:
                            if GameData.coins >= self.item_cost:
                                GameData.equipped_pet = self.pet_files[self.cur_pet]
                                self.pet_equipped_x = self.selector_x
                                GameData.owned_pets.append(self.pet_files[self.cur_pet])
                                GameData.coins -= self.item_cost
                                self.text_coins.text = f"C{GameData.coins}"
                            else:
                                self.text_coins.color = 'red'
                    elif self.cur_shop == self.hats_area:
                        if self.hat_files[self.cur_hat] in GameData.owned_hats:
                            if GameData.equipped_hat == self.hat_files[self.cur_hat]:
                                GameData.equipped_hat = "none"
                            else:
                                GameData.equipped_hat = self.hat_files[self.cur_hat]
                                self.hat_equipped_x = self.selector_x
                        else:
                            if GameData.coins >= self.item_cost:
                                GameData.equipped_hat = self.hat_files[self.cur_hat]
                                self.hat_equipped_x = self.selector_x
                                GameData.owned_hats.append(self.hat_files[self.cur_hat])
                                GameData.coins -= self.item_cost
                                self.text_coins.text = f"C{GameData.coins}"
                            else:
                                self.text_coins.color = 'red'

                if event.key == pygame.K_w:
                    self.cur_shop = self.pets_area
                    self.cur_pet = 0
                    self.selector_x = 16

                if event.key == pygame.K_s:
                    self.cur_shop = self.hats_area
                    self.cur_hat = 0
                    self.selector_x = 16

                if event.key == pygame.K_ESCAPE:
                    self.manager.go_to(GameScene()) # DEBUG ONLY

                #print(self.pet_files[self.cur_pet])
                #print(self.pet_files[self.cur_pet] in Game_Data.owned_pets)
        #print("Pet Equipped: " + GameData.equipped_pet)
        #print("Hat Equipped:" + GameData.equipped_hat)
        #print(self.cur_pet, self.cur_hat)

    def update(self):
        
        if self.pet_files[self.cur_pet] in GameData.owned_pets:
            self.text_isbought.visible = True
            self.text_cost.visible = False
        else:
            self.text_isbought.visible = False
            self.text_cost.visible = True

        self.texts.update()

    def draw(self, window):
        self.draw_items(self.pets_area, self.pet_imgs)
        self.draw_items(self.hats_area, self.hat_imgs)
        window.fill('black')
        window.blit(self.pets_area, (64,128))
        window.blit(self.hats_area, (64,256))
        self.pets_area.fill('black')
        self.hats_area.fill('black')
        pygame.draw.rect(self.cur_shop, 'white', (self.selector_x, self.selector_y, 64, 64), 8) # this is the selector
        pygame.draw.rect(self.pets_area, 'white', (0,0, self.pets_area.get_width(), self.pets_area.get_height()), 8, 8, 8, 8)
        pygame.draw.rect(self.hats_area, 'white', (0,0, self.hats_area.get_width(), self.hats_area.get_height()), 8, 8, 8, 8)

        if GameData.equipped_pet != "none":
            pygame.draw.rect(self.pets_area, 'yellow', (self.pet_equipped_x, self.init_y, 64, 64), 8)
        if GameData.equipped_hat != "none":
            pygame.draw.rect(self.hats_area, 'yellow', (self.hat_equipped_x, self.init_y, 64, 64), 8)
        self.texts.draw(window)

    def load_items(self, files):
        images = list()
        for f in files:
            images.append(load_png(f, IMG_DIR, 4))

        return images

    def draw_items(self, surface, imgs):
        x = self.init_x
        y = self.init_y
        cur_col = 0

        for pet in imgs:
            surface.blit(pet, (x,y))
            x += self.x_offset
            cur_col += 1
            #if cur_col > self.row_break:
                #cur_col = 0
                #x = self.init_x
                #y += self.y_offset + self.init_y

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
        self.coins = 0
        self.max_enemies = 2
        self.max_powerups = 1
        self.difficulty_ticks = 0
        self.difficulty_increase_delay = 7500
        self.difficulty_level = 0
        self.debug_mode = False
        self.start_delay = 3000
        self.exit_ticks = 0
        self.can_exit = False
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

        if GameData.equipped_pet != "none":
            pet_ing = load_png(GameData.equipped_pet, IMG_DIR, 3)
        if GameData.equipped_hat != "none":
            hat_img = load_png(GameData.equipped_hat, IMG_DIR, img_sc)

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
            "shield": load_png("powerup_shield.png", IMG_DIR, img_sc),
            "coin": load_png("powerup_coin.png", IMG_DIR, img_sc)
        }
        
        # Sprite groups
        self.sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.texts = pygame.sprite.Group()
        self.texts_pa = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()
        self.trails = pygame.sprite.Group()
        self.moving_stuff = pygame.sprite.Group() # this group is just for detecting overlapping sprites in the spawning functions

        # Player
        self.player = Player(player_imgs)
        if GameData.equipped_pet != "none":
            self.pet = Pet(pet_ing, self.player)
        if GameData.equipped_hat != "none":
            self.hat = Hat(hat_img, self.player, img_sc, img_sc * 6)
        
        # Stats texts
        self.text_stats = Text(self.stats_area.get_width() / 2, 0, "Stats", GAME_FONT, 28, 'white')
        self.coffee_o_meter = CoffeeOMeter(coffee_meter_imgs, (16, 0), "100", "10")
        self.text_scorelabel = Text(self.stats_area.get_width() / 2, self.stats_area.get_height() / 3.8, "Score", GAME_FONT, 28, 'white')
        self.text_score = Text(self.stats_area.get_width() / 2, self.stats_area.get_height() / 3, f"{str(self.score).zfill(5)}", GAME_FONT, 28, 'white')
        self.shield_o_meter = CoffeeOMeter(shield_meter_imgs, (16, WIN_SZ[1] / 2.8), "2", "0", False)
        self.text_coinslabel = Text(self.stats_area.get_width() / 2, self.stats_area.get_height() / 1.4, "Coins", GAME_FONT, 28, 'yellow')
        self.text_coins = Text(self.stats_area.get_width() / 2, self.stats_area.get_height() / 1.27, f"{str(self.coins).zfill(5)}", GAME_FONT, 28, 'yellow')
        self.texts.add(self.text_stats)
        self.texts.add(self.text_scorelabel)
        self.texts.add(self.text_score)
        self.texts.add(self.text_coinslabel)
        self.texts.add(self.text_coins)

        # Play area text(s)
        self.text_gameover = Text(self.play_area.get_width() / 2, self.play_area.get_height() / 4, "GAME OVER!", GAME_FONT, 48, 'white', False)
        self.text_finalscore = Text(self.play_area.get_width() / 2, self.play_area.get_height() / 2.4, "SCORE 00000", GAME_FONT, 32, 'white', False)
        self.text_finalcoin = Text(self.play_area.get_width() / 2, self.play_area.get_height() / 2, "COINS 00000", GAME_FONT, 32, 'white', False)
        self.text_exitbutton = Text(self.play_area.get_width() / 2, self.play_area.get_height() / 1.4, "[X] Exit", GAME_FONT, 32, 'white', False)
        self.texts_pa.add(self.text_gameover)
        self.texts_pa.add(self.text_finalscore)
        self.texts_pa.add(self.text_finalcoin)
        self.texts_pa.add(self.text_exitbutton)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Debug only
                if event.key == pygame.K_e and self.debug_mode:
                    self.global_xspeed += 0.25
                    #self.player.speedx = self.global_xspeed + 1
                    print(self.global_xspeed)
                if event.key == pygame.K_q and self.debug_mode:
                    self.orig_gxspeed = self.global_xspeed
                    self.global_xspeed = 1

                if event.key == pygame.K_x and self.can_exit:
                    GameData.coins += self.coins
                    if round(self.score) > GameData.highscore:
                        GameData.highscore = round(self.score)
                    self.manager.go_to(TitleScene())

    def update(self):
        
        # Update crap
        if self.player.has_started and not self.player.is_dead:
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
            hits = pygame.sprite.spritecollide(self.player, self.powerups, False, pygame.sprite.collide_rect_ratio(0.7))
            for hit in hits:

                self.spawn_particles(self.sprites, self.particles, self.player.rect.centerx, self.player.rect.centery, [(124,231,20)], 10)
                self.spawn_shockwave(self.player.rect.centerx, self.player.rect.centery, (124,231,20))

                if hit.type == "fuel":
                    self.player.fuel += 20
                    if self.player.fuel > 100:
                        self.player.fuel = 100
                elif hit.type == "shield":
                    self.player.shield += 1
                    if self.player.shield > 2:
                        self.player.shield = 2
                elif hit.type == "coin":
                    self.coins += 1
                    self.text_coins.text = f"{str(self.coins).zfill(5)}"
                hit.kill()

        # Update background and parallax x position
        self.bg_layer1_x -= self.global_xspeed / 4
        self.bg_layer2_x -= self.global_xspeed / 2
        self.bg_layer3_x -= self.global_xspeed

        if self.player.has_started:
            # Spawn enemies
            if len(self.enemies) < self.max_enemies:
                self.spawn_enemies()

            # Spawn powerups
            if len(self.powerups) < self.max_powerups:
                self.spawn_powerup()

        # Spawn trail
        if len(self.trails) < 64 and self.player.fuel > 0:
            self.spawn_trail(self.player.rect.left + 10, self.player.rect.centery, ['white'], 8)
            
        # Move enemies
        for sprite in self.enemies:
            sprite.rect.x -= self.global_xspeed

        # Move powerups
        for sprite in self.powerups:
            sprite.rect.x -= self.global_xspeed

        if self.player.has_started:
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

        # Do things when player dies
        if self.player.is_dead:
            self.exit_ticks += 10
            self.text_gameover.visible = True

            if self.exit_ticks > 500:
                self.text_finalscore.visible = True
                self.text_finalcoin.visible = True
                self.text_finalscore.text = "Score " + str(round(self.score))
                self.text_finalcoin.text = "Coin " + str(self.coins)
                self.text_exitbutton.visible = True
                self.can_exit = True

        self.sprites.update()
        self.player.update()
        self.texts.update()
        self.texts_pa.update()
        if GameData.equipped_pet != "none":
            self.pet.update()
        if GameData.equipped_hat != "none":
            self.hat.update()
        self.coffee_o_meter.update(self.player.fuel)
        self.shield_o_meter.update(self.player.shield)

    def draw(self, window):
        window.fill('black')
        window.blit(self.play_area, (32,32))
        window.blit(self.stats_area, (WIN_SZ[0] / 1.3, 64))
        self.stats_area.fill('black')
        self.play_area.fill('black')
        window.blit(window, next(self.offset))

        self.draw_background(self.play_area, self.bg_layer1_img, self.bg_layer1_rect, self.bg_layer1_x, "horizontal")
        self.draw_background(self.play_area, self.bg_layer2_img, self.bg_layer2_rect, self.bg_layer2_x, "horizontal")
        self.draw_background(self.play_area, self.bg_layer3_img, self.bg_layer3_rect, self.bg_layer3_x, "horizontal")

        self.sprites.draw(self.play_area)
        self.player.draw(self.play_area)
        if GameData.equipped_pet != "none":
            self.pet.draw(self.play_area)
        if GameData.equipped_hat != "none":
            self.hat.draw(self.play_area)
        self.play_area.blit(self.border_img, (0,0))
        self.play_area.blit(self.color_correction, (0,0))

        self.coffee_o_meter.draw(self.stats_area)
        self.shield_o_meter.draw(self.stats_area)
        self.texts.draw(self.stats_area)
        self.texts_pa.draw(self.play_area)
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
        if self.difficulty_ticks >= self.difficulty_increase_delay and self.difficulty_level != 20:
            self.difficulty_ticks = 0
            if self.difficulty_level < 5:
                self.max_enemies += 1
            if self.difficulty_level < 1:
                self.max_powerups += 1
            self.global_xspeed += 0.10
            self.player.speedx = self.global_xspeed
            self.difficulty_level += 1
            if self.difficulty_increase_delay > 2500:
                self.difficulty_increase_delay -= 500
            #print(self.difficulty_level, self.difficulty_increase_delay)

    def spawn_trail(self, x, y, colors, amount):
        for _ in range(amount):
            t = JetpackTrail(x, y, colors)
            self.trails.add(t)
            self.sprites.add(t)

# Application loop
def main():

    # Initialize the window
    window = pygame.display.set_mode(WIN_SZ, HWSURFACE|DOUBLEBUF)
    pygame.display.set_caption(TITLE)
    pygame.mouse.set_cursor(*pygame.cursors.tri_left)

    # Loop
    running = True
    #manager = SceneManager(GameScene())
    manager = SceneManager(ShopScene())
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
