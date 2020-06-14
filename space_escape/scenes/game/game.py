import random

from pygame.mixer import Sound
from pygame.sprite import Group, spritecollideany
from pygame.time import set_timer

from space_escape.core.colliders import box_collide
from space_escape.core.game_objects import Background, Cursor
from space_escape.core.path import get_asset_path
from space_escape.core.scene import Scene
from space_escape.utils import events

from .enemy import Enemy
from .game_ui import GameUI
from .player import Player

BACKGROUND_LAYER = 0
ENEMY_LAYER = 1
PLAYER_LAYER = 2
UI_LAYER = 3


class Game(Scene):
    '''
    This class represents the main game scene where the player will
    face multiples asteroids and will attempt to stay alive
    '''
    #
    # Base Sprites
    #
    tiny_meteors = (
        'meteorBrown_tiny1.png',
        'meteorBrown_tiny2.png',
        'meteorGrey_tiny1.png',
        'meteorGrey_tiny2.png',
    )
    small_meteors = (
        'meteorBrown_small1.png',
        'meteorBrown_small2.png',
        'meteorGrey_small1.png',
        'meteorGrey_small2.png',
    )
    med_meteors = (
        'meteorBrown_med1.png',
        'meteorBrown_med2.png',
        'meteorGrey_med1.png',
        'meteorGrey_med2.png',
    )
    big_meteors = (
        'meteorBrown_big1.png',
        'meteorBrown_big2.png',
        'meteorBrown_big3.png',
        'meteorBrown_big4.png',
        'meteorGrey_big1.png',
        'meteorGrey_big2.png',
        'meteorGrey_big3.png',
        'meteorGrey_big4.png',
    )

    #
    # Difficulty System
    #
    phase = 0

    def update_phase(self):
        '''
        This method update the phase of the game base on the score of
        the player
        '''
        score = self.ui.get_score()
        if score < 40:
            if self.phase < 1:
                self.phase = 1
                set_timer(events.ADD_ENEMY, 300)
        elif score < 60:
            if self.phase < 2:
                self.phase = 2
                set_timer(events.ADD_ENEMY, 200)
        elif score < 100:
            if self.phase < 3:
                self.phase = 3
                set_timer(events.ADD_ENEMY, 250)
        elif score < 120:
            if self.phase < 4:
                self.phase = 4
                set_timer(events.ADD_ENEMY, 150)
        elif score < 160:
            if self.phase < 5:
                self.phase = 5
                set_timer(events.ADD_ENEMY, 200)
        elif score < 180:
            if self.phase < 6:
                self.phase = 6
                set_timer(events.ADD_ENEMY, 100)
        elif score < 220:
            if self.phase < 7:
                self.phase = 7
                set_timer(events.ADD_ENEMY, 150)
        elif score < 240:
            if self.phase < 8:
                self.phase = 8
                set_timer(events.ADD_ENEMY, 50)
        else:
            if self.phase < 9:
                self.phase = 9
                set_timer(events.ADD_ENEMY, 100)

    def select_enemy(self):
        '''
        This method set the probabilities of a certain sprite to be choosen
        as enemy based on the phase of the game, at higher phases unlock
        more sprites and more velocity
        '''
        if self.phase < 3:
            # p_tiny = 100% - 50%
            p_tiny = 1 - self.ui.get_score() * .0083
            v_tiny = random.randint(5, 5 + int(self.ui.get_score() * 0.09))
            # p_small = 0% - 50%
            p_small = 1
            v_small = random.randint(5, 5 + int(self.ui.get_score() * 0.09))
        elif self.phase < 4:
            n_score = self.ui.get_score() - 60
            # p_tiny = 50% - 30%
            p_tiny = .5 - n_score * .0033
            v_tiny = random.randint(5, 10 + int(n_score * .09))
            # p_small = 50% - 60%
            p_small = 1 - n_score * .0016
            v_small = random.randint(5, 10 + int(n_score * .09))
            # p_med = 0% - 10%
            p_med = 1
            v_med = random.randint(3, 5 + int(n_score * .09))
        elif self.phase < 6:
            n_score = self.ui.get_score() - 120
            # p_tiny = 30% - 20%
            p_tiny = .3 - n_score * .0016
            v_tiny = random.randint(5, 15)
            # p_small = 60% - 50%
            p_small = .9 - n_score * .0033
            v_small = random.randint(5, 15)
            # p_med = 10% - 20%
            p_med = 1 - n_score * .0016
            v_med = random.randint(3, 10)
            # p_big = 0% - 10%
            p_big = 1
            v_big = random.randint(1, 2 + int(n_score * .09))
        else:
            # p_tiny = 20%
            p_tiny = .2
            v_tiny = random.randint(5, 15)
            # p_small = 50% - 40%
            p_small = .6
            v_small = random.randint(5, 15)
            # p_med = 20% - 25%
            p_med = .85
            v_med = random.randint(3, 10)
            # p_big = 10% - 15%
            p_big = 1
            v_big = random.randint(1, 7)

        p = random.random()
        if p < p_tiny:
            sprite = random.choice(self.tiny_meteors)
            speed = v_tiny
        elif p < p_small:
            sprite = random.choice(self.small_meteors)
            speed = v_small
        elif p < p_med:
            sprite = random.choice(self.med_meteors)
            speed = v_med
        elif p < p_big:
            sprite = random.choice(self.big_meteors)
            speed = v_big

        return f'meteors/{sprite}', speed

    #
    # Enemy System
    #
    def add_enemy(self):
        '''
        This method generates an enemy based on select enemy method of
        the difficulty system
        '''
        sprite, speed = self.select_enemy()
        enemy = Enemy(sprite)
        enemy.start(speed)
        enemy.set_pos(
            random.randint(
                self.screen_w + 20,
                self.screen_w + 100
            ),
            random.randint(0, self.screen_h)
        )
        enemy.update_box_collider()
        self.render_group.add(enemy, layer=ENEMY_LAYER)
        self.update_group.add(enemy)
        self.enemies.add(enemy)

    #
    # Player System
    #
    def player_collide(self):
        '''
        This method handles the case when the player hits an enemy
        Will trigger the game over ui
        '''
        self.player.kill()
        self.sound.fadeout(100)
        self.lose_sound.play()
        self.ui.start_game_over(self.cursor)
        self.cursor.add(
            self.event_group,
            self.update_group,
            self.render_group,
        )

    #
    # Restart System
    #
    def restart(self):
        '''
        This method handles the restart option of the game over menu
        will restart all the environment variables and restart the
        journey
        '''
        self.ui.start_score()
        self.cursor.clear()
        self.cursor.kill()
        for e in self.enemies.sprites():
            e.kill()
        self.phase = 0
        self.player.set_pos(0, 0)
        self.sound.play()
        self.render_group.add(self.player, layer=PLAYER_LAYER)
        self.update_group.add(self.player)

    #
    # CORE
    #
    def clear(self):
        self.enemies.empty()
        self.phase = 0
        set_timer(events.ADD_ENEMY, 0)

    def start(self):
        # Sound Config
        self.sound = Sound(
            get_asset_path('sounds', 'bensound-game.ogg')
        )
        self.sound.set_volume(.2)
        self.sound.play()

        self.lose_sound = Sound(
            get_asset_path('sounds', 'sfx_lose.ogg')
        )

        # Game object creation
        self.background = Background('blue.png')
        self.player = Player(
            'playerShip1_blue.png',
            rotation=-90,
            scale_factor=.5,
        )
        self.ui = GameUI()
        self.cursor = Cursor('playerLife1_blue.png', 'sfx_zap.ogg')

        # Custom group creation
        self.enemies = Group()

        # Add objects to groups
        self.render_group.add(self.background, layer=BACKGROUND_LAYER)
        self.render_group.add(self.player, layer=PLAYER_LAYER)
        self.render_group.add(self.ui, layer=UI_LAYER)

        self.update_group.add(
            self.player,
            self.ui,
        )

        # Start objects
        self.player.start()
        self.ui.start()

    def update(self):
        # Event handling
        for e in self.events:
            if e.type == events.ADD_ENEMY:
                self.add_enemy()

        if self.player.alive():
            # Phase handling
            self.update_phase()

            # Collision handling
            if spritecollideany(self.player, self.enemies, box_collide):
                self.player_collide()
        else:
            if self.cursor.selected is not None:
                if self.cursor.selected == 0:
                    self.restart()
                elif self.cursor.selected == 1:
                    self.exit(1)
