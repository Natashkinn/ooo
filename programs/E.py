import os
import sys
from random import choice, randint

import pyautogui as pyautogui
import pygame

width, height = 700, 700
screen_rect = (0, 0, width, height)
particles = []


def DrawPictures():
    for i in particles:
        i.render(screen)
        if i.radius <= 0:
            particles.remove(i)


def create_particles(position, all_sprites):
    # количество создаваемых частиц
    particle_count = 10
    # возможные скорости
    numbers = range(-60, 60)
    for _ in range(particle_count):
        Particle(position, choice(numbers), choice(numbers), all_sprites, 0, screen_rect, ['programs/data/box.png'])


def load_image(name, colorkey=None):
    fullname = name
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, all_sprites0):
        super().__init__(all_sprites0)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Particle_2:
    def __init__(self, x, y, x_vel, y_vel, radius, color, gravity=None):
        self.x = x
        self.y = y
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.radius = radius
        self.color = color
        self.gravity = gravity

    def render(self, screen):
        self.x += self.x_vel
        self.y += self.y_vel
        if self.gravity:
            self.y_vel += self.gravity
        self.radius -= 0.1
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)


class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, dx, dy, all_sprites, GRAVITY, screen_rect, image_name):
        super().__init__(all_sprites)
        fire = [[load_image(i) for i in image_name]]
        for scale in (20, 25, 30):
            fire.append(pygame.transform.scale(choice(fire[0]), (scale, scale)))
        self.screen_rect = screen_rect
        self.image = choice(fire[1:])
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = GRAVITY

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(self.screen_rect):
            self.kill()


def load_level(filename):
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))
    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


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


class Sprite_Mouse_Location(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0, 0, 1, 1)


class Mouse(pygame.sprite.Sprite):
    image = load_image("programs/data/curs.png")

    def __init__(self, group):
        super().__init__(group)
        self.image = Mouse.image
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100

    def update(self, x, y):
        if pygame.mouse.get_focused():
            self.rect.x = x - 10
            self.rect.y = y - 10


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 5, tile_height * pos_y + 5)
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
    all_sprites = pygame.sprite.Group()
    intro_text = ['Побег из лабиринта',
                  '(с анекдотами)',
                  'Выберите уровень сложности:',
                  'Легкий',
                  'Продвинутый']
    fon = pygame.transform.scale(load_image('programs/data/fon.png'), (700, 700))
    screen.blit(fon, (0, 0))
    mouse_sprite = Sprite_Mouse_Location()
    mouse_but = pygame.sprite.Group()
    pygame.mouse.set_visible(False)
    cloud = AnimatedSprite(load_image("programs/data/cloud.png"), 8, 2, 0, 610, all_sprites)
    color = (255, 255, 255)
    pygame.draw.rect(screen, color, (140, 390, 420, 70))
    pygame.draw.rect(screen, color, (140, 520, 420, 70))
    font = pygame.font.SysFont('times new roman', 80)
    string_rendered1 = font.render(intro_text[0], True, pygame.Color('pink'))
    screen.blit(string_rendered1, (10, 50))
    font = pygame.font.SysFont('times new roman', 40)
    string_rendered2 = font.render(intro_text[1], True, pygame.Color('pink'))
    screen.blit(string_rendered2, (240, 115))
    font = pygame.font.SysFont('times new roman', 50)
    string_rendered3 = font.render(intro_text[2], True, pygame.Color('pink'))
    screen.blit(string_rendered3, (20, 280))
    font = pygame.font.SysFont('times new roman', 60)
    string_rendered4 = font.render(intro_text[3], True, pygame.Color('pink'))
    screen.blit(string_rendered4, (260, 390))
    string_rendered5 = font.render(intro_text[4], True, pygame.Color('pink'))
    screen.blit(string_rendered5, (180, 520))
    mouse = Mouse(mouse_but)
    while True:
        colors = [(randint(100, 255), randint(100, 255), randint(100, 255))]
        pos = pygame.mouse.get_pos()
        mouse_sprite.rect.x = pos[0]
        mouse_sprite.rect.y = pos[1]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # создаём частицы по щелчку мыши
                create_particles(pygame.mouse.get_pos(), all_sprites)
                if event.pos[0] in range(140, 561) and event.pos[1] in range(390, 461):
                    return 0
                    # Начинаем простую игру
                if event.pos[0] in range(140, 561) and event.pos[1] in range(520, 591):
                    return 1
                    # начинаем продвинутую игру
            if event.type == pygame.MOUSEMOTION:
                mouse_but.update(pos[0], pos[1])
        pos = pygame.mouse.get_pos()
        for x in range(randint(15, 25)):
            particle = Particle_2(pos[0], pos[1], randint(0, 200) / 100,
                                  randint(-3, -1), randint(-10, 10), choice(colors), 0.06)
            particles.append(particle)
        screen.blit(fon, (0, 0))
        pygame.draw.rect(screen, color, (140, 390, 420, 70))
        pygame.draw.rect(screen, color, (140, 520, 420, 70))
        screen.blit(string_rendered1, (10, 50))
        screen.blit(string_rendered2, (240, 115))
        screen.blit(string_rendered3, (20, 280))
        screen.blit(string_rendered4, (260, 390))
        screen.blit(string_rendered5, (180, 520))
        all_sprites.update()
        all_sprites.draw(screen)
        DrawPictures()
        mouse_but.draw(screen)
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
    # pygame.mixer.music.play(-1)
    screen = pygame.display.set_mode(size)
    color = (255, 255, 255)
    screen.fill(color)
    maps_easy = ['programs/data/easy_1.txt',
                 'programs/data/easy_2.txt',
                 'programs/data/easy_3.txt']
    maps_hard = ['programs/data/hard_3.txt',
                 'programs/data/hard_3.txt',
                 'programs/data/hard_3.txt']
    FPS = 20
    tile_images = {
        'wall': pygame.image.load('programs/data/wall.png').convert(),
        'box': pygame.image.load('programs/data/box.png').convert(),
        'empty': pygame.image.load('programs/data/grass.png').convert(),
        'exit': pygame.image.load('programs/data/door.jpg').convert(),
    }
    player_image = pygame.image.load('programs/data/cat.png')
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                # создаём частицы по щелчку мыши
                create_particles(pygame.mouse.get_pos(), all_sprites)
        fill_color = pygame.Color('lightblue')
        screen.fill(fill_color)
        tiles_group.draw(screen)
        camera.update(player)
        ticks = pygame.time.get_ticks() - start_time
        seconds = int(ticks / 1000 % 60)
        minutes = int(ticks / 60000 % 24)
        out = '{minutes:02d}:{seconds:02d}'.format(minutes=minutes, seconds=seconds)
        string_rendered = font.render(out, True, pygame.Color('red'))
        screen.blit(string_rendered, (100, 40))
        clock.tick(60)
        for sprite in all_sprites:
            camera.apply(sprite)
        all_sprites.update()
        all_sprites.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
    pygame.quit()
