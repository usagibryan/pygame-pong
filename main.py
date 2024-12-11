import pygame, sys
from settings import *

# General setup
pygame.init()
clock = pygame.time.Clock()

# Setting up the main window
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Pong')

while True:
    # Handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Updating the window
    pygame.display.flip()
    clock.tick(FRAMERATE)