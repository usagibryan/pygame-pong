import pygame

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960
FRAMERATE = 60

# these change as the ball bounces at the edges of the screen
# so should they be in settings.py if they are not constants?
BALL_SPEED_X = 7
BALL_SPEED_Y = 7

# Colors
BG_COLOR = pygame.Color('grey12')
LIGHT_GREY = (200,200,200)