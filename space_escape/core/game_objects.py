from pygame import K_DOWN, K_RETURN, K_UP, KEYDOWN, RLEACCEL
from pygame.display import Info
from pygame.font import Font
from pygame.image import load
from pygame.mixer import Sound
from pygame.rect import Rect
from pygame.sprite import Sprite
from pygame.surface import Surface

from space_escape.utils import colors

from .path import get_asset_path


class GameObject(Sprite):
    '''
    Describe a Game Object in the game

    This is a base class for every visual object in any scene,
    the start function it's call on construct and the update method
    is call in every tick of the scene, if the object is part of the
    update_group.
    '''
    def __init__(self):
        # Super construcctor
        super().__init__()
        # Base fields
        # Screen size
        info = Info()
        self.screen_h, self.screen_w = info.current_h, info.current_w
        # Starts the event queue
        self.events = []

    def add_event(self, event):
        '''
        This method allows the Game Object to store the events captured by
        the scene and can be access throw self.events
        '''
        self.events.append(event)

    def get_draw(self) -> tuple:
        '''
        This method return a tuple containing the image and rect of the object
        '''
        assert hasattr(self, 'image'), \
            'The game object has no image assigned to'

        if not hasattr(self, 'rect'):
            self.rect = self.image.get_rect()

        return (
            self.image,
            self.rect
        )

    def set_pos(self, x: float, y: float) -> None:
        '''
        This method allow the positioning of the object in a Rect
        if the object doesn't posses a Rect it will be initialize
        '''
        assert hasattr(self, 'image'), \
            'The game object has no image assigned to'

        if not hasattr(self, 'rect'):
            self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def start(self):
        '''
        This function will is the first function called when the game object
        instantiate, here you can configure the position and starting
        behaviour of your game object
        '''
        pass

    def update(self):
        '''
        This function will be called every tick of the game and needs
        to be overrided in every game object to fill the desired behaviour

        The base behaviour to handle events is:
        ```python
        for event in self.events:
            ...
        ```
        '''
        pass


class TextObject(GameObject):
    def __init__(
        self,
        text,
        font_path,
        antialias=False,
        font_color=colors.black,
        font_size=16,
    ):
        super().__init__()
        self.font_color = font_color
        self.font_size = font_size
        self.antialias = antialias
        self.font = Font(
            get_asset_path('fonts', font_path),
            self.font_size
        )
        self.image = self.font.render(
            text,
            self.antialias,
            self.font_color
        )
        self.rect = self.image.get_rect()


class SpriteObject(GameObject):
    def __init__(self, image_path):
        super().__init__()

        self.image = load(
            get_asset_path('images', image_path)
        ).convert()
        self.image.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.image.get_rect()


class Background(SpriteObject):
    def __init__(self, bg_image):
        super().__init__(bg_image)

        raw_image = self.image
        self.image = Surface((self.screen_w, self.screen_h))
        for j in range(int(self.screen_h / raw_image.get_height()) + 1):
            for i in range(int(self.screen_w / raw_image.get_width()) + 1):
                self.image.blit(raw_image, (
                    raw_image.get_width() * i,
                    raw_image.get_height() * j
                ))
        self.rect = self.image.get_rect()


class Cursor(SpriteObject):
    def __init__(
        self,
        image_path: str,
        sfx_path: str = None,
        margin: int = 10
    ):
        super().__init__(image_path)

        self.actual_position = 0
        self.positions = []
        self.selected = None
        self.margin = margin

        if sfx_path:
            self.sound = Sound(
                get_asset_path('sounds', sfx_path)
            )

    def add_position(self, x, y):
        self.positions.append((x - self.margin, y))

    def add_event(self, event):
        self.events.append(event)

    def clear(self):
        self.selected = None
        self.actual_position = 0
        self.positions = []

    def start(self):
        self.selected = None
        self.actual_position = 0

    def update(self):
        assert len(self.positions) > 0, \
            'Cursor not initializated'

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
                    self.sound.play()
                    self.selected = self.actual_position
        self.events = []
        self.rect.x = self.positions[self.actual_position][0]
        self.rect.y = self.positions[self.actual_position][1]
