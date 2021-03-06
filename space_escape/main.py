import pygame
from space_escape.scenes import Menu, Game


def main(width=800, height=600, fullscreen=False):
    pygame.init()
    pygame.display.set_caption('Space Escape')
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

    pygame.quit()


if __name__ == '__main__':
    main(1024, 768)
