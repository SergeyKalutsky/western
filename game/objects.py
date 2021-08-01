from constants import RED
from random import randint
import pygame


def clamp(value, minv, maxv):
    """
    Эта функция ограничевает число(value).

    Если value меньше minv, то функция возвращает minv.
    Если value больше maxv, то функция возвращает maxv.
    Если value не больше maxv и не меньше min, то функция возвращает value.
    """
    return float(max(min(maxv, value), minv))


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        
        # чтобы изменить спрайт игрока на старый,
        # замените "player11.png" на "player1.png"
        self.stand_img = pygame.image.load('assets/images/player11.png') 
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
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def shoot(self):
        self.image = self.shooting_img

    def update(self):
        pass

class Aim(pygame.sprite.Sprite):

    def __init__(self, enemy, shake_power=1, shake_frequency=1):
        super().__init__()

        self.image = pygame.image.load('assets/images/aim.png')
        self.rect = self.image.get_rect()
        self.rect.x = enemy.rect.x + enemy.rect.width/2 - self.rect.width/2
        self.rect.y = enemy.rect.y + enemy.rect.height/2 - self.rect.height/2
        self.shake_power = shake_power
        self.shake_frequency = 10 - clamp(shake_frequency, 0, 10)
        self.bullet_hole = BulletHole()

    def update(self):
        self.shake()
    
    def shake(self):
        """
        shake_power - отвечает за силу тряски прицела

        shake_frequency - отвечает шанс тряски прицела в отдельном кадре
        shake_frequency = 0  -  шанс тряски прицела в отдельном кадре = 0%
        shake_frequency = 10  -  шанс тряски прицела в отдельном кадре = 100%
        """
        if randint(0, self.shake_frequency) == 0 and self.shake_frequency != 10:
            self.rect.x += randint(-10*self.shake_power, 10*self.shake_power)
            self.rect.y += randint(-10*self.shake_power, 10*self.shake_power)

    def make_bullet_hole(self):
        """
        В этом методе у обьекта bullet_hole изменяется позиция со стандартной,
        [-100, -100](за пределами экрана), на позицию центра прицела.
        """
        self.bullet_hole.rect.x, self.bullet_hole.rect.y = self.rect.x+40, self.rect.y+40

class BulletHole(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(-100, -100, 1 ,1)
        
        self.image = pygame.image.load('assets/images/bullet_hole.png')
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.mask = pygame.mask.from_surface(self.image)

class Timer:
    def __init__(self, fps, seconds):
        self.fps = fps
        self.seconds = seconds
        self.max_frames = fps * self.seconds
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