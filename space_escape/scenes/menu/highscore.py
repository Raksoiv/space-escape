import json

from pygame.surface import Surface

from space_escape.core.game_objects import Cursor, GameObject, TextObject
from space_escape.core.path import HIGHSCORES_BASEPATH
from space_escape.utils import colors


class HighScore(GameObject):
    def get_scores(self):
        with open(HIGHSCORES_BASEPATH, 'r') as scores_json:
            json_scores = json.loads(scores_json.read())
        return json_scores

    def set_cursor_positions(self, cursor: Cursor):
        # Cursor positions
        cursor.add_position(
            self.back.rect.left - cursor.rect.width,
            self.back.rect.centery - int(cursor.rect.height / 2),
        )

    def update_scores(self):
        # Create TExt objects for the scores
        font_file = 'BalooChettan2-SemiBold.ttf'
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

        # Set position of the scores
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

        # Draw base image
        self.image = Surface((self.screen_w, self.screen_h))
        self.image.blits((
            *[s.get_draw() for s in self.score_pos],
            *[s.get_draw() for s in self.scores],
            self.back.get_draw(),
            self.title_text.get_draw(),
        ))

        # Base rect
        self.rect = self.image.get_rect()

    def start(self):
        # Text creation
        font_file = 'BalooChettan2-SemiBold.ttf'
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

        # Text position
        self.title_text.set_pos(
            (self.screen_w - self.title_text.rect.width) / 2,
            int(self.screen_h * .1)
        )

        self.back.set_pos(
            (self.screen_w - self.back.rect.width) / 2,
            self.screen_h * .75
        )
