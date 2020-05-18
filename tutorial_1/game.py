# Import the pygame module
import pygame
# Import pygame.locals for easier access to key coordinates
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT

from player import Player
from enemy import Enemy, DifficultyLevel
from high_score import HighScore


class SpaceEscape:
    def __init__(self, width=800, height=600, diffculty=DifficultyLevel.EASY):
        self.width, self.height = width, height
        # Initialize pygame
        pygame.init()

        # Clock
        self.clock = pygame.time.Clock()

        # Create the screen object
        self.screen = pygame.display.set_mode((self.width, self.height))

        # Create a custom event for adding a new enemy
        self.add_enemy = pygame.USEREVENT + 1
        pygame.time.set_timer(self.add_enemy, 300 * diffculty)

        # Variable to keep the main loop running
        self.running = True

        # Initialize external objects
        self.player = Player(screen_limits=(width, height))
        self.score = HighScore()
        self.enemies = pygame.sprite.Group()

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

    def event_fase(self):
        # Look at every event in the queue
        for event in pygame.event.get():
            # Did the user hit a key?
            if event.type == KEYDOWN:
                # Was it the Escape key? If so, stop the loop.
                if event.key == K_ESCAPE:
                    self.running = False
            # Did the user click the window close button? If so, stop the loop.
            elif event.type == QUIT:
                self.running = False
            # Add a new enemy?
            elif event.type == self.add_enemy:
                # Create the new enemy and add it to sprite groups
                new_enemy = Enemy(
                    screen_limits=(self.width, self.height),
                )
                self.enemies.add(new_enemy)
                self.all_sprites.add(new_enemy)

    def update_face(self):
        # Get the set of keys pressed and check for user input
        pressed_keys = pygame.key.get_pressed()

        # Update the objects
        # Update the player sprite based on user keypresses
        self.player.update(pressed_keys)
        # Get the number of enemies
        n_enemies = len(self.enemies)
        # Update enemy position
        self.enemies.update()
        # Update score
        self.score.update()

    def render_fase(self):
        # Fill the screen with white
        self.screen.fill((0, 0, 0))

        # Merge the surf Surface with the screen
        for entity in self.all_sprites:
            self.screen.blit(entity.surf, entity.rect)

        self.screen.blit(self.score.surf, self.score.rect)

        # Collide detection
        if pygame.sprite.spritecollideany(self.player, self.enemies):
            self.player.kill()
            self.running = False

        # Redraw the screen
        pygame.display.flip()

    def main_loop(self):
        # Event catch
        self.event_fase()

        # Update fase
        self.update_face()

        # Render fase
        self.render_fase()

        # Ensure frame rate
        self.clock.tick(60)

    def quit(self):
        pygame.quit()
