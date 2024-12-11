import sys, random
from settings import *
from crt import CRT

def ball_animation():
    # use return statement or class instead of global
    global ball_speed_x, ball_speed_y

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        ball_speed_y *= -1
    if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
        ball_restart()

    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1

def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= SCREEN_HEIGHT:
        player.bottom = SCREEN_HEIGHT

def opponent_ai():
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= SCREEN_HEIGHT:
        opponent.bottom = SCREEN_HEIGHT

def ball_restart():
    global ball_speed_x, ball_speed_y
    ball.center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
    ball_speed_y *= random.choice((1,-1))
    ball_speed_x *= random.choice((1,-1))

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

ball_speed_x = 7 * random.choice((1,-1))
ball_speed_y = 7 * random.choice((1,-1))
player_speed = 0
opponent_speed = 7

while True:
    # Handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -= 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            if event.key == pygame.K_UP:
                player_speed += 7
                
    ball_animation()
    player_animation()
    opponent_ai()

    # Visuals
    screen.fill(BG_COLOR)
    pygame.draw.rect(screen,GOLD,player)
    pygame.draw.rect(screen,GOLD,opponent)
    pygame.draw.ellipse(screen,RED,ball)
    pygame.draw.aaline(screen,DEEPSKYBLUE,(SCREEN_WIDTH/2,0),(SCREEN_WIDTH/2,SCREEN_HEIGHT))

    # Updating the window
    crt.draw()
    pygame.display.flip()
    clock.tick(FRAMERATE)