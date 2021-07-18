import pygame
from objects import Player, Enemy, Aim, Timer
from constants import WIDTH, HEIGHT, FPS, RED

class Game:
    def __init__(self):
        pygame.init()
        self.font = pygame.font.SysFont('Arial', 30)
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        pygame.display.set_caption('WESTERN(Для выхда из игры нажать ESC)')
        self.bg = pygame.image.load('assets/images/background.png')
        self.shot_sound = pygame.mixer.Sound('assets/sound/shot.wav')
        self.player = Player(800, 350)
        self.enemy = Enemy(300, 170)
        self.aim = Aim(self.enemy)
        self.shoot_timer = Timer(FPS, 0.33)
        self.attack_timer = Timer(FPS, 2)
        self.all_sprite_list = pygame.sprite.Group()
        self.all_sprite_list.add(self.player)
        self.all_sprite_list.add(self.enemy)
        self.all_sprite_list.add(self.aim)
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(False)

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        self.all_sprite_list.draw(self.screen)
        if self.attack_timer.active:
            text = self.font.render(str(self.attack_timer.time), False, RED)
            coord = (self.aim.rect.x+25, self.aim.rect.y-35)
            self.screen.blit(text, coord)

    def move_aim(self):
        rel = pygame.mouse.get_rel()
        pos = pygame.mouse.get_pos()
        if pos[0] < 400 or pos[0] > 800:
            pygame.mouse.set_pos(600, pos[1])
        pos = pygame.mouse.get_pos()
        if pos[1] < 300 or pos[1] > 500:
            pygame.mouse.set_pos(pos[0], 400)
        if abs(rel[0]) < 150:
            self.aim.rect[0] += rel[0]
        if abs(rel[1]) < 60:
            self.aim.rect[1] += rel[1]
        

    def run(self):
        done = False
        
        while not done:
            self.move_aim()
            self.shoot_timer.update()
            self.attack_timer.update()
            
            if not self.shoot_timer.active:
                self.player.image = self.player.stand_img

            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    done = True
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.attack_timer.start()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.shoot_timer.start()
                        self.player.shoot()
                        self.shot_sound.play()
                        self.aim.make_bullet_hole(self.screen)

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT and self.player.change_x < 0:
                        self.player.stop()
                    if event.key == pygame.K_RIGHT and self.player.change_x > 0:
                        self.player.stop()

            self.all_sprite_list.update()
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()

game = Game()
game.run()
