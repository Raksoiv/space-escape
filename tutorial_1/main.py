import pygame
from scenes import Menu, Game


def main(width=800, height=600):
    pygame.init()
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

    # game = Game(screen)
    # game.main_loop()

    # menu = Menu(screen)
    # menu.main_loop()


if __name__ == '__main__':
    main()
