import time
from objects.text_objects import TextObject
from pygame.display import Info


class Score(TextObject):
    def start(self):
        self.start_time = time.time()

    def get_score(self):
        return int(time.time() - self.start_time)

    def update(self):
        score = int(time.time() - self.start_time)
        self.image = self.font.render(
            f'Score: {score}',
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