import pygame
from settings import *
from pygame import mixer_music


if __name__ == '__main__':
    filename = input()
    with open(f'data/txt/{filename}.txt', 'w') as file:
        file.writelines(['0' * 8 for _ in range(ACTIVE_ROWS)])
        pygame.init()

        screen = pygame.display.set_mode((300, 300))
        pygame.display.flip()

        running = True
        clock = pygame.time.Clock()
        keys = (pygame.K_d, pygame.K_w, pygame.K_a, pygame.K_s,
            pygame.K_RIGHT, pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN)
        scene_number = 1

        mixer_music.load(f'data/music/{filename}.wav')
        mixer_music.play()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            if mixer_music.get_busy():
                pressed_keys = pygame.key.get_pressed()
                line = ''
                for key in keys:
                    line += str(int(pressed_keys[key]))
                file.writelines([line])
            clock.tick(FPS)