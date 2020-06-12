from pygame.rect import Rect
from pygame import draw
from pygame.surface import Surface
from space_escape.core.game_objects import SpriteCollideObject
from pygame import BLEND_ADD


class Enemy(SpriteCollideObject):
    '''
    This class represents the asteriods in the game
    it's principal objective is to collision the player
    '''
    box_collider_scale = .75

    def start(self, speed: int):
        self.speed = speed
        self.start_box_collider()

    def update(self):
        self.update_box_collider()

        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
