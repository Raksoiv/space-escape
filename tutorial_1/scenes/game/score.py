import time
from objects.text_objects import TextObject


class Score(TextObject):
    def start(self):
        self.start_time = time.time()

    def update(self):
        score = int(time.time() - self.start_time)
        self.image = self.font.render(
            f'Score: {score}', self.antialias, self.font_color)
