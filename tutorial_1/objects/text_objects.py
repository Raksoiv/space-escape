from pygame.font import Font
from pygame.sprite import Sprite

from conf import colors


class TextObject(Sprite):
    def __init__(
        self, text, font_filename, font_color=colors.black,
        font_size=16, antialias=False,
    ):
        super().__init__()
        self.text = text
        self.font = Font(font_filename, font_size)
        self.image = self.font.render(self.text, antialias, font_color)
        self.rect = self.image.get_rect()
