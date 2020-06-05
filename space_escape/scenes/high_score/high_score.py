import json

from pygame import QUIT, event
from pygame.display import Info, flip
from pygame.sprite import Group, LayeredUpdates
from pygame.time import Clock

from space_escape.objects import Background, Cursor, TextObject
from space_escape.utils import colors
from space_escape.utils.path import HIGHSCORES_BASEPATH, get_asset_path


class HighScore:
    def __init__(self, screen):
        # Base configuration
        self.screen = screen
        info = Info()
        self.screen_h, self.screen_w = info.current_h, info.current_w
        self.running = True
        self.clock = Clock()

        # Groups creation
        self.event_sprites = Group()
        self.render_sprites = LayeredUpdates()
        self.update_sprites = Group()

        # GameObject creation
        font_file = get_asset_path('fonts/BalooChettan2-SemiBold.ttf')
        self.title_text = TextObject(
            'High Scores',
            font_file,
            antialias=True,
            font_color=colors.white,
            font_size=64,
        )
        self.back = TextObject(
            'Back',
            font_file,
            antialias=True,
            font_color=colors.white,
            font_size=32,
        )
        self.background = Background('images/purple.png')
        self.cursor = Cursor()

        self.title_text.rect.move_ip(
            (self.screen_w - self.title_text.rect.width) / 2,
            int(self.screen_h * .1)
        )

        self.back.rect.move_ip(
            (self.screen_w - self.back.rect.width) / 2,
            self.screen_h * .75
        )

        self.cursor.add_position(
            self.back.rect.left - self.cursor.rect.width,
            self.back.rect.centery - int(self.cursor.rect.height / 2),
        )

    def start(self):
        font_file = get_asset_path('fonts/BalooChettan2-SemiBold.ttf')
        self.scores = []
        self.score_pos = []
        for i, score in enumerate(self.get_scores()):
            self.scores.append(
                TextObject(
                    str(score),
                    font_file,
                    antialias=True,
                    font_color=colors.white,
                    font_size=32,
                ),
            )
            self.score_pos.append(
                TextObject(
                    f'{str(i + 1)}.',
                    font_file,
                    antialias=True,
                    font_color=colors.white,
                    font_size=32,
                )
            )

        # Assign groups
        self.event_sprites.add(self.cursor)
        self.render_sprites.add(
            self.background,
            *self.score_pos,
            *self.scores,
            self.back,
            self.cursor,
            self.title_text,
        )
        self.update_sprites.add(self.cursor)

        max_width = 0
        separation = 150
        for score in self.scores:
            if score.rect.width > max_width:
                max_width = score.rect.width
        for i, score in enumerate(self.scores):
            score.rect.move_ip(
                (
                    (self.screen_w / 2) + separation
                    + max_width - score.rect.width
                ),
                self.screen_h * .3 + self.screen_h * .05 * i,
            )
            self.score_pos[i].rect.move_ip(
                (
                    (self.screen_w / 2) - separation
                    - self.score_pos[i].rect.width
                ),
                score.rect.top,
            )

        self.cursor.start()

    def clean(self):
        self.event_sprites.empty()
        self.render_sprites.empty()
        self.update_sprites.empty()

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

            if self.cursor.selected == 0:
                self.clean()
                return 1

            flip()

            # Ensure frame rate
            self.clock.tick(60)

    def get_scores(self):
        with open(HIGHSCORES_BASEPATH, 'r') as scores_json:
            json_scores = json.loads(scores_json.read())
        return json_scores
