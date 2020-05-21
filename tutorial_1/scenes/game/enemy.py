import random

import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen_limits):
        # Super init
        super().__init__()

        # Set the screen size
        self.screen_width = screen_limits[0]
        self.screen_height = screen_limits[1]

        images = [
            pygame.image.load(image)
            for image in [
                'assets/images/meteorBrown_small1.png',
                'assets/images/meteorBrown_small2.png',
                'assets/images/meteorBrown_tiny1.png',
                'assets/images/meteorBrown_tiny2.png',
            ]
        ]
        images = [
            pygame.transform.scale(
                image,
                (
                    image.get_rect().width,
                    image.get_rect().height
                )
            ) for image in images
        ]

        self.image = images[random.randint(0, 3)].convert()

        # Set the enemy starting point
        self.rect = self.image.get_rect(center=(
            random.randint(
                self.screen_width + 20,
                self.screen_width + 100
            ),
            random.randint(0, self.screen_height)
        ))

        self.speed = random.randint(5, 10)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
