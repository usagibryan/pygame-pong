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
ball = pygame.Rect(SCREEN_WIDTH/2 - 15,SCREEN_HEIGHT/2 - 15,30,30)
player = pygame.Rect(SCREEN_WIDTH - 20, SCREEN_HEIGHT/2 - 70,10,140)
opponent = pygame.Rect(10, SCREEN_HEIGHT/2 - 70,10,140)

while True:
    # Handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    ball.x += BALL_SPEED_X
    ball.y += BALL_SPEED_Y

    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        BALL_SPEED_Y *= -1
    if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
        BALL_SPEED_X *= -1

    if ball.colliderect(player) or ball.colliderect(opponent):
        BALL_SPEED_X *= -1

    # Visuals
    screen.fill(BG_COLOR)
    pygame.draw.rect(screen,LIGHT_GREY,player)
    pygame.draw.rect(screen,LIGHT_GREY,opponent)
    pygame.draw.ellipse(screen,LIGHT_GREY,ball)
    pygame.draw.aaline(screen,LIGHT_GREY,(SCREEN_WIDTH/2,0),(SCREEN_WIDTH/2,SCREEN_HEIGHT))


    # Updating the window
    crt.draw()
    pygame.display.flip()
    clock.tick(FRAMERATE)