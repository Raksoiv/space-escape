import time
import json

from pygame.display import Info

from space_escape.objects.text_objects import TextObject
from space_escape.core.path import HIGHSCORES_BASEPATH


class Score(TextObject):
    def start(self):
        self.start_time = time.time()
        self.score = 0

    def get_score(self):
        return self.score

    def update(self):
        self.score = int(time.time() - self.start_time)
        self.image = self.font.render(
            f'Score: {self.score}',
            self.antialias,
            self.font_color,
        )

    def game_over(self):
        info = Info()
        self.rect = self.image.get_rect()
        self.rect.move_ip((
            (info.current_w / 2) - (self.rect.width / 2),
            info.current_h * .3
        ))

    def save_score(self):
        with open(HIGHSCORES_BASEPATH, 'r') as scores_json:
            scores = json.loads(scores_json.read())
        if type(scores) is list:
            new_scores = []
            insert_score = False
            i = 0
            while i < min(len(scores), 5):
                if not insert_score and self.get_score() > scores[i]:
                    new_scores.append(self.get_score())
                    insert_score = True
                else:
                    new_scores.append(scores[i])
                    i += 1
            if insert_score is False and i < 5:
                new_scores.append(self.get_score())
        else:
            new_scores = scores
        with open(HIGHSCORES_BASEPATH, 'w') as scores_json:
            scores_json.write(json.dumps(new_scores))
