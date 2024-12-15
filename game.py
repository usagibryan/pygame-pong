from settings import *

class GameManager:
	def __init__(self,ball_group,paddle_group,basic_font,screen):
		self.player_score = 0
		self.opponent_score = 0
		self.ball_group = ball_group
		self.paddle_group = paddle_group
		self.basic_font = basic_font
		self.screen = screen

	def run_game(self):
		# Drawing the game objects
		self.paddle_group.draw(self.screen)
		self.ball_group.draw(self.screen)

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
		player_score = self.basic_font.render(str(self.player_score),True,ACCENT_COLOR)
		opponent_score = self.basic_font.render(str(self.opponent_score),True,ACCENT_COLOR)

		player_score_rect = player_score.get_rect(midleft = (SCREEN_WIDTH  / 2 + 40,SCREEN_HEIGHT/2))
		opponent_score_rect = opponent_score.get_rect(midright = (SCREEN_WIDTH  / 2 - 40,SCREEN_HEIGHT/2))

		self.screen.blit(player_score,player_score_rect)
		self.screen.blit(opponent_score,opponent_score_rect)