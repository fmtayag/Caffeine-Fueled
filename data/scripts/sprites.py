import pygame, math
from random import randrange, choice, choices
from data.scripts.maths_stuff import roundup

class Player(pygame.sprite.Sprite):
    def __init__(self, images):
        super().__init__()
        self.images = images
        self.image = self.images["NORMAL"]["IDLE"]
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100
        self.speedx = 4
        self.speedy = 4
        self.GRAVITY = 0.1
        self.boost = 0.23
        self.state = "IDLE"
        self.status = "SHIELDED"
        self.shield = 2
        self.fuel = 100
        self.is_dead = False

        # Color correction
        self.color_correction = pygame.Surface((self.image.get_width(), self.image.get_height()))
        self.color_correction.set_alpha(100)

    def update(self):
        if self.fuel > 0 and not self.is_dead:

            if self.shield <= 0:
                self.status = "NORMAL"
            else:
                self.status = "SHIELDED"

            self.image = self.images[self.status]["IDLE"]
            self.state = "IDLE"
            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_a]:
                self.rect.x -= self.speedx * 1.5
                self.image = self.images[self.status]["MOVLEFT"]
                self.state = "MOVLEFT"
            if pressed[pygame.K_d]:
                self.rect.x += self.speedx
                self.image = self.images[self.status]["MOVRIGHT"]
                self.state = "MOVRIGHT"
            if pressed[pygame.K_w]:
                self.speedy -= (self.GRAVITY + self.boost)
            if pressed[pygame.K_s]:
                self.speedy += (self.GRAVITY + self.boost * 0.2)

            self.speedy += self.GRAVITY
            self.rect.y += self.speedy
        else:
            self.image.set_alpha(100)
            self.speedy += self.GRAVITY
            self.rect.y += self.speedy

    def draw(self, window):
        window.blit(self.image, (self.rect.x,self.rect.y))

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, obstacle_imgs, play_area):
        super().__init__()
        self.obstacle_imgs = obstacle_imgs
        self.obstacle_img = self.obstacle_imgs[0]
        self.image = pygame.Surface((self.obstacle_img.get_width() * 1.2, self.obstacle_img.get_height() * 1.2))
        self.rect = self.image.get_rect()
        self.rect.x = play_area.get_width() + randrange(32, 128)
        self.rect.y = randrange(0, play_area.get_height() - self.image.get_height())
        # For bobbing effect
        self.y = 0
        self.multiplier = 4
        self.bob = math.sin(self.y) * self.multiplier
        self.obstacle_img_rect = self.obstacle_img.get_rect(center=(self.image.get_width() / 2 - self.obstacle_img.get_width() / 2, self.image.get_height() / 2))
        # For animation
        if len(self.obstacle_imgs) > 1:
            self.anim_timer = pygame.time.get_ticks()
            self.anim_delay = 100
            self.frame = 0

    def update(self):
        if len(self.obstacle_imgs) > 1:
            self.animate()
        self.y += 0.1
        self.bob = math.sin(self.y) * self.multiplier
        self.image.fill('black')
        self.image.blit(self.obstacle_img, (self.obstacle_img_rect.center[0], 6 - self.bob)) # 6 is just an arbitrary offset
        self.image.set_colorkey('black')
        if self.rect.right < 0:
            self.kill()

    def animate(self):
        if pygame.time.get_ticks() - self.anim_timer > self.anim_delay:
            self.anim_timer = pygame.time.get_ticks()
            self.frame = not self.frame
            self.obstacle_img = self.obstacle_imgs[self.frame]

class Hat(pygame.sprite.Sprite):
    def __init__(self, image, wearer, x_offset, y_offset):
        super().__init__()
        self.wearer = wearer
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = self.wearer.rect.centerx
        self.rect.bottom = self.wearer.rect.top + self.y_offset

    def update(self):
        if self.wearer.state == "IDLE":
            self.rect.centerx = self.wearer.rect.centerx
        elif self.wearer.state == "MOVLEFT":
            self.rect.centerx = self.wearer.rect.centerx - self.x_offset
        elif self.wearer.state == "MOVRIGHT":
            self.rect.centerx = self.wearer.rect.centerx + self.x_offset

        self.rect.bottom = self.wearer.rect.top + self.y_offset

    def draw(self, window):
        window.blit(self.image, (self.rect.x,self.rect.y))

class Pet(pygame.sprite.Sprite):
    def __init__(self, image, wearer):
        super().__init__()
        self.wearer = wearer
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = self.wearer.rect.left
        self.rect.bottom = self.wearer.rect.bottom
        # For bobbing effect
        self.y = 0
        self.multiplier = 8
        self.bob = math.sin(self.y) * self.multiplier

    def update(self):
        self.rect.centerx = self.wearer.rect.left

        self.y += 0.1
        self.bob = math.sin(self.y) * self.multiplier

        self.rect.bottom = self.wearer.rect.bottom + self.bob

    def draw(self, window):
        window.blit(self.image, (self.rect.x,self.rect.y))

class CoffeeOMeter(pygame.sprite.Sprite):
    def __init__(self, images, pos, initial, end, do_round=True):
        super().__init__()
        self.images = images
        self.image = self.images[initial]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.end = end
        self.do_round = do_round
    
    def update(self, amount):
        try:
            if self.do_round:
                self.image = self.images[str(roundup(amount))]
            else:
                self.image = self.images[str(amount)]
        except Exception as e:
            self.image = self.images[self.end]

    def draw(self, surface):
        surface.blit(self.image, self.rect.center)

class Text(pygame.sprite.Sprite):
    def __init__(self, x, y, text, font_type, size, color):
        super().__init__()
        self.image = pygame.Surface((size * len(text),size)).convert_alpha()
        #self.image.fill('blue')
        self.image.set_colorkey('black')
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y

        # The text
        self.text = str(text)
        self.cur_text = self.text
        self.font_type = font_type
        self.size = size
        self.color = color
        self.font = pygame.font.Font(self.font_type, self.size)
        self.rendered = self.font.render(str(self.text), 0, self.color)
        self.rendered_rect = self.rendered.get_rect(center=(self.image.get_width()/2, self.image.get_height()/2))
        self.image.blit(self.rendered, self.rendered_rect)

    def update(self):
        self.image.fill('black')
        self.rendered = self.font.render(str(self.text), 0, self.color)
        self.rendered_rect = self.rendered.get_rect(center=(self.image.get_width()/2, self.image.get_height()/2))
        self.image.blit(self.rendered, self.rendered_rect)

class Powerup(pygame.sprite.Sprite):
    def __init__(self, images, play_area):
        super().__init__()
        self.images = images
        self.type = self.roll_type(self.images)
        self.pow_img = self.images[self.type]
        self.image = pygame.Surface((self.pow_img.get_width(), self.pow_img.get_height() * 1.5))
        self.rect = self.image.get_rect()
        self.rect.x = play_area.get_width() + randrange(32, 128)
        self.rect.y = randrange(self.image.get_height() / 2, play_area.get_height() - self.image.get_height() - 32)
        # For bobbing effect
        self.y = 0
        self.multiplier = 4
        self.bob = math.sin(self.y) * self.multiplier
        self.pow_img_rect = self.pow_img.get_rect(center=(self.image.get_width() / 2 - self.pow_img.get_width() / 2, self.image.get_height() / 2))

    def update(self):
        self.y += 0.1
        self.bob = math.sin(self.y) * self.multiplier
        self.image.fill('black')
        self.image.blit(self.pow_img, (self.pow_img_rect.center[0], 6 - self.bob)) # 6 is just an arbitrary offset
        self.image.set_colorkey('black')
        if self.rect.right < 0:
            self.kill()

    def roll_type(self, images):
        keys = list(images.keys())
        keys = choices(keys, weights=[8,2], k=10)
        roll = choice(keys)
        return roll

class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.color = choice(color)
        self.size = choice([8,12])
        self.image = pygame.Surface((self.size,self.size)).convert_alpha()
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.movspd = 8
        self.spdx = choice([num for num in range(-8,8) if num not in [-2,-1,0,1,2]])
        self.spdy = choice([num for num in range(-6,6) if num not in [-2,-1,0,1,2]])

        # For fade animation
        self.alpha = 255

    def update(self):
        self.rect.x += self.spdx
        self.rect.y += self.spdy

        if self.spdy < self.movspd:
            self.spdy += 0.1
        elif self.spdy > self.movspd:
            self.spdy -= 0.1

        if self.alpha <= 0:
            self.kill()

        self.fade()

    def fade(self):
        self.alpha -= 8
        self.image.set_alpha(self.alpha)

class Shockwave(pygame.sprite.Sprite):
    def __init__(self, x, y, color, K_SIZE):
        super().__init__()
        # The surface
        self.image = pygame.Surface((K_SIZE*4,K_SIZE*4)).convert_alpha()
        self.image.set_colorkey('black')
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.img_width = self.image.get_width()
        self.color = color
        self.alpha = 255
        
        # The circle
        self.expand_timer = pygame.time.get_ticks()
        self.expand_delay = 10
        self.radius = 2
        self.c_width = 5
        self.expand_amnt = 2

    def update(self):
        self.expand()
        if self.alpha <= 0:
            self.kill()

    def expand(self):
        now = pygame.time.get_ticks()
        if now - self.expand_timer > self.expand_delay:
            self.alpha -= 10
            self.radius += self.expand_amnt
            #self.c_width += 1
            #self.image.fill((20,18,29,0))
            self.image.fill((0,0,0,0))
            self.image.set_alpha(self.alpha)
            pygame.draw.circle(self.image, self.color, self.image.get_rect().center, self.radius, self.c_width)


# Unused
class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, text, font_name, color, width, height, thickness):
        super().__init__()
        self.x = x
        self.y = y
        self.text = text.split(" ")
        self.font_name = font_name
        self.color = color
        self.width = width
        self.height = height
        self.thickness = thickness
        self.orig_thickness = self.thickness
        self.state = "HIGHLIGHTED"
        
        # Surface
        self.image = pygame.Surface((self.width, self.height)).convert_alpha()
        self.image.set_colorkey('black')
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.img_center = (self.image.get_width() / 2, self.image.get_height() / 2)

        # Font
        self.font_size = self.width // 8
        self.font_object = pygame.font.Font(self.font_name, self.font_size)

    def update(self):
        if self.state == "HIGHLIGHTED":
            self.highlight()
        elif self.state == "UNHIGHLIGHTED":
            self.unhighlight()

    def highlight(self):
        self.refill()
        pygame.draw.rect(self.image, self.color, (0, 0, self.width, self.height), 0)
        self.draw_text()

    def unhighlight(self):
        self.refill()
        pygame.draw.rect(self.image, self.color, (0, 0, self.width, self.height), self.thickness)
        self.draw_text()

    def refill(self):
        self.image.fill('black')
        self.image.set_colorkey('black')

    def draw_text(self):
        y_pos = 1
        for text in self.text:
            self.font_render = self.font_object.render(text, 1, self.color)
            self.fr_rect = self.font_render.get_rect(center=(self.img_center[0], self.img_center[1] * y_pos / 1.5))
            self.image.blit(self.font_render, self.fr_rect)
            y_pos += 1