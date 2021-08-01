import pygame

from objects import Player, Enemy, Aim, Timer
from constants import WIDTH, HEIGHT, FPS, ISCANDER_RED


class Game:
    def __init__(self):
        
        pygame.init()
        self.font = pygame.font.SysFont('Arial', 30)
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        pygame.display.set_caption('WESTERN(Для выхда из игры нажать ESC)')
        self.bg = pygame.image.load('assets/images/background_v2.png')
        self.shot_sound = pygame.mixer.Sound('assets/sound/shot.wav')
        self.player = Player(800, 300)
        self.enemy = Enemy(250, 100)
        self.aim = Aim(self.enemy, shake_power=1, shake_frequency=0)
        self.shoot_timer = Timer(FPS, 0.33)
        self.attack_timer = Timer(FPS, 2)
        self.all_sprite_list = pygame.sprite.Group()
        self.all_sprite_list.add(self.player)
        self.all_sprite_list.add(self.enemy)
        
        self.all_sprite_list.add(self.aim.bullet_hole)
        self.clock = pygame.time.Clock()
        """
        battle_permissions == [False, False] - не один из игроков не нажал space
        battle_permissions == [True, False] or battle_permissions == [False, True] - один из игроков нажал space
        battle_permissions == [True, True] - оба игрока нажали пробел и таймер выстрела запустился
        """
        self.battle_permissions = [False, False]
        self.battle_permissions[0] = True

        self.attack_timer_HBA = False # attack_timer Has Been Activeted

        pygame.mouse.set_visible(False)

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        self.all_sprite_list.draw(self.screen)
        if self.attack_timer.active:
            text = self.font.render(str(self.attack_timer.time), False, ISCANDER_RED)
            coord = (self.aim.rect.x+25, self.aim.rect.y-35)
            self.screen.blit(text, coord)

    def move_aim(self):
        rel = pygame.mouse.get_rel()
        pos = pygame.mouse.get_pos()
        # следующее строки не позволяют курсору выйти за пределы окна
        if pos[0] < 400 or pos[0] > 800:
            pygame.mouse.set_pos(600, pos[1])
        pos = pygame.mouse.get_pos()
        if pos[1] < 300 or pos[1] > 500:
            pygame.mouse.set_pos(pos[0], 400)
        if abs(rel[0]) < 150:
            self.aim.rect[0] += rel[0]
        if abs(rel[1]) < 60:
            self.aim.rect[1] += rel[1]
    
    def score_culculate(self):
        """
        Этот метод подсчитывает количество очков набранных за выстрел
        """
        block_hit_list = pygame.sprite.spritecollide(self.enemy, [self.aim.bullet_hole], False, pygame.sprite.collide_mask)
        if block_hit_list:
            # если игрок попал в ноги противника, игрок получает 20 очков умноженных на процент прошедшего времени с момента запуска attack_timer
            if self.aim.bullet_hole.rect.y-self.enemy.rect.y > 180:
                return round(20*(self.attack_timer.seconds - self.attack_timer.time)/2, 2)
            # если игрок попал в голову противника, игрок получает 40 очков умноженных на процент прошедшего времени с момента запуска attack_timer
            elif self.aim.bullet_hole.rect.y-self.enemy.rect.y < 50:
                return round(40*(self.attack_timer.seconds - self.attack_timer.time)/2, 2)
            # если игрок попал в руки или туловеще противника,
            # игрок получает 30 очков умноженных на процент прошедшего времени с момента запуска attack_timer
            else:
                return round(30*(self.attack_timer.seconds - self.attack_timer.time)/2, 2)
        # если игрок не попал в противника, игрок получает 0 очков
        return 0

    def shoot(self):
        self.shoot_timer.start()
        self.player.shoot()
        self.shot_sound.play()
        self.aim.make_bullet_hole()
        print(f'Your score: {self.score_culculate()}!')
        self.battle_permissions = [False, False]

    def event_check(self, event):
        """
        В этом методе проверяется тип ивента.
        """
        # если attack_timer запущен и оба игрока нажали space, у игрока появляется возможность выстрелить
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.attack_timer.active and self.battle_permissions == [True, True]:
                self.shoot()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.battle_permissions[1] = True
        
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            # здесь возвращается True и в главном цикле присваевается локальная переменная "done"
            return True
        
        


    def run(self):
        pygame.mixer.music.load('assets/sound/music.ogg')
        pygame.mixer.music.play()
        done = False
        while not done:
            # обновление таймеров
            self.shoot_timer.update()
            self.attack_timer.update()
            
            # изменение спрайта игрока на стандартный через 0.33 сек. после выстрела
            if not self.shoot_timer.active:
                self.player.image = self.player.stand_img

            self.draw()
            for event in pygame.event.get():
                done = self.event_check(event)
            
            # если оба игрока нажали пробел запускается таймер
            if self.battle_permissions[0] and self.battle_permissions[1] and not self.attack_timer.active and not self.attack_timer_HBA:
                self.attack_timer.start()
                self.all_sprite_list.add(self.aim)
                self.attack_timer_HBA = True
            
            # когда attack_timer запущен, появляется возможность двигать прицелом
            if self.attack_timer.active:    
                self.move_aim()

            # обновление спрайтов и окна игры
            self.all_sprite_list.update()
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()

game = Game()
game.run()
