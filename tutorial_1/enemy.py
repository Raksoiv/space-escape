import random

import pygame


class DifficultyLevel:
    EASY = 1
    MEDIUM = 2
    HARD = 3


class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen_limits, difficult=1):
        # Super init
        super().__init__()

        # Set the screen size
        self.screen_width = screen_limits[0]
        self.screen_height = screen_limits[1]

        images = [
            pygame.image.load(image)
            for image in [
                'assets/meteorBrown_small1.png',
                'assets/meteorBrown_small2.png',
                'assets/meteorBrown_tiny1.png',
                'assets/meteorBrown_tiny2.png',
            ]
        ]
        images = [
            pygame.transform.scale(
                image,
                (
                    int(image.get_rect().width * 1),
                    int(image.get_rect().height * 1)
                )
            ) for image in images
        ]

        self.surf = images[random.randint(0, 3)].convert()

        # Set the enemy starting point
        self.rect = self.surf.get_rect(
            center=(
                random.randint(
                    self.screen_width + 20, self.screen_width + 100),
                random.randint(0, self.screen_height)
            )
        )

        if difficult == DifficultyLevel.EASY:
            self.speed = random.randint(5, 10)
        elif difficult == DifficultyLevel.MEDIUM:
            self.speed = random.randint(5, 20)
        else:
            self.speed = random.randint(5, 25)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
