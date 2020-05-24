from pygame.font import Font
from pygame.sprite import Sprite

from space_escape.utils import colors


class TextObject(Sprite):
    def __init__(
        self, text, font_filename, font_color=colors.black,
        font_size=16, antialias=False,
    ):
        super().__init__()
        self.font_color = font_color
        self.font_size = font_size
        self.antialias = antialias
        self.font = Font(font_filename, self.font_size)
        self.image = self.font.render(
            text,
            self.antialias,
            self.font_color
        )
        self.rect = self.image.get_rect()
