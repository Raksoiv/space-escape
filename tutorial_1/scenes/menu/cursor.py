import pygame.image
from pygame.locals import K_DOWN, K_RETURN, K_UP, KEYDOWN
from pygame.sprite import Sprite


class Cursor(Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load('assets/images/playerLife1_blue.png')
        self.rect = self.image.get_rect()
        self.actual_position = 0
        self.positions = []
        self.events = []
        self.selected = None

    def add_position(self, x, y):
        self.positions.append((x, y))

    def add_event(self, event):
        self.events.append(event)

    def update(self):
        for event in self.events:
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    if self.actual_position == 0:
                        self.actual_position = len(self.positions) - 1
                    else:
                        self.actual_position -= 1
                elif event.key == K_DOWN:
                    if self.actual_position == len(self.positions) - 1:
                        self.actual_position = 0
                    else:
                        self.actual_position += 1
                elif event.key == K_RETURN:
                    self.selected = self.actual_position
        self.events = []
        self.rect.x = self.positions[self.actual_position][0]
        self.rect.y = self.positions[self.actual_position][1]
