import json
import time

from pygame import Color, Surface
from space_escape.core.game_objects import GameObject, SpriteObject, TextObject
from space_escape.core.path import HIGHSCORES_BASEPATH
from space_escape.utils import colors


class UIModes:
    '''
    This class represent the possibles states for the UI
    '''
    GAME = 1
    GAME_OVER = 2


class GameUI(GameObject):
    '''
    This class represents all the ui in the Game scene
    '''
    font_file = 'BalooChettan2-SemiBold.ttf'
    score = 0
    mode = UIModes.GAME

    #
    # PLAYER LIFES
    #
    def create_player_lifes(self) -> None:
        '''
        This function creates all the game objects related to the player
        lifes counter
        '''
        self.player_lifes = [
            SpriteObject('playerLife1_blue.png')
            for _ in range(3)
        ]

        # Set on the screen
        y_pos = 10
        x_pos = self.screen_w - self.player_lifes[0].rect.width - 10

        for i in range(3):
            self.player_lifes[i].set_pos(
                x_pos,
                y_pos
            )
            x_pos -= self.player_lifes[i].rect.width + 10

    #
    # SCORE
    #
    def get_score(self) -> int:
        '''
        This method returns the current score of the player
        '''
        return self.score

    def update_score(self) -> None:
        '''
        This method update the score of the player based on the amount of time
        that the player stay alive
        '''
        if self.score != int(time.time() - self.start_time):
            self.score = int(time.time() - self.start_time)
            # Change text will reset the pos of the game object
            self.score_ui.change_text(f'Score: {self.score}')
            self.score_ui.dirty = 1

    def save_score(self):
        '''
        This method update the persistent score record of the game,
        it saves the best 5 scores
        '''
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

    def start_score(self):
        '''
        This method sets the default values for the score at the start
        of the game
        '''
        self.start_time = time.time()
        self.mode = UIModes.GAME
        self.score_ui.dirty = 1

    #
    # GAMEOVER
    #
    def create_game_over_screen(self):
        '''
        This method will create all the elements for the game over object
        creates the surface and asign to self.game_over
        '''
        self.title = TextObject(
            'GAME OVER',
            self.font_file,
            antialias=True,
            font_color=colors.white,
            font_size=62,
        )
        self.title.rect.move_ip((
            (self.screen_w - self.title.rect.width) / 2,
            self.screen_h * .2
        ))

        self.game_over_restart = TextObject(
            'Restart',
            self.font_file,
            antialias=True,
            font_color=colors.white,
            font_size=36,
        )
        self.game_over_restart.rect.move_ip((
            (self.screen_w - self.game_over_restart.rect.width) / 2,
            self.screen_h * .5
        ))

        self.game_over_exit_text = TextObject(
            'Exit',
            self.font_file,
            antialias=True,
            font_color=colors.white,
            font_size=36,
        )
        self.game_over_exit_text.rect.move_ip((
            (self.screen_w - self.game_over_exit_text.rect.width) / 2,
            self.screen_h * .6
        ))

    def start_game_over(self, cursor):
        '''
        This method will be trigger when the players die, it will save
        the score achieved and show the game over UI
        '''
        self.save_score()
        self.mode = UIModes.GAME_OVER
        self.score_ui.set_pos(
            (self.screen_w / 2) - (self.score_ui.rect.width / 2),
            self.screen_h * .3
        )

        cursor.add_position(
            self.game_over_restart.rect.left - cursor.rect.width,
            self.game_over_restart.rect.centery - (cursor.rect.height / 2),
        )
        cursor.add_position(
            self.game_over_restart.rect.left - cursor.rect.width,
            self.game_over_exit_text.rect.centery - (cursor.rect.height / 2),
        )

        self.score_ui.dirty = 1

    #
    # UI
    #
    def get_objects(self):
        if self.mode == UIModes.GAME:
            self.score_ui.dirty = 1
            for i in range(len(self.player_lifes)):
                self.player_lifes[i].dirty = 1
            return (self.score_ui, *self.player_lifes)
        elif self.mode == UIModes.GAME_OVER:
            self.title.dirty = 1
            self.game_over_restart.dirty = 1
            self.game_over_exit_text.dirty = 1
            return (
                self.title,
                self.game_over_restart,
                self.game_over_exit_text
            )

    #
    # CORE
    #
    def start(self):
        # Object creation
        self.score_ui = TextObject(
            'Score: 0',
            self.font_file,
            antialias=True,
            font_color=colors.white,
            font_size=36,
        )
        self.create_player_lifes()
        self.create_game_over_screen()

        # Start with score
        self.start_score()

    def update(self, delta):
        if self.mode == UIModes.GAME:
            self.update_score()
