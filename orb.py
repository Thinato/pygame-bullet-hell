import pygame as pg
from colors import *
import random

class Orb:
	def __init__(self, pos):
		self.size = (24,24)
		self.disappear_tick = 5000
		self.rect = pg.Rect(pos, self.size)
		self.surface = pg.Surface(self.size)
		self.mutations = ['speed+',
						  'regen+',
						  'regen rate+',
						  'health+',
						  'immunity+',
						  'defense+',
						  'bullet speed-']
		self.mutation = random.choice(self.mutations)



	def draw(self, screen):
		if   self.mutation == 'speed+':
			pg.draw.circle(screen, M_SPEED, (self.rect.x+self.size[0]//2, self.rect.y+self.size[0]//2), self.size[0]//2)
		elif self.mutation == 'regen+':
			pg.draw.circle(screen, M_REGEN, (self.rect.x+self.size[0]//2, self.rect.y+self.size[0]//2), self.size[0]//2)
		elif self.mutation == 'health+':
			pg.draw.circle(screen, M_REGENRATE, (self.rect.x+self.size[0]//2, self.rect.y+self.size[0]//2), self.size[0]//2)
		elif self.mutation == 'regen rate+':
			pg.draw.circle(screen, M_HEALTH, (self.rect.x+self.size[0]//2, self.rect.y+self.size[0]//2), self.size[0]//2)
		elif self.mutation == 'immunity+':
			pg.draw.circle(screen, M_IMMUNITY, (self.rect.x+self.size[0]//2, self.rect.y+self.size[0]//2), self.size[0]//2)
		elif self.mutation == 'defense+':
			pg.draw.circle(screen, M_DEFENSE, (self.rect.x+self.size[0]//2, self.rect.y+self.size[0]//2), self.size[0]//2)
		elif self.mutation == 'bullet speed-':
			pg.draw.circle(screen, M_BULLETSPEED, (self.rect.x+self.size[0]//2, self.rect.y+self.size[0]//2), self.size[0]//2)

	def mutate(self, game):
		game.points += 50

		game.last_mutation = self.mutation
		game.mutation_cp = game.current_time

		if self.mutation == 'speed+':
			game.player.speed += 1
		elif self.mutation == 'regen+':
			game.player.regen += 1
		elif self.mutation == 'health+':
			game.player.max_health += 20
			game.player.heal(20)
		elif self.mutation == 'regen rate+':
			game.player.regen_ticks -= 100
		elif self.mutation == 'immunity+':
			game.player.immunity_ticks += 100
		elif self.mutation == 'bullet speed-':
			game.bullet_speed -= 0.05
		elif self.mutation == 'defense+':
			game.player.defense += 1





