from pygame import QUIT, display, event
from pygame.sprite import Group, LayeredUpdates
from pygame.time import Clock

from space_escape.objects import Cursor, TextObject
from space_escape.utils import colors
from space_escape.utils.path import get_asset_path

from .background import Background


class Menu:
    def __init__(self, screen):
        # Base configuration
        self.screen = screen
        info = display.Info()
        self.screen_h, self.screen_w = info.current_h, info.current_w
        self.running = True
        self.clock = Clock()

        # Groups creation
        self.render_sprites = LayeredUpdates()
        self.update_sprites = Group()
        self.event_sprites = Group()

        # GameObject creation
        font_file = get_asset_path('fonts/BalooChettan2-SemiBold.ttf')
        self.title_text = TextObject(
            'Space Escape',
            font_file,
            antialias=True,
            font_color=colors.white,
            font_size=62,
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
        self.exit_text = TextObject(
            'Exit',
            font_file,
            antialias=True,
            font_color=colors.white,
            font_size=32,
        )
        self.background = Background()
        self.cursor = Cursor()

        # Assign groups
        self.render_sprites.add(
            self.background,
            self.title_text,
            self.start_text,
            self.score_text,
            self.exit_text,
            self.cursor,
        )
        self.update_sprites.add(
            self.cursor,
        )
        self.event_sprites.add(
            self.cursor,
        )

        # Start positions of the objects
        self.title_text.rect.move_ip(
            (self.screen_w - self.title_text.rect.width) / 2,
            int(self.screen_h * .2)
        )
        self.start_text.rect.move_ip(
            (self.screen_w - self.start_text.rect.width) / 2,
            int(self.screen_h * .4)
        )
        self.score_text.rect.move_ip(
            (self.screen_w - self.score_text.rect.width) / 2,
            int(self.screen_h * .5)
        )
        self.exit_text.rect.move_ip(
            (self.screen_w - self.exit_text.rect.width) / 2,
            int(self.screen_h * .6)
        )

        # Cursor positions
        self.cursor.add_position(
            self.score_text.rect.left - self.cursor.rect.width,
            self.start_text.rect.centery - int(self.cursor.rect.height / 2),
        )

        self.cursor.add_position(
            self.score_text.rect.left - self.cursor.rect.width,
            self.score_text.rect.centery - int(self.cursor.rect.height / 2),
        )

        self.cursor.add_position(
            self.score_text.rect.left - self.cursor.rect.width,
            self.exit_text.rect.centery - int(self.cursor.rect.height / 2),
        )

    def start(self):
        # Start cursor data
        self.cursor.start()

    def main_loop(self):
        self.start()
        while self.running:
            # Event catch
            for e in event.get():
                for s in self.event_sprites.sprites():
                    s.add_event(e)
                if e.type == QUIT:
                    self.running = False

            # Update fase
            self.update_sprites.update()

            # Render fase
            self.screen.fill((0, 0, 0))
            self.render_sprites.draw(self.screen)

            display.flip()

            if self.cursor.selected == 0:
                return 2
            elif self.cursor.selected == 2:
                return 0

            # Ensure frame rate
            self.clock.tick(60)

        return 0
