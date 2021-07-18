from constants import RED
from random import randint
import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()

        self.stand_img = pygame.image.load('assets/images/player1.png')
        self.shooting_img = pygame.image.load('assets/images/player2.png')
        self.image = self.stand_img
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def shoot(self):
        self.image = self.shooting_img

    def update(self):
        pass


class Enemy(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()

        self.stand_img = pygame.image.load('assets/images/enemy1.png')
        self.shooting_img = pygame.image.load('assets/images/enemy2.png')
        self.image = self.stand_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def shoot(self):
        self.image = self.shooting_img

    def update(self):
        pass

class Aim(pygame.sprite.Sprite):

    def __init__(self, enemy):
        super().__init__()

        self.image = pygame.image.load('assets/images/aim.png')
        self.rect = self.image.get_rect()
        self.rect.x = enemy.rect.x
        self.rect.y = enemy.rect.y

    def update(self):
        if randint(0, 1):
            self.rect.x += randint(1,10)
            self.rect.y += randint(1,10)
        else:
            self.rect.x -= randint(1,10)
            self.rect.y -= randint(1,10)

    def make_bullet_hole(self, screen):
        pygame.draw.circle(screen, RED, (self.rect.x+50, self.rect.y+50), 7)


class Timer:
    def __init__(self, fps, seconds):
        self.fps = fps
        self.seconds_per_frame = seconds
        self.max_frames = fps * seconds
        self.frames = 0
        self.active = False

    def update(self):
        if self.active:
            if self.frames <= self.max_frames:
                self.frames += 1
            else:
                self.active = False
    
    def start(self):
        self.active = True
        self.frames = 0

    @property
    def time(self):
        return round(self.frames / self.fps, 2)