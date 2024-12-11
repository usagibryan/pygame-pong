import sys
from settings import *
from crt import CRT

# General setup
pygame.init()
clock = pygame.time.Clock()

# Setting up the main window
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
crt = CRT(screen)
pygame.display.set_caption('Pong')

# Game Rectangles
ball = pygame.Rect(SCREEN_HEIGHT/2 - 15,SCREEN_HEIGHT/2 -15,30,30,)

while True:
    # Handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Updating the window
    crt.draw()
    pygame.display.flip()
    clock.tick(FRAMERATE)