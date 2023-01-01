import pygame
from settings import *
from pygame_widgets.button import Button
import pygame_widgets


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, cadres_code, cadres_number, *group):
        super().__init__(*group)
        self.cadres_info = (cadres_code, cadres_number)

class Figure(AnimatedSprite):

    def __init__(self, x, y, cadre_code, cadre_number, *group):
        super().__init__(cadre_code, cadre_number, *group)
        self.cadres = []
        for i in range(cadre_number):
            self.cadres.append(f'data/png/figure_{cadre_code}_{i + 1}.png')
        self.passive_update()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def passive_update(self):
        self.cadres = [self.cadres[-1]] + self.cadres[1:]
        self.image = pygame.image.load(self.cadres[0])


class ControlledHero(Figure):

    def __init__(self, x, y, cadre_code, cadre_number, *group):
        super().__init__(x, y, cadre_code, cadre_number, *group)
    
    def update(self, events):
        self.passive_update()
        keys = [pygame.K_RIGHT, pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN]
        for i in range(len(keys)):
            if events[keys[i]]:
                self.image = pygame.image.load(f'data/png/figure_{self.cadres_info[0]}_{SIDES[i]}.png')


class Bot(Figure):
    
    def __init__(self, x, y, cadre_code, cadre_number, hardless, *group):
        super().__init__(x, y, cadre_code, cadre_number, *group)
        self.hard = hardless

    def update(self, events) -> None:
        self.passive_update()


class Menu:

    def __init__(self, screen, buttons_tuple):
        self.buttons = buttons_tuple
        self.screen = screen

    def update(self, events):
        for btn in self.buttons:
            btn.listen(events)
            if btn.isVisible():
                btn.draw()

    def hide(self):
        for btn in self.buttons:
            btn.hide()

    def show(self):
        for btn in self.buttons:
            btn.show()


class ActiveArea:

    def __init__(self, first_scene):
        self.current_scene = first_scene
        self.width, self.height = ACTIVE_AREA_WIDTH, ACTIVE_AREA_HEIGHT

    def __add__(self, scene):
        self.current_scene = self.current_scene[4:] + scene
        return self

    def update(self):
        self.arrows = pygame.sprite.Group()
        for i in range(len(self.current_scene)):
            if self.current_scene[i] == '1':
                row, col = i // 4, i % 4
                x = row * 32
                y = 100 + col * 125 + current_night.areas.index(self) * 500
                Arrow(y, x, row, col, self.current_scene, self.arrows)

    def draw(self):
        self.arrows.draw(screen)


class Arrow(pygame.sprite.Sprite):
    images = ('data/png/right_arrow.png', 'data/png/up_arrow.png',
        'data/png/left_arrow.png', 'data/png/down_arrow.png')
    line_images = ('data/png/right_arrow_line.png', 'data/png/up_arrow_line.png',
        'data/png/left_arrow_line.png', 'data/png/down_arrow_line.png')

    def __init__(self, pos_x, pos_y, row, col, scene, *group):
        super().__init__(*group)
        self.image = pygame.image.load(Arrow.line_images[col]).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y


class Night:

    def __init__(self, night_number):

        self.sound = NIGHT_CODES[night_number]
        pygame.mixer.music.load(f'data/music/{self.sound}.wav')
        pygame.mixer.music.play()
        self.txt_file = open(f'data/txt/{self.sound}.txt')
        self.background = pygame.image.load(f'data/png/night_{night_number}.png')

        first_scenes = self._read_full_scene()
        self.areas = [ActiveArea(first_scenes[0]), ActiveArea(first_scenes[1])]

    def _read_full_scene(self):

        scene1, scene2 = '', ''
        for i in range(ACTIVE_ROWS):
            scene1, scene2 = self.add_one_row(scene1, scene2)
        return(scene1, scene2)
        
    def add_one_row(self, scene1, scene2):
        scene1 += self.txt_file.read(4)
        scene2 += self.txt_file.read(4)
        return (scene1, scene2)
    
    def update(self):
        scenes = self.add_one_row('', '')
        self.areas = [self.areas[0] + scenes[0], self.areas[1] + scenes[1]]
        for area in self.areas:
            area.update()

    def draw(self):
        for area in self.areas:
            area.draw()



def menu_buttons_array(screen):
    start_game_button = Button(screen, WIDTH / 2 - 250, HEIGHT / 2 + 50, 500, 100, 0, text='Начать игру',
        textColour=(255, 255, 255), fontSize=50, hoverColour=(200, 10, 200), onClick=open_choosing_night_menu, colour=(0, 0, 0), radius=50)
    godmode_button = Button(screen, WIDTH / 2 - 250, HEIGHT / 2 + 200, 500, 100, 0, text='Godmode',
        textColour=(255, 255, 255), fontSize=50, hoverColour=(255, 100, 100), onClick=reedit_godmode, colour=(0, 0, 0), radius=50)
    return [start_game_button, godmode_button]


def reedit_godmode():
    global GODMODE
    GODMODE = not GODMODE

    if GODMODE:
        main_menu.buttons[1].setHoverColour((20, 200, 20))
    else:
        main_menu.buttons[1].setHoverColour((255, 100, 100))


def choose_night_menu_buttons_array(screen):
    start_x, y = 100, 350
    array = []
    for i in range(5):
        button = Button(screen, start_x + i * 275, y, 200, 300, 0, text=f'Ночь {i + 1}',
            textColour=(255, 255, 255), fontSize=50, hoverColour=(200, 10, 200), colour=(0, 0, 0), radius=25)
        button.setOnClick(start_night, (button.getX(),))
        array.append(button)
    button = Button(screen, WIDTH / 2 - 250, HEIGHT / 2 - 200, 500, 100, 0, text='Назад в главное меню', onClick=open_main_menu,
        textColour=(255, 255, 255), fontSize=50, hoverColour=(200, 10, 200), colour=(0, 0, 0), radius=50)
    array.append(button)
    return array


def start_night(night_number):
    global in_menu, in_choosing_game_menu, in_game, current_night, choose_game_menu, current_bot, current_hero, figures_sprite_group

    night_number = (night_number - 100) // 275 + 1
    in_menu, in_choosing_game_menu, in_game = False, False, True
    choose_game_menu.hide()
    current_night = Night(night_number)

    hero, bot = ControlledHero(1000, 500, 1, 2, figures_sprite_group), Bot(300, 500, 2, 2, 50, figures_sprite_group)


def open_main_menu():
    global in_menu, in_choosing_game_menu, in_game, choose_game_menu, main_menu
    in_menu, in_choosing_game_menu, in_game = True, False, False
    choose_game_menu.hide()
    main_menu.show()


def open_choosing_night_menu():
    global in_menu, in_choosing_game_menu, in_game, choose_game_menu, main_menu
    in_menu, in_choosing_game_menu, in_game = False, True, False
    choose_game_menu.show()
    main_menu.hide()


if __name__ == '__main__':
    pygame.init()
    pygame.mouse.set_visible(False)

    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption('Игра')
    logo = pygame.image.load('data/png/logo.png')
    pygame.display.set_icon(logo)
    
    running = True
    clock = pygame.time.Clock()

    in_menu = True
    in_choosing_game_menu = False
    in_game = False

    GODMODE = False

    main_menu = Menu(screen, menu_buttons_array(screen))
    choose_game_menu = Menu(screen, choose_night_menu_buttons_array(screen))
    choose_game_menu.hide()

    cursor_group = pygame.sprite.Group()
    cursor = pygame.sprite.Sprite(cursor_group)
    cursor.image = pygame.image.load('data/png/arrow.png')

    background = pygame.image.load('data/png/background.png')

    current_night = None
    current_hero = None
    current_bot = None
    figures_sprite_group = pygame.sprite.Group()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if in_game:
            current_night.update()
            figures_sprite_group.update(pygame.key.get_pressed())

        pygame.display.flip()
        screen.fill((0, 0, 0))
        if in_menu or in_choosing_game_menu:
            screen.blit(background, (0, 0))
        if in_menu:
            screen.blit(logo, (WIDTH / 2 - 150, HEIGHT / 2 - 300))
        if in_game:
            screen.blit(current_night.background, (0, 0))
            current_night.draw()
            figures_sprite_group.draw(screen)

        pygame_widgets.update(pygame.event.get())

        if pygame.mouse.get_focused():
            cursor_pos = pygame.mouse.get_pos()

            cursor.rect = cursor.image.get_rect()
            cursor.rect.x, cursor.rect.y = cursor_pos
            cursor_group.draw(screen)

        clock.tick(FPS)