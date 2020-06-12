from pygame import K_DOWN, K_LEFT, K_RIGHT, K_UP
from pygame.key import get_pressed
from pygame.rect import Rect
from pygame import draw
from space_escape.core.game_objects import SpriteCollideObject


class Player(SpriteCollideObject):
    '''
    This class represents the player's ship
    '''
    speed = [0, 0]
    max_speed = 8
    acceleration = 2
    friction = 3
    box_collider_scale = .75

    def start(self):
        self.start_box_collider()

    def update(self):
        pressed_keys = get_pressed()

        # Y movement
        if pressed_keys[K_UP]:
            self.speed[1] = max(
                -self.max_speed,
                self.speed[1] - self.acceleration,
            )
        if pressed_keys[K_DOWN]:
            self.speed[1] = min(
                self.max_speed,
                self.speed[1] + self.acceleration,
            )
        if not pressed_keys[K_UP] and not pressed_keys[K_DOWN]:
            if self.speed[1] < 0:
                self.speed[1] = min(
                    0,
                    self.speed[1] + self.friction,
                )
            if self.speed[1] > 0:
                self.speed[1] = max(
                    0,
                    self.speed[1] - self.friction,
                )

        # X movement
        if pressed_keys[K_LEFT]:
            self.speed[0] = max(
                -self.max_speed,
                self.speed[0] - self.acceleration,
            )
        if pressed_keys[K_RIGHT]:
            self.speed[0] = min(
                self.max_speed,
                self.speed[0] + self.acceleration,
            )
        if not pressed_keys[K_LEFT] and not pressed_keys[K_RIGHT]:
            if self.speed[0] < 0:
                self.speed[0] = min(
                    0,
                    self.speed[0] + self.friction,
                )
            if self.speed[0] > 0:
                self.speed[0] = max(
                    0,
                    self.speed[0] - self.friction,
                )

        # Apply speed
        self.rect.move_ip(*self.speed)

        # Keep player on the screen
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(self.screen_w, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(self.screen_h, self.rect.bottom)

        # Update collider
        self.update_box_collider()
