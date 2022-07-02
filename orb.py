import pygame as pg
from colors import *
import random

class Orb:
	def __init__(self, pos):
		self.size = (24,24)
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



	def draw(self, screen, game):
		if game.player.maxxed:
			pg.draw.circle(screen, WHITE, (self.rect.x+self.size[0]//2, self.rect.y+self.size[0]//2), self.size[0]//2)
		else:
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
		game.mutation_cp = game.current_time

		if game.player.maxxed:
			game.points += 100
			game.last_mutation = ''

		else:
			game.points += 50
			game.last_mutation = self.mutation
	
			if self.mutation == 'speed+':
				if game.player.speed < game.player.max_speed:
					game.player.speed += 1
			elif self.mutation == 'regen+':
				if game.player.regen < game.player.max_regen:
					game.player.regen += 1
			elif self.mutation == 'health+':
				if game.player.max_health < game.player.max_max_health:
					game.player.max_health += 20
				game.player.heal(20)
			elif self.mutation == 'regen rate+':
				if game.player.regen_ticks > game.player.min_regen_ticks:
					game.player.regen_ticks -= 100
			elif self.mutation == 'immunity+':
				if game.player.immunity_ticks < game.player.max_immunity_ticks:
					game.player.immunity_ticks += 100
			elif self.mutation == 'bullet speed-':
				if round(game.bullet_speed,2) > game.bullet_speed_min:
					game.bullet_speed -= 0.05
			elif self.mutation == 'defense+':
				if game.player.defense < game.player.max_defense:
					game.player.defense += 1





