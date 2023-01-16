import os
import pygame
import sys

FPS = 50
pygame.init()
size = WIDTH, HEIGHT = 700, 700
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
running = True


def load_image(name, color_key=None):
    fullname = os.path.join('', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


tile_images = {
    'wall': pygame.image.load('data/wall.png').convert(),
    'box': pygame.image.load('data/box.png').convert(),
    'empty': pygame.image.load('data/grass.png').convert(),
    'empty_x': pygame.image.load('data/grass_x.png').convert(),
    'box_x': pygame.image.load('data/not_orig.jpg').convert()
}
player_image = pygame.image.load('data/mar.png').convert()

tile_width = tile_height = 50


class SpriteGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


class ScreenFrame(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = (0, 0, 500, 500)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * self.pos[0] + 15,
                                               tile_height * self.pos[1] + 5)


player = None

sprite_group = SpriteGroup()
hero_group = SpriteGroup()


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(pygame.image.load('data/fon.jpg').convert(), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)



def load_level(filename):
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    return level_map


def generate_level(level):
    new_player, x, y, x_p, y_p = None, None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                x_p, y_p = x, y
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == 'X':
                Tile('empty_x', x, y)
            elif level[y][x] == 'O':
                Tile('box', x, y)
            elif level[y][x] == 'Q':
                Tile('box_x', x, y)

    return new_player, x, y, x_p, y_p


def move(hero, movement, x, y):
    if movement == 'up':
        if y > 0 and level_map[y - 1][x] == '.':
            hero.move(x, y - 1)
            return x, y - 1
    if movement == 'down':
        if y > 0 and level_map[y + 1][x] == '.':
            hero.move(x, y + 1)
            return x, y + 1
    if movement == 'left':
        if x >= 0 and level_map[y][x - 1] == '.':
            hero.move(y, x - 1)
            return x - 1, y
    if movement == 'right':
        if x >= 0 and level_map[y][x + 1] == '.':
            hero.move(y, x + 1)
            return x + 1, y


if __name__ == '__main__':
    pygame.display.set_caption('Марио')
    player = None
    running = True
    start_screen()
    level_map = load_level('data/map.txt')
    hero, max_x, max_y, x_p, y_p = generate_level(level_map)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    x_p, y_p = move(hero, 'up', x_p, y_p)
                if event.key == pygame.K_DOWN:
                    move(hero, 'down', x_p, y_p)
                if event.key == pygame.K_RIGHT:
                    move(hero, 'right', x_p, y_p)
                if event.key == pygame.K_LEFT:
                    move(hero, 'left', x_p, y_p)
        screen.fill(pygame.Color('black'))
        sprite_group.draw(screen)
        hero_group.draw(screen)
        pygame.display.flip()
    pygame.quit()