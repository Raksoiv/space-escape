from pygame import K_DOWN, K_LEFT, K_RIGHT, K_UP, draw
from pygame.key import get_pressed
from pygame.math import Vector2
from pygame.rect import Rect

from space_escape.core.game_objects import SpriteCollideObject


class Player(SpriteCollideObject):
    '''
    This class represents the player's ship
    '''
    speed = Vector2()
    max_speed = 500
    acceleration = 75
    friction = 150
    box_collider_scale = .75
    lives = 3

    def set_start_position(self):
        self.set_pos(
            0,
            (self.screen_h - self.rect.height) / 2
        )

    def reset_life(self):
        self.lives = 3

    def damage(self):
        self.lives -= 1

    def heal(self):
        self.lives += 1

    def start(self):
        self.start_box_collider()

    def update(self, delta):
        pressed_keys = get_pressed()

        # Direction
        direction_vector = Vector2()
        direction_vector.y = pressed_keys[K_DOWN] - pressed_keys[K_UP]
        direction_vector.x = pressed_keys[K_RIGHT] - pressed_keys[K_LEFT]
        if direction_vector.length() != 0:
            direction_vector.normalize_ip()

        # Speed
        if direction_vector.magnitude() > 0:
            if self.speed.magnitude() < self.max_speed * delta/1000.0:
                self.speed += direction_vector * self.acceleration \
                    * delta/1000.0
            else:
                self.speed = direction_vector * self.max_speed * delta/1000.0
        elif self.speed.magnitude() > 1:
            self.speed += self.speed.normalize() * -self.friction \
                * delta/1000.0
        else:
            self.speed = self.speed * 0

        # Movement
        self.rect.move_ip(*self.speed)

        # Keep player on the screen
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(self.screen_w, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(self.screen_h, self.rect.bottom)

        # Update collider
        self.update_box_collider()
