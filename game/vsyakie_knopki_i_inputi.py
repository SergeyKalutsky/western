import pygame
pygame.init()

class Button(pygame.sprite.Sprite):
    def __init__(self, size, position):
        super().__init__()
        self.image = pygame.Surface(size)
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.position = position
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
    def update(self, event):
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
        if self.rect.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.if_activated()
    def if_activated(self):
        pass

class ExitButton(Button):
    def __init__(self, size, position):
        super().__init__(size, position)
    def if_activated(self):
        pygame.quit()


class TextInput(pygame.sprite.Sprite):
    def __init__(self, size, position, color, activated_color, text_color, font='Arial', font_size=20):
        super().__init__()
        self.color = color
        self.activated_color = activated_color

        self.image = pygame.Surface(size)
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.position = position
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
        self.activated = False

        self.text = ''
        self.final_text = ''

        self.text_color = text_color
        self.font = font
        self.font_size = font_size
    def update(self, event):
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
        if self.rect.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.activated = True
        if not self.rect.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.activated = False
        
        if self.activated:
            self.image.fill(self.activated_color)
            if event.type == pygame.KEYDOWN:
                if event.key == 8:
                    self.text = self.text[:-1]
                elif event.key == 13:
                    self.final_text = self.text
                    self.activated = False
                else:
                    self.text += event.unicode
        else:
            self.image.fill(self.color)
    @property
    def rendered_text(self):
        if self.font != 'Arial':
            return pygame.font.Font(self.font, self.font_size).render(self.text, 1, self.text_color), self.rect
        return pygame.font.SysFont('Arial', self.font_size).render(self.text, 1, self.text_color), self.rect



class Table(pygame.sprite.Sprite):
    def __init__(self, size, color, font_color, font_size, position):
        super().__init__()
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.content = []

        self.font_color = font_color
        self.font_size = font_size

    @property
    def rendered_text(self):
        self.text = '№   Name   Score\n'
        self.result = []
        for i in range(len(self.content)):
            self.text += f'{i+1}    {self.content[i][0]}       {self.content[i][1]}\n'
        for i in self.text.split('\n'):
            self.result.append(i)
        for i in range(len(self.result)):
            self.result[i] = pygame.font.SysFont('Arial', self.font_size).render(self.result[i], 1, self.font_color), (self.rect.x, self.rect.y + i*self.font_size*1.5)
        return self.result
