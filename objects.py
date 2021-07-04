from random import randint
import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()

        self.stand_img = pygame.image.load('assets/images/player1.png')
        self.shooting_img = pygame.image.load('assets/images/player2.png')
        self.image = self.stand_img
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

    def __init__(self, enemy) -> None:
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