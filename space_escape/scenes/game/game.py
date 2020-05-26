from pygame import QUIT, display, event
from pygame.display import Info
from pygame.sprite import Group, LayeredUpdates, spritecollideany
from pygame.time import Clock, set_timer

from space_escape.objects import Cursor
from space_escape.utils import colors, events
from space_escape.utils.path import get_asset_path

from .background import Background
from .enemy import Enemy
from .game_over import GameOver
from .player import Player
from .score import Score


class Game:
    def __init__(self, screen):
        # Base configuration
        self.screen = screen
        info = Info()
        self.screen_h, self.screen_w = info.current_h, info.current_w
        self.running = True
        self.clock = Clock()

        self.phase = 0

        # Groups creation
        self.render_sprites = LayeredUpdates()
        self.update_sprites = Group()
        self.event_sprites = Group()
        self.enemies = Group()

        # GameObject creation
        self.player = Player(screen_limits=(self.screen_w, self.screen_h))
        self.background = Background()
        self.cursor = Cursor()

        font_file = get_asset_path('fonts/BalooChettan2-SemiBold.ttf')
        self.score = Score(
            'Score: 0',
            font_file,
            antialias=True,
            font_color=colors.white,
            font_size=36,
        )

        self.game_over = GameOver(self.score, self.cursor)

    def add_enemy(self):
        enemy = Enemy((self.screen_w, self.screen_h), self.score.get_score())
        if enemy.image:
            self.render_sprites.add(enemy)
            self.update_sprites.add(enemy)
            self.enemies.add(enemy)

    def start(self):
        self.player.start()
        self.score.start()
        self.score.rect = self.score.image.get_rect()
        self.cursor.start()
        self.phase = 0

        self.render_sprites.add(self.background)
        self.render_sprites.add(self.player)
        self.update_sprites.add(self.player)
        self.render_sprites.add(self.score)
        self.update_sprites.add(self.score)

    def restart(self):
        self.clean()
        self.start()

    def clean(self):
        set_timer(events.ADD_ENEMY, 0)
        self.game_over.kill()
        self.cursor.kill()
        self.render_sprites.empty()
        self.update_sprites.empty()
        self.event_sprites.empty()
        self.enemies.empty()

    def player_death(self):
        self.player.kill()
        self.score.game_over()
        self.score.remove(self.update_sprites)
        self.render_sprites.add(self.game_over, self.cursor)
        self.update_sprites.add(self.cursor)
        self.event_sprites.add(self.cursor)
        # self.clean()

    def main_loop(self):
        self.start()
        while self.running:
            # Event catch
            for e in event.get():
                for s in self.event_sprites.sprites():
                    s.add_event(e)
                if e.type == QUIT:
                    self.running = False
                elif e.type == events.ADD_ENEMY:
                    self.add_enemy()

            # Update fase
            if self.score.get_score() < 40:
                if self.phase < 1:
                    self.phase = 1
                    set_timer(events.ADD_ENEMY, 300)
                    print(self.phase)
            elif self.score.get_score() < 60:
                if self.phase < 2:
                    self.phase = 2
                    set_timer(events.ADD_ENEMY, 200)
                    print(self.phase)
            elif self.score.get_score() < 100:
                if self.phase < 3:
                    self.phase = 3
                    set_timer(events.ADD_ENEMY, 250)
                    print(self.phase)
            elif self.score.get_score() < 120:
                if self.phase < 4:
                    self.phase = 4
                    set_timer(events.ADD_ENEMY, 150)
                    print(self.phase)
            elif self.score.get_score() < 160:
                if self.phase < 5:
                    self.phase = 5
                    set_timer(events.ADD_ENEMY, 200)
                    print(self.phase)
            elif self.score.get_score() < 180:
                if self.phase < 6:
                    self.phase = 6
                    set_timer(events.ADD_ENEMY, 100)
                    print(self.phase)
            elif self.score.get_score() < 220:
                if self.phase < 7:
                    self.phase = 7
                    set_timer(events.ADD_ENEMY, 150)
                    print(self.phase)
            elif self.score.get_score() < 240:
                if self.phase < 8:
                    self.phase = 8
                    set_timer(events.ADD_ENEMY, 50)
                    print(self.phase)
            else:
                if self.phase < 9:
                    self.phase = 9
                    set_timer(events.ADD_ENEMY, 100)
                    print(self.phase)

            self.update_sprites.update()

            if not self.player.alive():
                if self.cursor.selected == 0:
                    self.cursor.selected = None
                    self.restart()
                elif self.cursor.selected == 1:
                    self.cursor.selected = None
                    self.clean()
                    return 1

            # Collision fase
            if (
                self.player.alive() and
                spritecollideany(self.player, self.enemies)
            ):
                self.player_death()

            # Render fase
            self.screen.fill((0, 0, 0))
            self.render_sprites.draw(self.screen)

            display.flip()

            # Ensure frame rate
            self.clock.tick(60)

        return 0
