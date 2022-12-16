import pygame
from settings import *
from pygame_widgets.button import Button
import pygame_widgets


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


def open_choosing_night_menu():
    global in_menu, in_choosing_game_menu, in_game, choose_game_menu, main_menu
    in_menu, in_choosing_game_menu, in_game = False, True, False
    choose_game_menu.show()
    main_menu.hide()


def menu_buttons_array(screen):
    start_game_button = Button(screen, WIDTH / 2 - 250, HEIGHT / 2 - 200, 500, 100, 0, text='Начать игру',
        textColour=(255, 255, 255), fontSize=50, hoverColour=(200, 50, 200), onClick=open_choosing_night_menu, colour=(0, 0, 0), radius=50)
    godmode_button = Button(screen, WIDTH / 2 - 250, HEIGHT / 2 - 50, 500, 100, 0, text='Godmode',
        textColour=(255, 255, 255), fontSize=50, hoverColour=(255, 100, 100), onClick=reedit_godmode, colour=(0, 0, 0), radius=50)
    return [start_game_button, godmode_button]


def reedit_godmode():
    global GODMODE
    GODMODE = not GODMODE

    print(main_menu.buttons[1].text)
    if GODMODE:
        main_menu.buttons[1].setHoverColour((20, 200, 20))
    else:
        main_menu.buttons[1].setHoverColour((255, 100, 100))


def choose_night_menu_buttons_array(screen):
    start_x, y = 100, 350
    array = []
    for i in range(5):
        button = Button(screen, start_x + i * 275, y, 200, 300, 0, text=f'Ночь {i + 1}',
            textColour=(255, 255, 255), fontSize=50, hoverColour=(200, 50, 200), colour=(0, 0, 0), radius=25)
        array.append(button)
    button = Button(screen, WIDTH / 2 - 250, HEIGHT / 2 - 200, 500, 100, 0, text='Назад в главное меню', onClick=open_main_menu,
        textColour=(255, 255, 255), fontSize=50, hoverColour=(200, 50, 200), colour=(0, 0, 0), radius=50)
    array.append(button)
    return array


def open_main_menu():
    global in_menu, in_choosing_game_menu, in_game, choose_game_menu, main_menu
    in_menu, in_choosing_game_menu, in_game = True, False, False
    choose_game_menu.hide()
    main_menu.show()



if __name__ == '__main__':
    print(SCREEN_SIZE)
    pygame.init()
    pygame.mouse.set_visible(False)

    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption('Игра')
    
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
    cursor.image.convert_alpha()
    cursor.image = pygame.transform.scale(cursor.image, (50, 75))

    background = pygame.image.load('data/png/background.png')

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
        screen.fill((0, 0, 0))
        if in_menu or in_choosing_game_menu:
            screen.blit(background, (0, 0))

        pygame_widgets.update(pygame.event.get())

        if pygame.mouse.get_focused():
            cursor_pos = pygame.mouse.get_pos()

            cursor.rect = cursor.image.get_rect()
            cursor.rect.x, cursor.rect.y = cursor_pos
            cursor_group.draw(screen)

        clock.tick(FPS)