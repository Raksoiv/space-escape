from pygame.display import Info
from pygame.sprite import Sprite
from pygame.surface import Surface

from space_escape.objects import Cursor, TextObject
from space_escape.utils import colors
from space_escape.utils.path import get_asset_path


class GameOver(Sprite):
    def __init__(self, score: Sprite, cursor: Cursor):
        super().__init__()

        info = Info()
        screen_h, screen_w = info.current_h, info.current_w

        self.image = Surface((screen_w, screen_h))
        self.rect = self.image.get_rect()

        font_file = get_asset_path('fonts/BalooChettan2-SemiBold.ttf')

        title = TextObject(
            'GAME OVER',
            font_file,
            antialias=True,
            font_color=colors.white,
            font_size=62,
        )
        title.rect.move_ip((
            self.rect.centerx - (title.rect.width / 2),
            self.rect.height * .2
        ))

        restart = TextObject(
            'Restart',
            font_file,
            antialias=True,
            font_color=colors.white,
            font_size=36,
        )
        restart.rect.move_ip((
            self.rect.centerx - (restart.rect.width / 2),
            self.rect.height * .5
        ))

        exit_text = TextObject(
            'Exit',
            font_file,
            antialias=True,
            font_color=colors.white,
            font_size=36,
        )
        exit_text.rect.move_ip((
            self.rect.centerx - (exit_text.rect.width / 2),
            self.rect.height * .6
        ))

        self.image.blit(title.image, title.rect)
        self.image.blit(restart.image, restart.rect)
        self.image.blit(exit_text.image, exit_text.rect)

        cursor.add_position(
            restart.rect.left - cursor.rect.width,
            restart.rect.centery - (cursor.rect.height / 2),
        )
        cursor.add_position(
            restart.rect.left - cursor.rect.width,
            exit_text.rect.centery - (cursor.rect.height / 2),
        )
