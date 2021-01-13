import pygame

class Crew(pygame.sprite.Sprite):
    def __init__(self, portrait, bio):
        super().__init__()
        self.portrait = portrait
        self.name = bio["name"]
        self.gender = bio["gender"]
        self.personality = bio["personality"]
        self.role = bio["role"]
        self.health = 100
        self.hunger = 100
        self.sanity = 100
        self.consumption_rate = self.calculate_consumption(self.personality)

        self.image = self.portrait

    def update(self):
        pass

    def calculate_consumption(self, personality):
        if personality == "greedy":
            return 0.20
        else:
            return 0.10

class Ship(pygame.sprite.Sprite):
    def __init__(self, images):
        super().__init__()
        self.images = images
        self.fuel = 100
        self.food = 100
        self.supplies = 100
        self.speed = 5

        self.image = self.images[0]

    def update(self):
        pass