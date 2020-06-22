from pygame.surface import Surface
from pygame.rect import Rect

from space_escape.core.game_objects import SpriteObject


class BackgroundParalax(SpriteObject):
    velocity = (-1, 0)
    frames_move = 5
    _frames = 0

    def __init__(self, bg_image, n):
        super().__init__(bg_image)

        raw_image = self.image
        self.image = Surface((self.screen_w + 10, self.screen_h))
        self.n = n

        for j in range(int(self.screen_h / raw_image.get_height()) + 1):
            for i in range(int(self.screen_w / raw_image.get_width()) + 1):
                self.image.blit(
                    raw_image,
                    (
                        raw_image.get_width() * i,
                        raw_image.get_height() * j,
                    )
                )
        self.rect = self.image.get_rect()

    def reset_frame_move(self):
        self.frames_move = 5

    def increase_frame_move(self):
        if self.frames_move == 1:
            velocity = (velocity[0] - 1, 0)
        else:
            self.frames_move -= 1

    def background_pos(self, pos):
        self.rect.right = (self.screen_w * pos) + 2

    def update(self):
        if self.rect.right < 0:
            self.rect.right = self.screen_w * self.n
        if self._frames > self.frames_move:
            self.rect.move_ip(self.velocity)
            self._frames = 0
        else:
            self._frames += 1
