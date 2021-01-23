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

import pygame, os, sys, pickle
from pygame.locals import *
from random import randrange, choice, choices
from itertools import repeat
from data.scripts.sprites import Player, Obstacle, Hat, Pet, CoffeeOMeter, Text, Powerup, Particle, Shockwave, JetpackTrail
from data.scripts.scene import Scene, SceneManager
from data.scripts.config import *

pygame.init()
pygame.mixer.init()

# Directories
GAME_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(GAME_DIR, "data")
FONT_DIR = os.path.join(DATA_DIR, "fonts")
IMG_DIR = os.path.join(DATA_DIR, "img")
SFX_DIR = os.path.join(DATA_DIR, "sfx")
GAME_FONT = os.path.join(FONT_DIR, "prstartk.ttf")

# GameData
class GameData:
    def __init__(self):
        self.equipped_pet = "none"
        self.owned_pets = []
        self.equipped_hat = "none"
        self.owned_hats = []

        # Stats for nerds
        self.coins = 0
        self.highscore = 0
        self.times_died = 0
        self.times_hit = 0
        self.times_fuelpickup = 0
        self.times_shieldpickup = 0
        self.play_time = 0

# Load game data
infile = open(os.path.join(DATA_DIR, "user_data.dat"), "rb")
game_data = pickle.load(infile)
infile.close()

# Functions
def load_sound(filename, sfx_dir, volume):
    path = os.path.join(sfx_dir, filename)
    snd = pygame.mixer.Sound(path)
    snd.set_volume(volume)
    return snd

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

# Load sounds ====================
select_sfx = load_sound("select.wav", SFX_DIR, 0.6)
enter_sfx = load_sound("enter.wav", SFX_DIR, 0.6)
buy_sfx = load_sound("buy.wav", SFX_DIR, 0.6)
denied_sfx = load_sound("denied.wav", SFX_DIR, 0.8)
explosion_sfx = load_sound("explosion.wav", SFX_DIR, 0.5)

class TitleScene(Scene):
    def __init__(self):
        # Booleans
        self.help_available = False
        self.stats_available = False

        # Surfaces
        self.menu_area = pygame.Surface((256, 280))
        self.menu_area_rect = self.menu_area.get_rect()
        self.menu_area_rect.centerx = WIN_SZ[0] / 2
        self.menu_area_rect.y = 200
        self.logo_img = load_png("logo.png", IMG_DIR, 4)
        self.help_area = pygame.Surface((300, 450))
        self.help_img = load_png("help.png", IMG_DIR, 4)
        self.stats_area = pygame.Surface((300, 450))
        self.dev_img = load_png("dev_info.png", IMG_DIR, 4)

        self.bg_layer1_x = 0
        self.bg_layer2_x = 0
        self.bg_layer3_x = 0

        self.bg_layer1_img = load_png("title_bg_layer1.png", IMG_DIR, 4)     
        self.bg_layer1_rect = self.bg_layer1_img.get_rect()
        self.bg_layer2_img = load_png("title_bg_layer2.png", IMG_DIR, 4)
        self.bg_layer2_rect = self.bg_layer2_img.get_rect()
        self.bg_layer3_img = load_png("title_bg_layer3.png", IMG_DIR, 4)
        self.bg_layer3_rect = self.bg_layer3_img.get_rect()

        # Selector
        self.y_offset = 32
        self.selector_width = 6
        self.selector_y = -self.selector_width + self.y_offset
        self.cur_sel = 0

        # Sprite groups
        self.statstexts = pygame.sprite.Group()
        self.helptexts = pygame.sprite.Group()
        self.optiontexts = pygame.sprite.Group()

        # Texts for menu
        #self.text_title = Text(self.menu_area.get_width() / 2, self.menu_area.get_height () / 8, "CAFFEINE", GAME_FONT, 48, 'white')
        self.text_play = Text(self.menu_area.get_width() / 2, 0 + self.y_offset, "PLAY", GAME_FONT, 34, 'white')
        self.text_shop = Text(self.menu_area.get_width() / 2, 45 + self.y_offset, "SHOP", GAME_FONT, 32, 'yellow')
        self.text_stats = Text(self.menu_area.get_width() / 2, 90 + self.y_offset, "STATS", GAME_FONT, 32, 'white')
        self.text_help = Text(self.menu_area.get_width() / 2, 135 + self.y_offset, "HELP", GAME_FONT, 32, 'white')
        self.text_quit = Text(self.menu_area.get_width() / 2, 180 + self.y_offset, "QUIT", GAME_FONT, 32, 'white')
        #self.texts.add(self.text_title)
        self.optiontexts.add(self.text_play)
        self.optiontexts.add(self.text_shop)
        self.optiontexts.add(self.text_stats)
        self.optiontexts.add(self.text_help)
        self.optiontexts.add(self.text_quit)

        # Texts for help area
        self.text_help = Text(0, 0, "HELP", GAME_FONT, 32, 'white')
        self.text_help.rect = (16,16)
        self.helptexts.add(self.text_help)

        # Texts for stats area
        self.text_statslabel = Text(0, 0, "STATS", GAME_FONT, 32, 'white')
        self.text_statslabel.rect = (16,16)
        self.text_highscore = Text(0,0, f"Hi-score: {game_data.highscore}", GAME_FONT, 14, 'yellow')
        self.text_highscore.rect = (16,64)
        self.text_coins = Text(0,0, f"Coins: {game_data.coins}", GAME_FONT, 14, 'white')
        self.text_coins.rect = (16,94)
        self.text_timesdied = Text(0,0, f"Times died: {game_data.times_died}", GAME_FONT, 14, 'white')
        self.text_timesdied.rect = (16,124)
        self.text_timeshit = Text(0,0, f"Times hit: {game_data.times_hit}", GAME_FONT, 14, 'white')
        self.text_timeshit.rect = (16,154)
        self.text_timesfuel = Text(0,0, f"Fuel pickups: {game_data.times_fuelpickup}", GAME_FONT, 14, 'white')
        self.text_timesfuel.rect = (16,184)
        self.text_timesshield = Text(0,0, f"Shield pickups: {game_data.times_shieldpickup}", GAME_FONT, 14, 'white')
        self.text_timesshield.rect = (16,214)
        self.text_playtime = Text(0,0, f"Play time: {game_data.play_time}s", GAME_FONT, 14, 'white')
        self.text_playtime.rect = (16,244)
        self.statstexts.add(self.text_statslabel)
        self.statstexts.add(self.text_highscore)
        self.statstexts.add(self.text_coins)
        self.statstexts.add(self.text_timesdied)
        self.statstexts.add(self.text_timeshit)
        self.statstexts.add(self.text_timesfuel)
        self.statstexts.add(self.text_timesshield)
        self.statstexts.add(self.text_playtime)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_w or event.key == pygame.K_UP) and self.cur_sel > 0:
                    self.selector_y -= 45
                    self.cur_sel -= 1
                    select_sfx.play()
                if (event.key == pygame.K_s or event.key == pygame.K_DOWN) and self.cur_sel < len(self.optiontexts) - 1:
                    self.selector_y += 45
                    self.cur_sel += 1
                    select_sfx.play()
                
                if event.key == pygame.K_RETURN:
                    if self.cur_sel == 0:
                        self.manager.go_to(GameScene())
                    elif self.cur_sel == 1:
                        self.manager.go_to(ShopScene())
                    elif self.cur_sel == 2:
                        self.stats_available = not self.stats_available
                        self.help_available = False
                    elif self.cur_sel == 3:
                        self.stats_available = False
                        self.help_available = not self.help_available
                    elif self.cur_sel == 4:
                        # Save data and exit
                        #game_data.coins = 3000
                        outfile = open(os.path.join(DATA_DIR, "user_data.dat"), "wb")
                        pickle.dump(game_data, outfile)
                        outfile.close()
                        sys.exit()
                    enter_sfx.play()

    def update(self):

        # Update background and parallax x position
        self.bg_layer1_x -= 1
        self.bg_layer2_x -= 2
        self.bg_layer3_x -= 4

        self.statstexts.update()
        self.helptexts.update()
        self.optiontexts.update()

    def draw(self, window):
        window.fill((0,0,12))
        self.draw_background(window, self.bg_layer1_img, self.bg_layer1_rect, self.bg_layer1_x)
        self.draw_background(window, self.bg_layer2_img, self.bg_layer2_rect, self.bg_layer2_x)
        self.draw_background(window, self.bg_layer3_img, self.bg_layer3_rect, self.bg_layer3_x)
        window.blit(self.logo_img, (32,64))
        window.blit(self.menu_area, (96,198))
        window.blit(self.dev_img, (360,128))
        if self.help_available:
            window.blit(self.help_area, (430, 32))
            self.help_area.fill('black')
            self.helptexts.draw(self.help_area)
            self.help_area.blit(self.help_img, (0,0))
            pygame.draw.rect(self.help_area, 'white', (0,0,self.help_area.get_width(),self.help_area.get_height()), 8)
        if self.stats_available:
            window.blit(self.stats_area, (430, 32))
            self.stats_area.fill('black')
            self.statstexts.draw(self.stats_area)
            pygame.draw.rect(self.stats_area, 'white', (0,0,self.stats_area.get_width(),self.stats_area.get_height()), 8)
        #window.blit(self.menu_area, self.menu_area_rect)
        #window.blit(self.logo_img, (WIN_SZ[1] / 2 - (self.logo_img.get_width()/6), 48))
        self.menu_area.fill('brown')
        self.menu_area.set_colorkey('brown')
        self.optiontexts.draw(self.menu_area)
        pygame.draw.rect(self.menu_area, 'white', (3,self.selector_y,249,40), self.selector_width) # selector

    def draw_background(self, surf, img, img_rect, pos):
        surf_w = surf.get_width()
        rel_x = pos % img_rect.width
        surf.blit(img, (rel_x - img_rect.width, 0))

        if rel_x < surf_w:
            surf.blit(img, (rel_x, 0))

class ShopScene(Scene):
    def __init__(self):
        #print(game_data.highscore, game_data.coins)
        self.coins = 1000
        self.init_x = 16
        self.init_y = 16
        self.x_offset = 64 + self.init_x 
        self.y_offset = 64 + self.init_y
        self.pet_files = [
            'pet_cat.png', 
            'pet_chiki.png', 
            'pet_coffee.png', 
            'pet_dog.png', 
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
        if game_data.equipped_pet != "none":
            self.pet_equipped_x = 16 + (80 * self.pet_files.index(game_data.equipped_pet))
            #self.row_break = len(self.all_pets) // 2
        if game_data.equipped_hat != "none":
            self.hat_equipped_x = 16 + (80 * self.hat_files.index(game_data.equipped_hat))
        self.cur_pet = 0
        self.cur_hat = 0
        self.item_cost = 20
        self.debug_mode = False
        
        # Surfaces
        self.pets_area = pygame.Surface((WIN_SZ[0] / 1.33, 96))
        self.hats_area = pygame.Surface((WIN_SZ[0] / 1.33, 96))
        self.cur_shop = self.pets_area

        self.bg_layer1_img = load_png("title_bg_layer1.png", IMG_DIR, 4)     
        self.bg_layer1_rect = self.bg_layer1_img.get_rect()
        self.bg_layer2_img = load_png("title_bg_layer2.png", IMG_DIR, 4)
        self.bg_layer2_rect = self.bg_layer2_img.get_rect()
        self.bg_layer3_img = load_png("title_bg_layer3.png", IMG_DIR, 4)
        self.bg_layer3_rect = self.bg_layer3_img.get_rect()

        self.bg_layer1_x = 0
        self.bg_layer2_x = 0
        self.bg_layer3_x = 0

        # Sprite groups
        self.texts = pygame.sprite.Group()

        # Texts
        self.text_shoplabel = Text(WIN_SZ[0] / 5, 64, "Shop", GAME_FONT, 48, 'white')
        self.text_coins = Text(WIN_SZ[0] / 1.4, 75, f"C{game_data.coins}", GAME_FONT, 32, 'yellow')
        self.text_isbought = Text(WIN_SZ[0] / 1.5, 400, "Bought", GAME_FONT, 32, 'white', False)
        self.text_entbutton = Text(WIN_SZ[0] / 1.5, 360, "[ENT]", GAME_FONT, 32, 'white')
        self.text_cost = Text(WIN_SZ[0] / 1.5, 400, f"Cost {self.item_cost}", GAME_FONT, 32, 'white', False)
        self.text_exitbutton = Text(WIN_SZ[0] / 4.2, 400, "[ESC]", GAME_FONT, 32, 'white')
        self.texts.add(self.text_shoplabel)
        self.texts.add(self.text_coins)
        self.texts.add(self.text_isbought)
        self.texts.add(self.text_cost)
        self.texts.add(self.text_exitbutton)
        self.texts.add(self.text_entbutton)

    def handle_events(self, events):
        # YandereDev-esque code here. Beware!
        for event in events:
            if event.type == pygame.KEYDOWN:

                if self.cur_shop == self.pets_area:
                    if event.key == pygame.K_d and self.cur_pet < len(self.pet_files) - 1:
                        self.selector_x += 64 + self.init_x
                        self.cur_pet += 1
                        select_sfx.play()
                    if event.key == pygame.K_a and self.cur_pet > 0:
                        self.selector_x -= 64 + self.init_x
                        self.cur_pet -= 1
                        select_sfx.play()
                elif self.cur_shop == self.hats_area:
                    if event.key == pygame.K_d and self.cur_hat < len(self.hat_files) - 1:
                        self.selector_x += 64 + self.init_x
                        self.cur_hat += 1
                        select_sfx.play()
                    if event.key == pygame.K_a and self.cur_hat > 0:
                        self.selector_x -= 64 + self.init_x
                        self.cur_hat -= 1
                        select_sfx.play()

                if event.key == pygame.K_RETURN:
                    if self.cur_shop == self.pets_area:
                        if self.pet_files[self.cur_pet] in game_data.owned_pets:
                            if game_data.equipped_pet == self.pet_files[self.cur_pet]:
                                game_data.equipped_pet = "none"
                                enter_sfx.play()
                            else:
                                game_data.equipped_pet = self.pet_files[self.cur_pet]
                                self.pet_equipped_x = self.selector_x
                                enter_sfx.play()
                        else:
                            if game_data.coins >= self.item_cost:
                                game_data.equipped_pet = self.pet_files[self.cur_pet]
                                self.pet_equipped_x = self.selector_x
                                game_data.owned_pets.append(self.pet_files[self.cur_pet])
                                game_data.coins -= self.item_cost
                                self.text_coins.text = f"C{game_data.coins}"
                                buy_sfx.play()
                            else:
                                self.text_coins.color = 'red'
                                denied_sfx.play()
                                
                    elif self.cur_shop == self.hats_area:
                        if self.hat_files[self.cur_hat] in game_data.owned_hats:
                            if game_data.equipped_hat == self.hat_files[self.cur_hat]:
                                game_data.equipped_hat = "none"
                                enter_sfx.play()
                            else:
                                game_data.equipped_hat = self.hat_files[self.cur_hat]
                                self.hat_equipped_x = self.selector_x
                                enter_sfx.play()
                        else:
                            if game_data.coins >= self.item_cost:
                                game_data.equipped_hat = self.hat_files[self.cur_hat]
                                self.hat_equipped_x = self.selector_x
                                game_data.owned_hats.append(self.hat_files[self.cur_hat])
                                game_data.coins -= self.item_cost
                                self.text_coins.text = f"C{game_data.coins}"
                                buy_sfx.play()
                            else:
                                self.text_coins.color = 'red'
                                denied_sfx.play()

                if event.key == pygame.K_w:
                    self.cur_shop = self.pets_area
                    self.cur_pet = 0
                    self.selector_x = 16
                    select_sfx.play()

                if event.key == pygame.K_s:
                    self.cur_shop = self.hats_area
                    self.cur_hat = 0
                    self.selector_x = 16
                    select_sfx.play()

                if event.key == pygame.K_ESCAPE:
                    self.manager.go_to(TitleScene())
                    enter_sfx.play()

                #print(self.pet_files[self.cur_pet])
                #print(self.pet_files[self.cur_pet] in Game_Data.owned_pets)
        #print("Pet Equipped: " + game_data.equipped_pet)
        #print("Hat Equipped:" + game_data.equipped_hat)
        #print(self.cur_pet, self.cur_hat)

    def update(self):

        # Update background and parallax x position
        self.bg_layer1_x -= 1
        self.bg_layer2_x -= 2
        self.bg_layer3_x -= 4

        if self.cur_shop == self.pets_area:

            if self.pet_files[self.cur_pet] in game_data.owned_pets:
                self.text_isbought.visible = True
                self.text_cost.visible = False
            else:
                self.text_isbought.visible = False
                self.text_cost.visible = True

            self.item_cost = 30
            self.text_cost.text = f"C{self.item_cost}"

        elif self.cur_shop == self.hats_area:

            if self.hat_files[self.cur_hat] in game_data.owned_hats:
                self.text_isbought.visible = True
                self.text_cost.visible = False
            else:
                self.text_isbought.visible = False
                self.text_cost.visible = True

            self.item_cost = 20
            self.text_cost.text = f"C{self.item_cost}"

        self.texts.update()

    def draw(self, window):
        self.draw_items(self.pets_area, self.pet_imgs)
        self.draw_items(self.hats_area, self.hat_imgs)
        window.fill((0,0,12))
        self.draw_background(window, self.bg_layer1_img, self.bg_layer1_rect, self.bg_layer1_x)
        self.draw_background(window, self.bg_layer2_img, self.bg_layer2_rect, self.bg_layer2_x)
        self.draw_background(window, self.bg_layer3_img, self.bg_layer3_rect, self.bg_layer3_x)
        window.blit(self.pets_area, (64,128))
        window.blit(self.hats_area, (64,256))
        self.pets_area.fill('black')
        self.hats_area.fill('black')
        pygame.draw.rect(self.pets_area, 'white', (0,0, self.pets_area.get_width(), self.pets_area.get_height()), 8, 8, 8, 8)
        pygame.draw.rect(self.hats_area, 'white', (0,0, self.hats_area.get_width(), self.hats_area.get_height()), 8, 8, 8, 8)
        pygame.draw.rect(self.cur_shop, 'white', (self.selector_x, self.selector_y, 64, 64), 8) # this is the selector
        if game_data.equipped_pet != "none":
            pygame.draw.rect(self.pets_area, 'yellow', (self.pet_equipped_x, self.init_y, 64, 64), 8)
        if game_data.equipped_hat != "none":
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

    def draw_background(self, surf, img, img_rect, pos):
        surf_w = surf.get_width()
        rel_x = pos % img_rect.width
        surf.blit(img, (rel_x - img_rect.width, 0))

        if rel_x < surf_w:
            surf.blit(img, (rel_x, 0))

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
        self.cur_playtime = 0
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

        if game_data.equipped_pet != "none":
            pet_ing = load_png(game_data.equipped_pet, IMG_DIR, 3)
        if game_data.equipped_hat != "none":
            hat_img = load_png(game_data.equipped_hat, IMG_DIR, img_sc)

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
        if game_data.equipped_pet != "none":
            self.pet = Pet(pet_ing, self.player)
        if game_data.equipped_hat != "none":
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
                    game_data.coins += self.coins
                    if round(self.score) > game_data.highscore:
                        game_data.highscore = round(self.score)
                    game_data.times_died += 1
                    game_data.play_time += round(self.cur_playtime / 1000)
                    self.manager.go_to(TitleScene())

                if event.key == pygame.K_ESCAPE:
                    self.manager.go_to(TitleScene())
                    game_data.play_time += round(self.cur_playtime / 1000)

                    if self.can_exit:
                        game_data.coins += self.coins
                        if round(self.score) > game_data.highscore:
                            game_data.highscore = round(self.score)
                        game_data.times_died += 1
                        game_data.play_time += round(self.cur_playtime / 1000)
                        self.manager.go_to(TitleScene())

    def update(self):
        
        # Update crap
        self.cur_playtime += 10
        if self.player.has_started and not self.player.is_dead:
            self.update_difficulty()
            self.score += 0.1
            self.player.fuel -= 0.1 + (self.global_xspeed // 15)
            self.text_score.text = f"{str(round(self.score)).zfill(5)}"

        # Check for enemy collision
        if self.player.fuel > 0 and not self.player.is_dead:
            hits = pygame.sprite.spritecollide(self.player, self.enemies, False, pygame.sprite.collide_rect_ratio(0.7))
            for hit in hits:
                self.offset = self.shake(20,5)
                self.spawn_particles(self.sprites, self.particles, hit.rect.centerx, hit.rect.centery, ['white'], 10)
                self.spawn_shockwave(hit.rect.centerx, hit.rect.centery, 'white')
                if self.player.shield <= 0:
                    self.player.is_dead = True
                else:
                    self.player.shield -= 1
                game_data.times_hit += 1
                
                hit.kill()
                explosion_sfx.play()

        # Check for powerup collisions
        if not self.player.is_dead:
            hits = pygame.sprite.spritecollide(self.player, self.powerups, False, pygame.sprite.collide_rect_ratio(0.7))
            for hit in hits:

                self.spawn_particles(self.sprites, self.particles, self.player.rect.centerx, self.player.rect.centery, [(124,231,20)], 10)
                self.spawn_shockwave(self.player.rect.centerx, self.player.rect.centery, (124,231,20))

                if hit.type == "fuel":
                    game_data.times_fuelpickup += 1
                    self.player.fuel += 20
                    if self.player.fuel > 100:
                        self.player.fuel = 100
                elif hit.type == "shield":
                    game_data.times_shieldpickup += 1
                    self.player.shield += 1
                    if self.player.shield > 2:
                        self.player.shield = 2
                elif hit.type == "coin":
                    self.coins += 1
                    self.text_coins.text = f"{str(self.coins).zfill(5)}"
                hit.kill()
                buy_sfx.play()

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
        if game_data.equipped_pet != "none":
            self.pet.update()
        if game_data.equipped_hat != "none":
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
        if game_data.equipped_pet != "none":
            self.pet.draw(self.play_area)
        if game_data.equipped_hat != "none":
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
        if self.difficulty_ticks >= self.difficulty_increase_delay and self.difficulty_level != 15:
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
    window = pygame.display.set_mode(WIN_SZ)
    pygame.display.set_caption(TITLE)
    pygame.display.set_icon(load_png("CoffeeOMeter1.png", IMG_DIR, 1))
    pygame.mouse.set_visible(False)

    # Load and play music
    pygame.mixer.music.load(os.path.join(SFX_DIR, "music.ogg"))
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)

    # Loop
    running = True
    manager = SceneManager(TitleScene())
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

# Exit pygame and application, and save user data
pygame.quit()

outfile = open(os.path.join(DATA_DIR, "user_data.dat"), "wb")
pickle.dump(game_data, outfile)
outfile.close()

sys.exit()
