from game import SpaceEscape


def main():
    game = SpaceEscape(800, 600)

    while game.running:
        game.main_loop()

    game.quit()


if __name__ == '__main__':
    main()
