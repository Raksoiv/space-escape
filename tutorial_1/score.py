import time

import pygame


class Score:
    def __init__(self):
        # Create the font
        self.font = pygame.font.SysFont("Sans", 36)

        # Initialize the score in 0
        self.time = time.time()

        # Intialize the surface
        self.surf = self.font.render(
            f'Score: 0', False, (255, 255, 255))
        self.rect = self.surf.get_rect()

    def update(self):
        score = int(time.time() - self.time)
        self.surf = self.font.render(
            f'Score: {score}', False, (255, 255, 255))
