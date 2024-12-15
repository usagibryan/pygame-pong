import sys
from settings import *
from sprites import Player, Opponent, Ball
from game import GameManager
from crt import CRT
from audio import Audio

# General setup
pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
clock = pygame.time.Clock()
audio = Audio()

# Joystick setup
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

# Main Window
# without pygame.SCALED as a second argument the aspect ratio stretches, but with scaled CRT doesn't look good
screen = pygame.display.set_mode((SCREEN_WIDTH ,SCREEN_HEIGHT), pygame.SCALED)
crt = CRT(screen)
pygame.display.set_caption('Pong')

# Global Variables
basic_font = pygame.font.Font('freesansbold.ttf', 32)
middle_strip = pygame.Rect(SCREEN_WIDTH /2 - 2,0,4,SCREEN_HEIGHT)
full_screen = False

# Game objects
player = Player('graphics/paddle.png',SCREEN_WIDTH  - 20,SCREEN_HEIGHT/2,5)
opponent = Opponent('graphics/paddle.png',20,SCREEN_WIDTH /2,5)
paddle_group = pygame.sprite.Group()
paddle_group.add(player)
paddle_group.add(opponent)

# TODO find a better solution to just passing in basic_font and screen. Put font in settings?
ball = Ball('graphics/ball.png',SCREEN_WIDTH /2,SCREEN_HEIGHT/2,4,4,paddle_group,audio,basic_font,screen)
ball_sprite = pygame.sprite.GroupSingle()
ball_sprite.add(ball)

game_manager = GameManager(ball_sprite,paddle_group,basic_font,screen)

while True:
	
	# Handling Input
	for event in pygame.event.get():

		# Exit Window Option
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		# Keyboard Controls
		if event.type == pygame.KEYDOWN:
			if event.mod & pygame.KMOD_ALT and event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]: # change to F11?
				pygame.display.toggle_fullscreen()
				full_screen = not full_screen # when full screen is toggled change when CRT lines are drawn
			if event.key == pygame.K_UP:
				player.movement -= player.speed
			if event.key == pygame.K_DOWN:
				player.movement += player.speed
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_UP:
				player.movement += player.speed
			if event.key == pygame.K_DOWN:
				player.movement -= player.speed
	
		# Joystick controls

		# Get data from print outs
		# if event.type == pygame.JOYBUTTONDOWN:
		# 	print(event)
		# if event.type == pygame.JOYBUTTONUP:
		# 	print(event)
		if event.type == pygame.JOYAXISMOTION:
			# print(event)
			# Axis 1 (Vertical movement) controls paddle
			if event.axis == 1:  # Vertical axis on most joysticks
				if event.value < -0.1:  # Push up
					player.movement = -player.speed
				elif event.value > 0.1:  # Push down
					player.movement = player.speed
				else:  # Stick is centered
					player.movement = 0
		if event.type == pygame.JOYHATMOTION:
			# print(event)
			# D-Pad controls paddle
			if event.value[1] == 1:  # D-Pad up
				player.movement = -player.speed
			elif event.value[1] == -1:  # D-Pad down
				player.movement = player.speed
			else:  # D-Pad centered
				player.movement = 0

	# Background Stuff
	screen.fill(BG_COLOR)
	pygame.draw.rect(screen,ACCENT_COLOR,middle_strip)
	
	# Run the game
	game_manager.run_game()

	#Music
	if not audio.channel_0.get_busy(): # without this it sounds like static
		audio.channel_0.play(audio.bg_music)

	# Rendering
	if full_screen == False: # only draw CRT lines when not in full screen
		crt.draw()
	pygame.display.flip()
	clock.tick(FRAMERATE) # TODO use delta time for frame rate, also IMO ball is too slow