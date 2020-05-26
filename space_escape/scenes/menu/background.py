from pygame.display import Info
from pygame.image import load
from pygame.sprite import Sprite
from pygame.surface import Surface

from space_escape.utils.path import get_asset_path


class Background(Sprite):
    def __init__(self):
        super().__init__()

        info = Info()
        self.image = Surface((info.current_w, info.current_h))
        raw_image = load(get_asset_path('images/purple.png')).convert()
        for j in range(3):
            for i in range(4):
                self.image.blit(raw_image, (
                    raw_image.get_width() * i,
                    raw_image.get_height() * j
                ))
        self.rect = self.image.get_rect()
