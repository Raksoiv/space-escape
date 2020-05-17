# Import the pygame module
import pygame
# Import pygame.locals for easier access to key coordinates
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT

from player import Player
from enemy import Enemy

# Initialize pygame
pygame.init()

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Variable to keep the main loop running
running = True

# Initialize external objects
player = Player(screen_limits=(SCREEN_WIDTH, SCREEN_HEIGHT))

enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Main loop
while running:
    # Event catch
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False
        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            running = False
    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()

    # Update the objects
    # Update the player sprite based on user keypresses
    player.update(pressed_keys)

    # Render
    # Fill the screen with white
    screen.fill((0, 0, 0))

    # Merge the surf Surface with the screen
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Redraw the screen
    pygame.display.flip()

pygame.quit()
