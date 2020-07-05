from pygame import K_DOWN, K_RETURN, K_UP, KEYDOWN, RLEACCEL, draw
from pygame.display import Info
from pygame.font import Font
from pygame.image import load
from pygame.mixer import Sound
from pygame.rect import Rect
from pygame.sprite import DirtySprite
from pygame.surface import Surface
from pygame.transform import rotate, scale
from space_escape.utils import colors

from .path import get_asset_path
from .settings import DEBUG


class GameObject(DirtySprite):
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
        # Set the default dirty value to 2 => always dirty
        self.dirty = 2

    def add_event(self, event) -> None:
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

    def update(self, delta):
        '''
        This function will be called every tick of the game and needs
        to be overrided in every game object to fill the desired behaviour

        The delta atttribute is the time on miliseconds that occurs between
        frames

        The base behaviour to handle events is:
        ```python
        for event in self.events:
            ...
        ```
        '''
        pass


class TextObject(GameObject):
    '''
    This class describe a Text Game Object

    This class will be take almost the same parameters as the Font class
    of pygame, it's objective is to create a Game Object that holds a Text
    '''
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
            self.font_color,
        )
        self.rect = self.image.get_rect()

    def change_text(self, text: str):
        '''
        This method allow the change of the text that the object holds
        '''
        self.image = self.font.render(
            text,
            self.antialias,
            self.font_color,
        )
        self.rect = self.image.get_rect()


class SpriteObject(GameObject):
    '''
    This class describe a Image Game Object

    This class admits a image_path relative to the assets/image folder
    as a source for the sprite and two optional parameters that can
    scale and rotate the image
    '''
    def __init__(
        self,
        image_path: str,
        rotation: int = 0,
        scale_factor: float = 1
    ):
        super().__init__()

        raw_image = load(
            get_asset_path('images', image_path)
        )
        raw_image = scale(
            raw_image,
            (
                int(raw_image.get_rect().width * scale_factor),
                int(raw_image.get_rect().height * scale_factor),
            ),
        )
        raw_image = rotate(
            raw_image,
            rotation,
        )
        self.image = raw_image.convert()
        self.image.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.image.get_rect()


class SpriteCollideObject(SpriteObject):
    '''
    This class describes a Sprite Object with a custom box collider

    This class is usefull when you want a object with a collider different
    that the default rect of the image.

    This is usefull to adjust the collider to a
    image with transparent background
    '''
    def start_box_collider(self):
        '''
        This method will set the initial configuration of the collider

        Needs a box_collider_scale to scale the original rect
        '''
        assert hasattr(self, 'box_collider_scale'), \
            'SpriteCollideObject needs a box_collider_scale'
        width = int(self.rect.width * self.box_collider_scale)
        height = int(self.rect.height * self.box_collider_scale)
        self.box_collider = Rect(0, 0, width, height)
        self.box_collider.center = self.rect.center

    def update_box_collider(self):
        '''
        This method will update the location of the collider based on the
        current location of the default rect, to maintain consistency

        This method will listen to DEBUG env variable to show on the screen
        the actual collider boundaries
        '''
        self.box_collider.center = self.rect.center
        if DEBUG:
            draw.rect(
                self.image,
                (0, 255, 0),
                (
                    self.box_collider.x - self.rect.x,
                    self.box_collider.y - self.rect.y,
                    self.box_collider.width,
                    self.box_collider.height,
                ),
                2
            )


class Background(SpriteObject):
    '''
    This class describe a SpriteObject with a custom constructor to
    build a background. It will take a bg_image and replicate throw
    x and y to fill the width and height of the scene
    '''
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

        # Background images should only render once
        # You can override this if your background moves
        self.dirty = 1


class Cursor(SpriteObject):
    '''
    This class describe a SpriteObject with custom methods to build
    and control a cursor, handful for the ui elements

    It will take a image_path as a image located on assets/image,
    a sfx_path as a sound for selected feedback located on assets/sounds
    and an optional margin to set the margin between the position and
    the cursor
    '''
    def __init__(
        self,
        image_path: str,
        sfx_path: str = None,
        margin: int = 10
    ):
        super().__init__(image_path)

        self.actual_position: int = 0
        self.positions: list = []
        self.selected: int = None
        self.margin = margin

        if sfx_path:
            self.sound = Sound(
                get_asset_path('sounds', sfx_path)
            )

    def add_position(self, x, y):
        '''
        This method add a position (x, y) for the cursor to move
        base on player input
        '''
        self.positions.append((x - self.margin, y))
        self.update(0)

    def clear(self):
        '''
        This method resets the cursor information, useful when recycling
        the cursor for more than one ui layout
        '''
        self.selected = None
        self.actual_position = 0
        self.positions = []

    def start(self):
        self.selected = None
        self.actual_position = 0

    def update(self, delta):
        assert len(self.positions) > 0, \
            'Cursor not initializated'

        for event in self.events:
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    self.dirty = 1
                    if self.actual_position == 0:
                        self.actual_position = len(self.positions) - 1
                    else:
                        self.actual_position -= 1
                elif event.key == K_DOWN:
                    self.dirty = 1
                    if self.actual_position == len(self.positions) - 1:
                        self.actual_position = 0
                    else:
                        self.actual_position += 1
                elif event.key == K_RETURN:
                    self.dirty = 1
                    self.sound.play()
                    self.selected = self.actual_position
        self.events = []
        self.rect.x = self.positions[self.actual_position][0]
        self.rect.y = self.positions[self.actual_position][1]
