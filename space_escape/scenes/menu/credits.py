from pygame.surface import Surface

from space_escape.core.game_objects import Cursor, GameObject, TextObject
from space_escape.utils import colors


class Credits(GameObject):
    font_file = 'BalooChettan2-SemiBold.ttf'

    def set_cursor_positions(self, cursor: Cursor):
        # Cursor positions
        cursor.add_position(
            self.back.rect.left - cursor.rect.width,
            self.back.rect.centery - int(cursor.rect.height / 2),
        )

    def start(self):
        # Text creation
        self.title_text = TextObject(
            'Credits',
            self.font_file,
            antialias=True,
            font_color=colors.white,
            font_size=64,
        )

        font_size = 24
        # Game Developer
        self.gd_title = TextObject(
            'Game Developer:',
            self.font_file,
            antialias=True,
            font_color=colors.white,
            font_size=font_size,
        )
        self.gd_content = TextObject(
            'Oscar Rencoret github.com/Raksoiv',
            self.font_file,
            antialias=True,
            font_color=colors.white,
            font_size=font_size,
        )

        # Assets
        self.a_title = TextObject(
            'Art Pack:',
            self.font_file,
            antialias=True,
            font_color=colors.white,
            font_size=font_size,
        )
        self.a_content = TextObject(
            '« Space Shooter Redux » from Kenney.nl',
            self.font_file,
            antialias=True,
            font_color=colors.white,
            font_size=font_size,
        )

        # Music
        self.s_title = TextObject(
            'Music:',
            self.font_file,
            antialias=True,
            font_color=colors.white,
            font_size=font_size,
        )
        self.s1_content = TextObject(
            '« Deep Blue » from Bensound.com',
            self.font_file,
            antialias=True,
            font_color=colors.white,
            font_size=font_size,
        )
        self.s2_content = TextObject(
            '« Extreme Action » from Bensound.com',
            self.font_file,
            antialias=True,
            font_color=colors.white,
            font_size=font_size,
        )

        # Back
        self.back = TextObject(
            'Back',
            self.font_file,
            antialias=True,
            font_color=colors.white,
            font_size=font_size,
        )

        # Set the positions of the text
        self.title_text.set_pos(
            (self.screen_w - self.title_text.rect.width) / 2,
            int(self.screen_h * .1)
        )

        title_x = int(self.screen_w * .4) - 10
        content_x = int(self.screen_w * .4) + 10

        gd_top = self.screen_h * .3
        self.gd_title.set_pos(0, gd_top)
        # self.gd_title.rect.left = 100
        self.gd_title.rect.right = title_x
        self.gd_content.set_pos(0, gd_top)
        # self.gd_content.rect.right = self.screen_w - 100
        self.gd_content.rect.left = content_x

        a_top = gd_top + 2 * font_size
        self.a_title.set_pos(0, a_top)
        # self.a_title.rect.left = 100
        self.a_title.rect.right = title_x
        self.a_content.set_pos(0, a_top)
        # self.a_content.rect.right = self.screen_w - 100
        self.a_content.rect.left = content_x

        s1_top = a_top + 2 * font_size
        s2_top = s1_top + font_size
        self.s_title.set_pos(0, s1_top)
        # self.s_title.rect.left = 100
        self.s_title.rect.right = title_x
        self.s1_content.set_pos(0, s1_top)
        # self.s1_content.rect.right = self.screen_w - 100
        self.s1_content.rect.left = content_x
        self.s2_content.set_pos(0, s2_top)
        # self.s2_content.rect.right = self.screen_w - 100
        self.s2_content.rect.left = content_x

        self.back.set_pos(
            (self.screen_w - self.back.rect.width) / 2,
            self.screen_h * .75
        )

        # Set the base image
        self.image = Surface((self.screen_w, self.screen_h))
        self.image.set_colorkey((0, 0, 0))
        self.image.blits((
            self.title_text.get_draw(),
            self.gd_title.get_draw(),
            self.gd_content.get_draw(),
            self.a_title.get_draw(),
            self.a_content.get_draw(),
            self.s_title.get_draw(),
            self.s1_content.get_draw(),
            self.s2_content.get_draw(),
            self.back.get_draw(),
        ))

        self.rect = self.image.get_rect()

        # Update draw
        self.dirty = 1
