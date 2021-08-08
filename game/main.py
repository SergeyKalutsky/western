import pygame
import requests
import ast

from objects import Player, Enemy, Aim, Timer
from constants import WIDTH, HEIGHT, FPS, ISCANDER_RED, RED
import vsyakie_knopki_i_inputi as vkii


def get_info(url):
    return ast.literal_eval(requests.get(url).content.decode(encoding='utf-8'))


class Game:
    def __init__(self, url):

        pygame.init()
        self.name = ''
        self.url = url
        self.font = pygame.font.SysFont('Arial', 30)
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        pygame.display.set_caption('WESTERN(Для выхда из игры нажать ESC)')
        self.bg = pygame.image.load('assets/images/background_v2.png')
        self.shot_sound = pygame.mixer.Sound('assets/sound/shot.wav')
        self.player = Player(800, 300)
        self.enemy = Enemy(250, 100)
        self.aim = Aim(self.enemy, shake_power=1, shake_frequency=0)
        self.shoot_timer = Timer(FPS, 0.33)
        self.attack_timer = Timer(FPS, 20)
        self.pre_attack_timer = Timer(FPS, 5)
        self.requst_timer = Timer(FPS, 2)
        self.all_sprite_list = pygame.sprite.Group()
        self.all_sprite_list.add(self.player)
        self.all_sprite_list.add(self.enemy)

        self.all_sprite_list.add(self.aim.bullet_hole)
        self.clock = pygame.time.Clock()
        self.battle_permissions = get_info(
            f'http://{self.url}/get_permissions')

        self.attack_timer_HBA = False  # attack_timer Has Been Activeted
        self.pre_attack_timer_HBA = False  # pre_attack_timer Has Been Activeted

        self.HBS = False

        self.input_field = vkii.TextInput(
            (200, 60), (400, 240), ISCANDER_RED, RED, (100, 100, 100), font_size=50)

        self.players_count = 2

        self.in_menu = False

        self.table = vkii.Table((1000, 700), (50, 50, 50),
                                ISCANDER_RED, 40, (100, 50))

        self.players_scores = []

    def draw(self):
        self.screen.blit(self.bg, (0, 0))

        self.all_sprite_list.draw(self.screen)
        if self.input_field.final_text == '':
            self.screen.blit(self.input_field.image, self.input_field.rect)
            self.screen.blit(
                self.input_field.rendered_text[0], self.input_field.rendered_text[1])
        if self.attack_timer.active:
            text = self.font.render(
                str(self.attack_timer.time), False, ISCANDER_RED)
            coord = (self.aim.rect.x+25, self.aim.rect.y-35)
            self.screen.blit(text, coord)

        if self.pre_attack_timer.active:
            pre_text = self.font.render(
                str(int(round(self.pre_attack_timer.time, 0))), False, ISCANDER_RED)
            pre_coord = (600+25, 400-35)
            self.screen.blit(pre_text, pre_coord)

        if not len(self.battle_permissions) == self.players_count and self.input_field.final_text != '':
            self.screen.blit(self.font.render(
                'Нажмите SPACE для начала игры', False, ISCANDER_RED), (400, 400))

        if len(self.players_scores) == self.players_count:
            self.screen.blit(self.table.image, self.table.rect)
            for i in self.table.rendered_text:
                self.screen.blit(i[0], i[1])

    def move_aim(self):
        rel = pygame.mouse.get_rel()
        # следующее строки не позволяют курсору выйти за пределы окна
        if abs(rel[0]) < 150:
            self.aim.rect[0] += rel[0]
        if abs(rel[1]) < 60:
            self.aim.rect[1] += rel[1]

    def score_culculate(self):
        """
        Этот метод подсчитывает количество очков набранных за выстрел
        """
        block_hit_list = pygame.sprite.spritecollide(
            self.enemy, [self.aim.bullet_hole], False, pygame.sprite.collide_mask)
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
        print(requests.post(url=f'http://{self.url}/post_score', json={
              'name': self.name, 'score': self.score_culculate()}).content)

    def event_check(self, event):
        """
        В этом методе проверяется тип ивента.
        """

        if self.input_field.final_text != '':
            self.name = self.input_field.final_text
            if not self.requst_timer.active:
                requests.post(
                    url=f'http://{self.url}/session', json={'name': self.name})
        else:
            self.input_field.update(event)
        # если attack_timer запущен и оба игрока нажали space, у игрока появляется возможность выстрелить
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.attack_timer.active and self.HBS != True:
                self.shoot()
                self.HBS = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                requests.post(
                    f'http://{self.url}/post_permission', json={'name': self.name})

        if event.type == pygame.QUIT:
            # здесь возвращается True и в главном цикле присваевается локальная переменная "done"
            return True

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.in_menu = True if not self.in_menu else False

    def run(self):
        pygame.mixer.music.load('assets/sound/music.ogg')
        pygame.mixer.music.play()
        done = False
        while not done:
            if not self.requst_timer.active:
                self.battle_permissions = list(
                    get_info(f'http://{self.url}/get_permissions').values())
                self.players_scores = list(
                    get_info(f'http://{self.url}/get_scores').values())
                self.requst_timer.start()
            if len(self.players_scores) == self.players_count and self.table.content == []:
                self.table.content = list(
                    get_info(f'http://{self.url}/score_sort').values())
            # обновление таймеров
            self.shoot_timer.update()
            self.attack_timer.update()
            self.pre_attack_timer.update()
            self.requst_timer.update()

            # изменение спрайта игрока на стандартный через 0.33 сек. после выстрела
            if not self.shoot_timer.active:
                self.player.image = self.player.stand_img

            self.draw()
            if self.in_menu:
                self.screen.blit(pygame.image.load(
                    './assets/images/very_cool_name_for_png_file.png'), (0, 0))
            for event in pygame.event.get():
                done = self.event_check(event)

            # если оба игрока нажали пробел запускается таймер
            if len(self.battle_permissions) == self.players_count and not self.pre_attack_timer_HBA:
                pygame.mouse.set_visible(False)
                self.pre_attack_timer.start()
                self.pre_attack_timer_HBA = True

            if self.pre_attack_timer_HBA and not self.pre_attack_timer.active and not self.attack_timer.active and self.attack_timer_HBA != True:
                self.attack_timer.start()
                self.all_sprite_list.add(self.aim)
                pygame.mouse.set_pos((600, 400))
                self.attack_timer_HBA = True

            if self.pre_attack_timer.active or self.attack_timer.active and not self.in_menu:
                pos = pygame.mouse.get_pos()
                if pos[0] < 400 or pos[0] > 800:
                    pygame.mouse.set_pos(600, pos[1])
                pos = pygame.mouse.get_pos()
                if pos[1] < 300 or pos[1] > 500:
                    pygame.mouse.set_pos(pos[0], 400)
            if self.in_menu:
                pygame.mouse.set_visible(True)
            elif self.pre_attack_timer.active or self.attack_timer.active:
                pygame.mouse.set_visible(False)

            # когда attack_timer запущен, появляется возможность двигать прицелом
            if self.attack_timer.active:
                self.move_aim()

            # обновление спрайтов и окна игры
            self.all_sprite_list.update()
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()


game = Game(input("\"ip:port\": "))
game.run()
