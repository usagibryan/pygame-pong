import sys, random
from settings import *
from crt import CRT
from audio import Audio

class Block(pygame.sprite.Sprite):
	def __init__(self,path,x_pos,y_pos):
		super().__init__()
		self.image = pygame.image.load(path)
		self.rect = self.image.get_rect(center = (x_pos,y_pos))

class Player(Block):
	def __init__(self,path,x_pos,y_pos,speed):
		super().__init__(path,x_pos,y_pos)
		self.speed = speed
		self.movement = 0

	def screen_constrain(self):
		if self.rect.top <= 0:
			self.rect.top = 0
		if self.rect.bottom >= SCREEN_HEIGHT:
			self.rect.bottom = SCREEN_HEIGHT

	def update(self,ball_group): # does not use ball_group but still needs it
		self.rect.y += self.movement
		self.screen_constrain()

class Ball(Block):
	def __init__(self,path,x_pos,y_pos,speed_x,speed_y,paddles):
		super().__init__(path,x_pos,y_pos)
		self.speed_x = speed_x * random.choice((-1,1))
		self.speed_y = speed_y * random.choice((-1,1))
		self.paddles = paddles
		self.active = False
		self.score_time = 0

	def update(self):
		if self.active:
			self.rect.x += self.speed_x
			self.rect.y += self.speed_y
			self.collisions()
		else:
			self.restart_counter()
		
	def collisions(self):
		if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
			audio.channel_1.play(audio.plob_sound)
			self.speed_y *= -1

		if pygame.sprite.spritecollide(self,self.paddles,False):
			audio.channel_1.play(audio.plob_sound)
			collision_paddle = pygame.sprite.spritecollide(self,self.paddles,False)[0].rect
			if abs(self.rect.right - collision_paddle.left) < 10 and self.speed_x > 0:
				self.speed_x *= -1
			if abs(self.rect.left - collision_paddle.right) < 10 and self.speed_x < 0:
				self.speed_x *= -1
			if abs(self.rect.top - collision_paddle.bottom) < 10 and self.speed_y < 0:
				self.rect.top = collision_paddle.bottom
				self.speed_y *= -1
			if abs(self.rect.bottom - collision_paddle.top) < 10 and self.speed_y > 0:
				self.rect.bottom = collision_paddle.top
				self.speed_y *= -1

	def reset_ball(self):
		self.active = False
		self.speed_x *= random.choice((-1,1))
		self.speed_y *= random.choice((-1,1))
		self.score_time = pygame.time.get_ticks()
		self.rect.center = (SCREEN_WIDTH /2,SCREEN_HEIGHT/2)
		audio.channel_2.play(audio.score_sound)

	def restart_counter(self):
		current_time = pygame.time.get_ticks()
		countdown_number = 3

		if current_time - self.score_time <= 700:
			countdown_number = 3
		if 700 < current_time - self.score_time <= 1400:
			countdown_number = 2
		if 1400 < current_time - self.score_time <= 2100:
			countdown_number = 1
		if current_time - self.score_time >= 2100:
			self.active = True

		time_counter = basic_font.render(str(countdown_number),True,ACCENT_COLOR)
		time_counter_rect = time_counter.get_rect(center = (SCREEN_WIDTH /2,SCREEN_HEIGHT/2 + 50))
		pygame.draw.rect(screen,BG_COLOR,time_counter_rect)
		screen.blit(time_counter,time_counter_rect)

class Opponent(Block):
	def __init__(self,path,x_pos,y_pos,speed):
		super().__init__(path,x_pos,y_pos)
		self.speed = speed

	def update(self,ball_group):
		if self.rect.top < ball_group.sprite.rect.y:
			self.rect.y += self.speed
		if self.rect.bottom > ball_group.sprite.rect.y:
			self.rect.y -= self.speed
		self.constrain()

	def constrain(self):
		if self.rect.top <= 0: self.rect.top = 0
		if self.rect.bottom >= SCREEN_HEIGHT: self.rect.bottom = SCREEN_HEIGHT

class GameManager:
	def __init__(self,ball_group,paddle_group):
		self.player_score = 0
		self.opponent_score = 0
		self.ball_group = ball_group
		self.paddle_group = paddle_group

	def run_game(self):
		# Drawing the game objects
		self.paddle_group.draw(screen)
		self.ball_group.draw(screen)

		# Updating the game objects
		self.paddle_group.update(self.ball_group)
		self.ball_group.update()
		self.reset_ball()
		self.draw_score()

	def reset_ball(self):
		if self.ball_group.sprite.rect.right >= SCREEN_WIDTH :
			self.opponent_score += 1
			self.ball_group.sprite.reset_ball()
		if self.ball_group.sprite.rect.left <= 0:
			self.player_score += 1
			self.ball_group.sprite.reset_ball()

	def draw_score(self):
		player_score = basic_font.render(str(self.player_score),True,ACCENT_COLOR)
		opponent_score = basic_font.render(str(self.opponent_score),True,ACCENT_COLOR)

		player_score_rect = player_score.get_rect(midleft = (SCREEN_WIDTH  / 2 + 40,SCREEN_HEIGHT/2))
		opponent_score_rect = opponent_score.get_rect(midright = (SCREEN_WIDTH  / 2 - 40,SCREEN_HEIGHT/2))

		screen.blit(player_score,player_score_rect)
		screen.blit(opponent_score,opponent_score_rect)

# General setup
pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
clock = pygame.time.Clock()
audio = Audio()

# Main Window
# without pygame.SCALED as a second argument it stretches, but with scaled CRT doesn't look good
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

ball = Ball('graphics/ball.png',SCREEN_WIDTH /2,SCREEN_HEIGHT/2,4,4,paddle_group)
ball_sprite = pygame.sprite.GroupSingle()
ball_sprite.add(ball)

game_manager = GameManager(ball_sprite,paddle_group)

while True:
	
	# Handling Input
	for event in pygame.event.get():

		# Exit Window Option
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		# Keyboard Controls
		if event.type == pygame.KEYDOWN:
			if event.mod & pygame.KMOD_ALT and event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
				pygame.display.toggle_fullscreen()
				full_screen = not full_screen
			if event.key == pygame.K_UP:
				player.movement -= player.speed
			if event.key == pygame.K_DOWN:
				player.movement += player.speed
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_UP:
				player.movement += player.speed
			if event.key == pygame.K_DOWN:
				player.movement -= player.speed
	
	# Background Stuff
	screen.fill(BG_COLOR)
	pygame.draw.rect(screen,ACCENT_COLOR,middle_strip)
	
	# Run the game
	game_manager.run_game()

	# Music
	if not audio.channel_0.get_busy(): # without this it sounds like static
		audio.channel_0.play(audio.bg_music)

	# Rendering
	if full_screen == False:
		crt.draw()
	pygame.display.flip()
	clock.tick(FRAMERATE) # TODO use delta time for frame rate, also IMO ball is too slow