from pygame.surface import Surface

from space_escape.core.game_objects import GameObject, TextObject, Cursor
from space_escape.utils import colors


class MainMenu(GameObject):
    def get_objects(self) -> tuple:
        return (
            self.title_text,
            self.start_text,
            self.score_text,
            self.credits,
            self.exit_text,
        )

    def set_cursor_positions(self, cursor: Cursor):
        # Cursor positions
        cursor.add_position(
            self.score_text.rect.left - cursor.rect.width,
            self.start_text.rect.centery - int(cursor.rect.height / 2),
        )

        cursor.add_position(
            self.score_text.rect.left - cursor.rect.width,
            self.score_text.rect.centery - int(cursor.rect.height / 2),
        )

        cursor.add_position(
            self.score_text.rect.left - cursor.rect.width,
            self.credits.rect.centery - int(cursor.rect.height / 2),
        )

        cursor.add_position(
            self.score_text.rect.left - cursor.rect.width,
            self.exit_text.rect.centery - int(cursor.rect.height / 2),
        )

    def start(self):
        # Set the game object to render only once on every start
        self.dirty = 1
        # Text creation
        font_file = 'BalooChettan2-SemiBold.ttf'
        self.title_text = TextObject(
            'Space Escape',
            font_file,
            antialias=True,
            font_color=colors.white,
            font_size=64,
        )
        self.start_text = TextObject(
            'Start',
            font_file,
            antialias=True,
            font_color=colors.white,
            font_size=32,
        )
        self.score_text = TextObject(
            'High Scores',
            font_file,
            antialias=True,
            font_color=colors.white,
            font_size=32,
        )
        self.credits = TextObject(
            'Credits',
            font_file,
            antialias=True,
            font_color=colors.white,
            font_size=32,
        )
        self.exit_text = TextObject(
            'Exit',
            font_file,
            antialias=True,
            font_color=colors.white,
            font_size=32,
        )

        # Text position
        self.title_text.set_pos(
            (self.screen_w - self.title_text.rect.width) / 2,
            int(self.screen_h * .1)
        )
        self.start_text.set_pos(
            (self.screen_w - self.start_text.rect.width) / 2,
            int(self.screen_h * .4)
        )
        self.score_text.set_pos(
            (self.screen_w - self.score_text.rect.width) / 2,
            int(self.screen_h * .5)
        )
        self.credits.set_pos(
            (self.screen_w - self.credits.rect.width) / 2,
            int(self.screen_h * .6)
        )
        self.exit_text.set_pos(
            (self.screen_w - self.exit_text.rect.width) / 2,
            int(self.screen_h * .7)
        )
