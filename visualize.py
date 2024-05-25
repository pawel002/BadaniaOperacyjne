from classes import *
import matplotlib.pyplot as plt
import pygame
import sys

def visualise(instances: list[RelaxedInstance]):

    pygame.init()

    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Visualisation')

    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)

    clock = pygame.time.Clock()

    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update game state
        # (Add game logic here)

        # Draw everything
        screen.fill(WHITE)  # Fill the screen with white

        # Draw a blue rectangle in the center of the screen
        pygame.draw.rect(screen, BLUE, (screen_width // 2 - 50, screen_height // 2 - 50, 100, 100))

        # Update the display
        pygame.display.flip()

        # Cap the frame rate at 60 FPS
        clock.tick(60)

    # Quit Pygame
    pygame.quit()
    sys.exit()

