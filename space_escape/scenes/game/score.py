import time

from pygame.display import Info

from space_escape.objects.text_objects import TextObject


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
