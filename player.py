from colors import *
import pygame as pg
import math
import sfx

class Player:
	def __init__(self, screen, cfg):
		self.size = (16,16)
		self.rect = pg.Rect((screen.get_size()[0]//2 - self.size[0]//2, screen.get_size()[1]//2 - self.size[1]//2 + (80-self.size[0])), self.size )
		self.speed = cfg.upgrades['speed']
		self.max_speed = 3
		self.defense = 1
		self.max_defense = 8

		self.show_info = cfg.show_info

		self.immunity_cp = 0
		self.immunity_ticks = 1000
		self.max_immunity_ticks = 1500
		self.is_immune = False


		self.regen_cp = 0
		self.regen, self.regen_ticks = 1, 1500
		self.max_regen = 5
		self.min_regen_ticks = 1000

		self.max_health, self.health = 100,100
		self.max_max_health = 220

		self.color = GREEN
		self.immunity_color = DARK_GREEN

		self.maxxed = False

		self.px, self.py = 0,0


	def max(self, game):
		self.speed = self.max_speed
		self.regen = self.max_regen
		self.max_health = self.max_max_health
		self.health = self.max_health
		self.regen_ticks = self.min_regen_ticks
		self.immunity_ticks = self.max_immunity_ticks
		game.bullet_speed = game.bullet_speed_min
		self.defense = self.max_defense
		self.is_maxxed(game)

	def draw(self, screen, show_info=False):
		if self.is_immune:
			if pg.time.get_ticks() - self.immunity_cp > self.immunity_ticks:
				self.is_immune = False
			pg.draw.rect(screen, self.immunity_color, self.rect)
		else:
			self.check_regen()
			pg.draw.rect(screen, self.color, self.rect)
		if show_info:
			pg.draw.rect(screen, WHITE, self.rect, 1)
			pg.draw.line(screen, BLUE, (self.rect.x+self.size[0]//2, self.rect.y+self.size[1]//2), (self.rect.x+self.size[0]//2+self.px, self.rect.y+self.size[1]//2+self.py))

	def check_regen(self):
		if pg.time.get_ticks() - self.regen_cp > self.regen_ticks and self.health < self.max_health:
			self.heal(self.regen)
			self.regen_cp = pg.time.get_ticks()


	def move(self, keys, screen, fps):
		self.px, self.py = 0,0
		if keys[pg.K_a] and self.rect.x - self.speed > 0: # LEFT
			self.rect.x -= self.speed
			self.px -= self.speed*fps
		if keys[pg.K_d] and self.rect.x + self.speed < screen.get_size()[0] - self.rect.width: # RIGHT
			self.rect.x += self.speed
			self.px += self.speed*fps
		if keys[pg.K_w] and self.rect.y - self.speed > 56: # UP
			self.rect.y -= self.speed
			self.py -= self.speed*fps
		if keys[pg.K_s] and self.rect.y + self.speed < screen.get_size()[1] - self.rect.height: # DOWN
			self.rect.y += self.speed
			self.py += self.speed*fps


	# get hit, damage is the amount of health to be removed
	# truedamage is to ignore player's defense
	def gethit(self, damage, game, truedamage=False):
		if truedamage:
			dmg = damage
		else:
			dmg = math.floor(damage * math.log(85 - self.defense*10, 100))
		self.health	-= dmg
		self.is_immune = True
		self.immunity_cp = pg.time.get_ticks()
		game.draw(game.SCREEN) # just to update the health bar
		if self.is_dead():
			game.cfg.mutation_points += game.points
			game.in_game_over = True
		return dmg

	def heal(self, amount):
		if self.health + amount > self.max_health:
			self.health = self.max_health
		else:
			self.health += amount

	def is_maxxed(self, game):
		if not self.maxxed and self.speed / self.max_speed == 1 and self.regen / self.max_regen == 1 and self.max_health / self.max_max_health == 1 and self.regen_ticks / self.min_regen_ticks == 1 and self.immunity_ticks / self.max_immunity_ticks == 1 and self.defense / self.max_defense == 1 and round(game.bullet_speed, 2) / game.bullet_speed_min == 1:
			self.maxxed = True
			self.color = MAXXED
			self.immunity_color = DARK_MAXXED
			game.orb_ticks = 3000
			sfx.player_evolve.play()
		else:
			self.maxxed = False

	def teleport(self, coords, game):
		sfx.player_teleport.play()
		game.last_damage = self.gethit(25, game, True)
		game.damagetext_cp = game.current_time
		self.rect.x, self.rect.y = coords[0]-self.size[0]//2, coords[1]-self.size[1]//2
		game.last_player_pos = (self.rect.x, self.rect.y-12)

	def is_dead(self):
		if self.health <= 0:
			sfx.player_death.play()
			return True
		return False
