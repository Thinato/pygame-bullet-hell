from colors import *
import pygame as pg
import math

class Player:
	def __init__(self, screen):
		self.size = (16,16)
		self.rect = pg.Rect((screen.get_size()[0]//2 - self.size[0]//2, screen.get_size()[1]//2 - self.size[1]//2 + (80-self.size[0])), self.size )
		self.speed = 1
		self.defense = 1

		self.immunity_cp = 0
		self.immunity_ticks = 1000
		self.is_immune = False


		self.regen_cp = 0
		self.regen, self.regen_ticks = 1, 1500

		self.max_health, self.health = 100,100


	def draw(self, screen):
		if self.is_immune:
			if pg.time.get_ticks() - self.immunity_cp > self.immunity_ticks:
				self.is_immune = False
			pg.draw.rect(screen, DARK_GREEN, self.rect)
		else:
			self.check_regen()
			pg.draw.rect(screen, GREEN, self.rect)

	def check_regen(self):
		if pg.time.get_ticks() - self.regen_cp > self.regen_ticks and self.health < self.max_health:
			self.heal(self.regen)
			self.regen_cp = pg.time.get_ticks()


	def move(self, keys, screen):
		if keys[pg.K_a] and self.rect.x - self.speed > 0: # LEFT
			self.rect.x -= self.speed
		if keys[pg.K_d] and self.rect.x + self.speed < screen.get_size()[0] - self.rect.width: # RIGHT
			self.rect.x += self.speed
		if keys[pg.K_w] and self.rect.y - self.speed > 56: # UP
			self.rect.y -= self.speed
		if keys[pg.K_s] and self.rect.y + self.speed < screen.get_size()[1] - self.rect.height: # DOWN
			self.rect.y += self.speed

	def gethit(self, damage):
		dmg = math.floor(damage * math.log(100 - self.defense*10, 100))
		self.health	-= dmg
		self.is_immune = True
		self.immunity_cp = pg.time.get_ticks()
		return dmg

	def heal(self, amount):
		if self.health + amount > self.max_health:
			self.health = self.max_health
		else:
			self.health += amount
