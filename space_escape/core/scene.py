from pygame import QUIT, display, event
from pygame.display import Info
from pygame.sprite import Group, LayeredUpdates
from pygame.surface import Surface
from pygame.time import Clock


class Scene:
    '''
    Describe a Scene in a game.

    This is a base class for every scene in the game, has a main_loop
    that can be called from the main process and the functions start and
    update to controll the first and sucesives ticks respectively.
    '''
    def __init__(self, screen: Surface):
        '''
        Constructor of the class, takes the screen to gain control over
        the render of the game objects
        '''
        # Get display info
        info = Info()
        # Get Clock to ensure frame rating
        self.clock = Clock()
        # The default return value of the Scene
        self.return_value = -1
        # Set the continue condition
        self.running = True
        # Get the relevant information from info
        self.screen_h, self.screen_w = info.current_h, info.current_w
        # Set the screen of the Scene
        self.screen: Surface = screen

        # Main Sprite groups
        self.event_group = Group()
        self.update_group = Group()
        self.render_group = LayeredUpdates()

    def start(self):
        '''
        This function will is the first function called when the scene starts
        running, here you can configure the position and starting behaviour of
        your scene
        '''
        pass

    def update(self):
        '''
        This function will be called every tick of the game and needs
        to be overrided in every scene to fill the desired behaviour
        '''
        pass

    def clear(self):
        '''
        This function will be called on the end of the scene to clean any
        configuration or variables to the next scene.

        It will raise NotImplementedError if it's not implemented, at least
        needs a pass function if no work is needed
        '''
        raise NotImplementedError

    def exit(self, return_value):
        '''
        This function will end the scene and return the value to the parent
        '''
        self.running = False
        self.return_value = return_value
        self.event_group.empty()
        self.update_group.empty()
        self.render_group.empty()
        self.clear()

    def main_loop(self):
        '''
        This is the main loop of the scene, don't overrive if not necesary.
        Here you will find the main workflow for an scene
        '''
        # Ensures the starts conditions
        self.running = True
        self.return_value = -1

        # Calls the start function, to configurate the scene
        self.start()

        # Main loop of the scene
        while self.running:
            # Event catch
            for e in event.get():
                for s in self.event_group.sprites():
                    s.add_event(e)
                if e.type == QUIT:
                    self.running = False

            # Group update
            self.update_group.update()

            # Calls the update function for every tick of the game
            self.update()

            # Render group
            self.screen.fill((0, 0, 0))
            self.render_group.draw(self.screen)

            display.flip()

            # Ensure frame rate
            self.clock.tick(60)

        return self.return_value
