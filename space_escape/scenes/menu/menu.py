from pygame.mixer import Sound

from space_escape.core.game_objects import Background, Cursor
from space_escape.core.scene import Scene
from space_escape.core.path import get_asset_path

from .main_menu import MainMenu
from .highscore import HighScore


class Menu(Scene):
    def clear(self):
        self.background_sound.fadeout(100)
        self.cursor.clear()

    def start(self):
        # Scene configuration
        self.selected = 'main_menu'

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
        self.cursor = Cursor('playerLife1_blue.png', 'sfx_zap.ogg')

        # Game object start
        self.background.start()
        self.main_menu.start()
        self.cursor.start()
        self.highscore.start()

        # Add cursor positions
        self.main_menu.set_cursor_positions(self.cursor)

        # Add objects to groups
        self.render_group.add(
            self.background,
            self.main_menu,
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
            if self.selected == 'main_menu':
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
                    self.selected = 'highscore'
                elif self.cursor.selected == 2:
                    self.exit(0)
            elif self.selected == 'highscore':
                if self.cursor.selected == 0:
                    self.cursor.clear()
                    self.main_menu.set_cursor_positions(self.cursor)
                    self.render_group.empty()
                    self.render_group.add(
                        self.background,
                        self.main_menu,
                        self.cursor,
                    )
                    self.selected = 'main_menu'
