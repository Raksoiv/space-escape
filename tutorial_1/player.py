from pygame import Surface
from pygame.locals import K_DOWN, K_LEFT, K_RIGHT, K_UP
from pygame.sprite import Sprite


class Player(Sprite):
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

        # Set the player rect
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= self.screen_height:
            self.rect.bottom = self.screen_height
