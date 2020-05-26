import pygame
from space_escape.scenes import Menu, Game


def main(width=1024, height=768, fullscreen=False):
    pygame.init()
    if fullscreen:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((width, height))

    game = Game(screen)
    menu = Menu(screen)

    running = True
    r = 1
    while running:
        if r == 1:
            r = menu.main_loop()
        elif r == 2:
            r = game.main_loop()
        else:
            running = False


if __name__ == '__main__':
    main(1024, 768)
