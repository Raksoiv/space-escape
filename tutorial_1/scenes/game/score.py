import time
from objects.text_objects import TextObject


class Score(TextObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initialize the score in 0
        self.start = time.time()

    def update(self):
        score = int(time.time() - self.start)
        self.image = self.font.render(
            f'Score: {score}', self.antialias, self.font_color)
