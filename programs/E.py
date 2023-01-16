import os
import sys
from random import choice

import pyautogui as pyautogui
import pygame


def load_level(filename):
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))
    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def load_image(name, colorkey=None):
    fullname = name
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        if x < 0:
            if move(player, 'left'):
                self.rect = self.rect.move(x, y)
                self.pos = (self.pos[0] - 1, self.pos[1])
        elif x > 0:
            if move(player, 'right'):
                self.rect = self.rect.move(x, y)
                self.pos = (self.pos[0] + 1, self.pos[1])
        elif y > 0:
            if move(player, 'down'):
                self.rect = self.rect.move(x, y)
                self.pos = (self.pos[0], self.pos[1] + 1)
        elif y < 0:
            if move(player, 'up'):
                self.rect = self.rect.move(x, y)
                self.pos = (self.pos[0], self.pos[1] - 1)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    def move(self, x, y, minutes, seconds, jokes):
        with open('programs/data/jokes.txt', encoding='utf8') as file:
            text_joke = choice(''.join(file.readlines()).split('***'))

        if x < 0:
            if move(player, 'left') == 10:
                jokes += 1
                self.rect = self.rect.move(x, y)
                self.pos = (self.pos[0] - 1, self.pos[1])
                pyautogui.alert(title='анекдот', text=text_joke)
            if move(player, 'left') == 888:
                self.rect = self.rect.move(x, y)
                self.pos = (self.pos[0] - 1, self.pos[1])
                finish_screen(minutes, seconds, jokes)
            elif move(player, 'left'):
                self.rect = self.rect.move(x, y)
                self.pos = (self.pos[0] - 1, self.pos[1])
        elif x > 0:
            if move(player, 'right') == 10:
                jokes += 1
                self.rect = self.rect.move(x, y)
                self.pos = (self.pos[0] + 1, self.pos[1])
                pyautogui.alert(title='анекдот', text=text_joke)
            if move(player, 'right') == 888:
                self.rect = self.rect.move(x, y)
                self.pos = (self.pos[0] + 1, self.pos[1])
                finish_screen(minutes, seconds, jokes)
            elif move(player, 'right'):
                self.rect = self.rect.move(x, y)
                self.pos = (self.pos[0] + 1, self.pos[1])
        elif y > 0:
            if move(player, 'down') == 10:
                jokes += 1
                self.rect = self.rect.move(x, y)
                self.pos = (self.pos[0], self.pos[1] + 1)
                pyautogui.alert(title='анекдот', text=text_joke)
            elif move(player, 'down') == 888:
                self.rect = self.rect.move(x, y)
                self.pos = (self.pos[0], self.pos[1] + 1)
                finish_screen(minutes, seconds, jokes)
            elif move(player, 'down'):
                self.rect = self.rect.move(x, y)
                self.pos = (self.pos[0], self.pos[1] + 1)
        elif y < 0:
            if move(player, 'up') == 10:
                jokes += 1
                self.rect = self.rect.move(x, y)
                self.pos = (self.pos[0], self.pos[1] - 1)
                pyautogui.alert(title='анекдот', text=text_joke)
            if move(player, 'up') == 888:
                self.rect = self.rect.move(x, y)
                self.pos = (self.pos[0], self.pos[1] - 1)
                finish_screen(minutes, seconds, jokes)
            elif move(player, 'up'):
                self.rect = self.rect.move(x, y)
                self.pos = (self.pos[0], self.pos[1] - 1)
        return jokes


def terminate():
    pygame.quit()
    sys.exit()


def finish_screen(minutes, seconds, jokes):
    outro_text = ['Победа!',
                  'Время выполнения:',
                  f'{minutes} {ending_min(minutes)} ',
                  f'{seconds} {ending_sec(seconds)}',
                  'Собрано',
                  str(jokes),
                  ending_anec(jokes)]
    fon = pygame.transform.scale(load_image('programs/data/fon.png'), (700, 700))
    screen.blit(fon, (0, 0))
    color = (255, 255, 255)
    font = pygame.font.SysFont('times new roman', 80)
    string_rendered = font.render(outro_text[0], True, pygame.Color('pink'))
    screen.blit(string_rendered, (10, 50))
    font = pygame.font.SysFont('times new roman', 50)
    string_rendered = font.render(outro_text[1], True, pygame.Color('pink'))
    screen.blit(string_rendered, (10, 150))
    string_rendered = font.render(outro_text[2], True, pygame.Color('pink'))
    screen.blit(string_rendered, (10, 220))
    string_rendered = font.render(outro_text[3], True, pygame.Color('pink'))
    screen.blit(string_rendered, (200, 220))
    string_rendered = font.render(outro_text[4], True, pygame.Color('pink'))
    screen.blit(string_rendered, (10, 300))
    string_rendered = font.render(outro_text[5], True, pygame.Color('pink'))
    screen.blit(string_rendered, (200, 300))
    string_rendered = font.render(outro_text[6], True, pygame.Color('pink'))
    screen.blit(string_rendered, (240, 300))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    intro_text = ['Побег из лабиринта',
                  '(с анекдотами)',
                  'Выберите уровень сложности:',
                  'Легкий',
                  'Продвинутый']
    fon = pygame.transform.scale(load_image('programs/data/fon.png'), (700, 700))
    screen.blit(fon, (0, 0))
    color = (255, 255, 255)
    pygame.draw.rect(screen, color, (140, 390, 420, 70))
    pygame.draw.rect(screen, color, (140, 520, 420, 70))
    font = pygame.font.SysFont('times new roman', 80)
    string_rendered = font.render(intro_text[0], True, pygame.Color('pink'))
    screen.blit(string_rendered, (10, 50))
    font = pygame.font.SysFont('times new roman', 40)
    string_rendered = font.render(intro_text[1], True, pygame.Color('pink'))
    screen.blit(string_rendered, (240, 115))
    font = pygame.font.SysFont('times new roman', 50)
    string_rendered = font.render(intro_text[2], True, pygame.Color('pink'))
    screen.blit(string_rendered, (20, 280))
    font = pygame.font.SysFont('times new roman', 60)
    string_rendered = font.render(intro_text[3], True, pygame.Color('pink'))
    screen.blit(string_rendered, (260, 390))
    string_rendered = font.render(intro_text[4], True, pygame.Color('pink'))
    screen.blit(string_rendered, (180, 520))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] in range(140, 561) and event.pos[1] in range(390, 461):
                    return 0
                    # Начинаем простую игру
                if event.pos[0] in range(140, 561) and event.pos[1] in range(520, 591):
                    return 1
                    # начинаем продвинутую игру
        pygame.display.flip()
        clock.tick(FPS)


def ending_anec(anec):
    if anec in range(5, 20):
        return 'анекдотов'
    elif anec % 10 == 1:
        return 'анекдот'
    elif anec % 10 == 0:
        return 'анекдотов'
    elif anec % 10 in [2, 3, 4]:
        return 'анекдота'
    elif anec % 10 in range(5, 10):
        return 'анекдотов'


def ending_sec(sec):
    if sec in range(5, 20):
        return 'секунд'
    elif sec % 10 == 1:
        return 'секунда'
    elif sec % 10 == 0:
        return 'секунд'
    elif sec % 10 in [2, 3, 4]:
        return 'секунды'
    elif sec % 10 in range(5, 10):
        return 'секунд'


def ending_min(min):
    if min in range(5, 20):
        return 'минут'
    elif min % 10 == 1:
        return 'минута'
    elif min % 10 == 0:
        return 'минут'
    elif min % 10 in [2, 3, 4]:
        return 'минуты'
    elif min % 10 in range(5, 10):
        return 'минут'


def choose_easy_level():
    choose_text = ['Простой уровень',
                   'Выберите номер уровня',
                   '1', '2', '3']
    fon = pygame.transform.scale(load_image('programs/data/fon.png'), (700, 700))
    screen.blit(fon, (0, 0))
    color = (255, 255, 255)
    pygame.draw.rect(screen, color, (40, 220, 200, 200))
    pygame.draw.rect(screen, color, (250, 220, 200, 200))
    pygame.draw.rect(screen, color, (460, 220, 200, 200))
    font = pygame.font.SysFont('times new roman', 90)
    string_rendered = font.render(choose_text[0], True, pygame.Color('pink'))
    screen.blit(string_rendered, (30, 5))
    font = pygame.font.SysFont('times new roman', 60)
    string_rendered = font.render(choose_text[1], True, pygame.Color('pink'))
    screen.blit(string_rendered, (50, 130))
    font = pygame.font.SysFont('times new roman', 190)
    string_rendered = font.render(choose_text[2], True, pygame.Color('pink'))
    screen.blit(string_rendered, (100, 230))
    string_rendered = font.render(choose_text[3], True, pygame.Color('pink'))
    screen.blit(string_rendered, (310, 230))
    string_rendered = font.render(choose_text[4], True, pygame.Color('pink'))
    screen.blit(string_rendered, (520, 230))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] in range(40, 241) and event.pos[1] in range(190, 391):
                    return 0
                if event.pos[0] in range(250, 451) and event.pos[1] in range(190, 391):
                    return 1
                if event.pos[0] in range(460, 661) and event.pos[1] in range(190, 391):
                    return 2
        pygame.display.flip()


def choose_hard_level():
    choose_text = ['Сложный уровень',
                   'Выберите номер уровня',
                   '1', '2', '3']
    fon = pygame.transform.scale(load_image('programs/data/fon.png'), (700, 700))
    screen.blit(fon, (0, 0))
    color = (255, 255, 255)
    pygame.draw.rect(screen, color, (40, 220, 200, 200))
    pygame.draw.rect(screen, color, (250, 220, 200, 200))
    pygame.draw.rect(screen, color, (460, 220, 200, 200))
    font = pygame.font.SysFont('times new roman', 88)
    string_rendered = font.render(choose_text[0], True, pygame.Color('pink'))
    screen.blit(string_rendered, (10, 5))
    font = pygame.font.SysFont('times new roman', 60)
    string_rendered = font.render(choose_text[1], True, pygame.Color('pink'))
    screen.blit(string_rendered, (50, 130))
    font = pygame.font.SysFont('times new roman', 190)
    string_rendered = font.render(choose_text[2], True, pygame.Color('pink'))
    screen.blit(string_rendered, (100, 230))
    string_rendered = font.render(choose_text[3], True, pygame.Color('pink'))
    screen.blit(string_rendered, (310, 230))
    string_rendered = font.render(choose_text[4], True, pygame.Color('pink'))
    screen.blit(string_rendered, (520, 230))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] in range(40, 241) and event.pos[1] in range(190, 391):
                    return 0
                if event.pos[0] in range(250, 451) and event.pos[1] in range(190, 391):
                    return 1
                if event.pos[0] in range(460, 661) and event.pos[1] in range(190, 391):
                    return 2
        pygame.display.flip()


def generate_level(level):
    new_player = None
    x = None
    y = None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == 'O':
                Tile('box', x, y)
            elif level[y][x] == 'e':
                Tile('exit', x, y)
    return new_player, x, y


def move(hero, movement):
    x, y = hero.pos
    if movement == 'up':
        if y > 0 and (level_map[y - 1][x] == 'O' or level_map[y - 1][x] == 'Q'):
            return 10
        if level_map[y - 1][x] == 'e':
            return 888
        if y > 0 and (level_map[y - 1][x] == '.' or level_map[y - 1][x] == '@' or level_map[y - 1][x] == 'X'):
            return True
    elif movement == 'down':
        if y < level_y and (level_map[y + 1][x] == 'O' or level_map[y + 1][x] == 'Q'):
            return 10
        if level_map[y + 1][x] == 'e':
            return 888
        if y < level_y and (level_map[y + 1][x] == '.' or level_map[y + 1][x] == '@'):
            return True
    elif movement == 'left':
        if x > 0 and (level_map[y][x - 1] == 'O' or level_map[y][x - 1] == 'Q'):
            return 10
        if level_map[y][x - 1] == 'e':
            return 888
        if x > 0 and (level_map[y][x - 1] == '.' or level_map[y][x - 1] == '@'):
            return True
    elif movement == 'right':
        if x < level_x and level_map[y][x + 1] == 'O':
            return 10
        if level_map[y][x + 1] == 'e':
            return 888
        if x < level_x and (level_map[y][x + 1] == '.' or level_map[y][x + 1] == '@'):
            return True


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0
    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy
    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Labyrinth')
    size = width, height = 700, 700
    clock = pygame.time.Clock()
    pygame.mixer.music.load("programs/data/tatar.mp3")
    pygame.mixer.music.play(-1)
    screen = pygame.display.set_mode(size)
    color = (255, 255, 255)
    screen.fill(color)
    maps_easy = ['programs/data/easy_1.txt',
                 'programs/data/easy_2.txt',
                 'programs/data/easy_3.txt']
    maps_hard = ['programs/data/hard_3.txt',
                 'programs/data/hard_3.txt',
                 'programs/data/hard_3.txt']
    FPS = 50
    tile_images = {
        'wall': pygame.image.load('programs/data/wall.png').convert(),
        'box': pygame.image.load('programs/data/box.png').convert(),
        'empty': pygame.image.load('programs/data/grass.png').convert(),
        'exit': pygame.image.load('programs/data/door.jpg').convert(),
    }
    player_image = pygame.image.load('programs/data/mar.png').convert()
    tile_width = tile_height = 50
    tip = start_screen()
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    if tip == 0:
        level_map = load_level(maps_easy[choose_easy_level()])
    else:
        level_map = load_level(maps_hard[choose_hard_level()])
    player, level_x, level_y = generate_level(level_map)
    start_time = pygame.time.get_ticks()
    running = True
    camera = Camera()
    font = pygame.font.SysFont('footlight', 34)
    minutes = 0
    seconds = 0
    count = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    count = player.move(0, -50, minutes, seconds, count)
                if event.key == pygame.K_DOWN:
                    count = player.move(0, 50, minutes, seconds, count)
                if event.key == pygame.K_RIGHT:
                    count = player.move(50, 0, minutes, seconds, count)
                if event.key == pygame.K_LEFT:
                    count = player.move(-50, 0, minutes, seconds, count)
        fill_color = pygame.Color('lightblue')
        screen.fill(fill_color)
        tiles_group.draw(screen)
        player_group.draw(screen)
        camera.update(player)
        ticks = pygame.time.get_ticks() - start_time
        seconds = int(ticks / 1000 % 60)
        minutes = int(ticks / 60000 % 24)
        out = '{minutes:02d}:{seconds:02d}'.format(minutes=minutes, seconds=seconds)
        string_rendered = font.render(out, True, pygame.Color('red'))
        screen.blit(string_rendered, (100, 40))
        pygame.display.flip()
        clock.tick(60)
        for sprite in all_sprites:
            camera.apply(sprite)
        pygame.display.flip()
    pygame.quit()
