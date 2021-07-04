import pygame
from objects import Player, Enemy, Aim
from constants import WIDTH, HEIGHT, FPS

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        pygame.display.set_caption('WESTERN')
        self.bg = pygame.image.load('assets/images/background.png')
        self.shot_sound = pygame.mixer.Sound('assets/sound/shot.wav')
        self.player = Player(800, 350)
        self.enemy = Enemy(300, 170)
        self.aim = Aim(self.enemy)

        self.all_sprite_list = pygame.sprite.Group()
        self.all_sprite_list.add(self.player)
        self.all_sprite_list.add(self.enemy)
        self.all_sprite_list.add(self.aim)
        self.clock = pygame.time.Clock()

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        self.all_sprite_list.draw(self.screen)

    def run(self):
        done = False
        while not done:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.player.shoot()
                        self.shot_sound.play()

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT and self.player.change_x < 0:
                        self.player.stop()
                    if event.key == pygame.K_RIGHT and self.player.change_x > 0:
                        self.player.stop()

            self.draw()
            self.all_sprite_list.update()
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()

game = Game()
game.run()
