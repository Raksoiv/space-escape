import pygame
from pygame.image import load
from pygame.key import get_pressed
from pygame.locals import (K_DOWN, K_LEFT, K_RIGHT, K_UP, KEYDOWN, KEYUP,
                           RLEACCEL)
from pygame.sprite import Sprite
from pygame.transform import rotate, scale


class Player(Sprite):
    def __init__(self, screen_limits):
        super().__init__()

        # Set the screen size
        self.screen_width = screen_limits[0]
        self.screen_height = screen_limits[1]

        # Added the image to the Player
        image = load('assets/images/playerShip1_blue.png')
        image = scale(
            image,
            (
                int(image.get_rect().width * .5),
                int(image.get_rect().height * .5)
            )
        )
        image = rotate(image, -90)
        self.image = image.convert()
        self.image.set_colorkey((0, 0, 0), RLEACCEL)

        # Set the player rect
        self.rect = self.image.get_rect()

    def add_event(self, event):
        self.events.append(event)

    def update(self):
        pressed_keys = get_pressed()
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
