import random

from pygame import Surface
from pygame.sprite import Sprite


class Enemy(Sprite):
    def __init__(self, screen_limits):
        # Super init
        super().__init__()

        # Set the screen size
        self.screen_width = screen_limits[0]
        self.screen_height = screen_limits[1]

        # Set the plater surface
        self.surf = Surface((75, 25))

        # Set color White
        self.surf.fill((255, 255, 255))

        # Set the enemy starting point
        self.rect = self.surf.get_rect(
            center=(
                random.randint(
                    self.screen_width + 20, self.screen_width + 100),
                random.randint(0, self.screen_height)
            )
        )

        self.speed = random.randint(5, 20)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
