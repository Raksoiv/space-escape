from pygame import QUIT, USEREVENT, display, event
from pygame.display import Info
from pygame.sprite import Group, LayeredUpdates
from pygame.time import Clock, set_timer

from utils import colors

from .enemy import Enemy
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

        # Groups creation
        self.render_sprites = LayeredUpdates()
        self.update_sprites = Group()
        self.event_sprites = Group()

        # GameObject creation
        self.player = Player(screen_limits=(self.screen_w, self.screen_h))

        font_file = 'assets/fonts/BalooChettan2-SemiBold.ttf'
        self.score = Score(
            'Score: 0',
            font_file,
            antialias=True,
            font_color=colors.white,
            font_size=36,
        )

        # Assign groups
        self.render_sprites.add(self.player)
        self.update_sprites.add(self.player)

    def add_enemy(self):
        enemy = Enemy(screen_limits=(self.screen_w, self.screen_h))
        self.render_sprites.add(enemy)
        self.update_sprites.add(enemy)

    def start(self):
        self.add_enemy_event = USEREVENT + 1
        set_timer(self.add_enemy_event, 300)

    def main_loop(self):
        exit = None
        self.start()
        while self.running:
            # Event catch
            for e in event.get():
                for s in self.event_sprites.sprites():
                    s.add_event(e)
                if e.type == QUIT:
                    self.running = False
                elif e.type == self.add_enemy_event:
                    self.add_enemy()

            # Update fase
            self.update_sprites.update()

            # Render fase
            self.screen.fill((0, 0, 0))
            self.render_sprites.draw(self.screen)

            display.flip()

            # Ensure frame rate
            self.clock.tick(60)

        return exit
