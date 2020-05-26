import random

from pygame import RLEACCEL
from pygame.image import load
from pygame.sprite import Sprite
from pygame.transform import scale

from space_escape.utils.path import get_assets_path_folder


class Enemy(Sprite):
    def __init__(self, screen_limits: tuple, score: int):
        # Super init
        super().__init__()

        # Set the screen size
        self.screen_width = screen_limits[0]
        self.screen_height = screen_limits[1]

        image_paths = get_assets_path_folder('images/meteors/')
        tiny_meteors = [
            image_path
            for image_path in image_paths
            if 'tiny' in image_path
        ]
        small_meteors = [
            image_path
            for image_path in image_paths
            if 'small' in image_path
        ]
        med_meteors = [
            image_path
            for image_path in image_paths
            if 'med' in image_path
        ]
        big_meteors = [
            image_path
            for image_path in image_paths
            if 'big' in image_path
        ]

        # Phases
        if score < 60:
            # p_tiny = 100% - 50%
            p_tiny = 1 - score * .0083
            v_tiny = random.randint(5, 5 + int(score * 0.09))
            # p_small = 0% - 50%
            p_small = 1
            v_small = random.randint(5, 5 + int(score * 0.09))
        elif score < 120:
            n_score = score - 60
            # p_tiny = 50% - 30%
            p_tiny = .5 - n_score * .0033
            v_tiny = random.randint(5, 10 + int(n_score * .09))
            # p_small = 50% - 60%
            p_small = 1 - n_score * .0016
            v_small = random.randint(5, 10 + int(n_score * .09))
            # p_med = 0% - 10%
            p_med = 1
            v_med = random.randint(3, 5 + int(n_score * .09))
        elif score < 180:
            n_score = score - 120
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
            raw_image = random.choice(tiny_meteors)
            self.speed = v_tiny
        elif p < p_small:
            raw_image = random.choice(small_meteors)
            self.speed = v_small
        elif p < p_med:
            raw_image = random.choice(med_meteors)
            self.speed = v_med
        elif p < p_big:
            raw_image = random.choice(big_meteors)
            self.speed = v_big

        self.image = load(raw_image).convert()
        self.image.set_colorkey((0, 0, 0), RLEACCEL)

        # Set the enemy starting point
        self.rect = self.image.get_rect(center=(
            random.randint(
                self.screen_width + 20,
                self.screen_width + 100
            ),
            random.randint(0, self.screen_height)
        ))

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
