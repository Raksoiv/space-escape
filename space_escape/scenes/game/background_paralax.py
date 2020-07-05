from pygame.surface import Surface
from pygame.rect import Rect

from space_escape.core.game_objects import SpriteObject


class BackgroundParalax(SpriteObject):
    _frames = 0

    def __init__(self, bg_image: str):
        super().__init__(bg_image)

        raw_image = self.image
        self.image = Surface((self.screen_w * 2, self.screen_h))
        self.rect = self.image.get_rect()

        for j in range(int(self.rect.height / raw_image.get_height()) + 1):
            for i in range(int(self.rect.width / raw_image.get_width()) + 1):
                self.image.blit(
                    raw_image,
                    (
                        raw_image.get_width() * i,
                        raw_image.get_height() * j,
                    )
                )

    def increase_frame_move(self):
        if self.frames_move < 1:
            self.velocity = (self.velocity[0] - 1, 0)
        else:
            self.frames_move -= 1

    def update(self):
        if self.rect.centerx <= abs(self.velocity[0]):
            self.rect.centerx = self.screen_w
        if self._frames >= self.frames_move:
            self.rect.move_ip(self.velocity)
            self._frames = 0
            self.dirty = 1
        else:
            self._frames += 1

    def start(self):
        self._frames = 0
        self.frames_move = 20
        self.velocity = (-1, 0)
