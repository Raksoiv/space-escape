from pygame.mixer import Sound

from space_escape.core.game_objects import Background, Cursor
from space_escape.core.scene import Scene
from space_escape.core.path import get_asset_path
from space_escape.core.settings import DEBUG

from .main_menu import MainMenu
from .highscore import HighScore
from .credits import Credits


MAINMENU = 'mainmenu'
HIGHSCORE = 'highscore'
CREDITS = 'credits'


class Menu(Scene):
    def clear(self):
        self.background_sound.fadeout(100)
        self.cursor.clear()

    def start(self):
        # Scene configuration
        self.selected = MAINMENU

        # Sound configuration
        self.background_sound = Sound(
            get_asset_path('sounds', 'bensound-menu.ogg')
        )
        self.background_sound.play(loops=-1)
        self.background_sound.set_volume(.25)

        # Game object creation
        self.background = Background('purple.png')
        self.main_menu = MainMenu()
        self.highscore = HighScore()
        self.credits = Credits()
        self.cursor = Cursor('playerLife1_blue.png', 'sfx_zap.ogg')

        # Game object start
        self.background.start()
        self.main_menu.start()
        self.cursor.start()
        self.highscore.start()
        self.credits.start()

        # Add cursor positions
        self.main_menu.set_cursor_positions(self.cursor)

        # Add objects to groups
        self.render_group.add(
            self.background,
            *self.main_menu.get_objects(),
            self.cursor,
        )
        self.update_group.add(
            self.cursor,
        )
        self.event_group.add(
            self.cursor,
        )

    def update(self):
        if self.cursor.selected is not None:
            if self.selected == MAINMENU:
                if self.cursor.selected == 0:
                    self.exit(2)
                elif self.cursor.selected == 1:
                    self.highscore.update_scores()
                    self.cursor.clear()
                    self.highscore.set_cursor_positions(self.cursor)
                    self.render_group.empty()
                    self.render_group.add(
                        self.background,
                        self.highscore,
                        self.cursor,
                    )
                    self.selected = HIGHSCORE
                elif self.cursor.selected == 2:
                    self.cursor.clear()
                    self.credits.set_cursor_positions(self.cursor)
                    self.render_group.empty()
                    self.render_group.add(
                        self.background,
                        self.credits,
                        self.cursor,
                    )
                    self.selected = CREDITS
                elif self.cursor.selected == 3:
                    self.exit(0)
            elif self.selected == HIGHSCORE or self.selected == CREDITS:
                if self.cursor.selected == 0:
                    self.cursor.clear()
                    self.main_menu.set_cursor_positions(self.cursor)
                    self.render_group.empty()
                    self.render_group.add(
                        self.background,
                        *self.main_menu.get_objects(),
                        self.cursor,
                    )
                    self.selected = MAINMENU
