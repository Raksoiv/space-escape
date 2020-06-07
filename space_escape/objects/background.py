from pygame.display import Info
from pygame.image import load
from pygame.sprite import Sprite
from pygame.surface import Surface

from space_escape.core.path import get_asset_path


class Background(Sprite):
    def __init__(self, bg_image):
        super().__init__()

        info = Info()
        self.image = Surface((info.current_w, info.current_h))
        raw_image = load(get_asset_path(bg_image)).convert()
        for j in range(int(info.current_h / raw_image.get_height()) + 1):
            for i in range(int(info.current_w / raw_image.get_width()) + 1):
                self.image.blit(raw_image, (
                    raw_image.get_width() * i,
                    raw_image.get_height() * j
                ))
        self.rect = self.image.get_rect()
