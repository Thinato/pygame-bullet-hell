import pygame as pg
from colors import *
import math
import random

class Orb:
	def __init__(self, pos, weights, magnet):
		self.size = (24,24)
		self.rect = pg.Rect(pos, self.size)
		self.magnet_value = magnet
		self.magnet_rect = pg.Rect((pos[0]-10*self.magnet_value, pos[1]-10*self.magnet_value), (self.size[0] + 20*self.magnet_value, self.size[1] + 20*self.magnet_value))

		self.surface = pg.Surface(self.size)
		self.mutations = ['speed+',
						  'regen+',
						  'regen rate+',
						  'health+',
						  'immunity+',
						  'defense+',
						  'bullet speed-']
		self.weights = weights
		self.mutation = random.choices(self.mutations, weights=weights, k=1)[0]

	def magnet(self, speed, target_pos):
		angle = math.atan2(target_pos[1] - self.rect.y, target_pos[0] - self.rect.x)
		dx = math.cos(angle) * speed
		dy = math.sin(angle) * speed

		self.rect.x += int(dx)
		self.rect.y += int(dy)

		self.magnet_rect.x = self.rect.x-10*self.magnet_value
		self.magnet_rect.y = self.rect.y-10*self.magnet_value


	def draw(self, screen, game):
		if game.cfg.show_info:
			pg.draw.rect(screen, WHITE, self.magnet_rect, 1)
			pg.draw.line(screen, RED, (self.rect.x+self.size[0]//2, self.rect.y+self.size[1]//2), (game.player.rect.x+game.player.size[0]//2, game.player.rect.y+game.player.size[1]//2))
		if game.player.maxxed:
			pg.draw.circle(screen, WHITE, (self.rect.x+self.size[0]//2, self.rect.y+self.size[0]//2), self.size[0]//2)
		else:
			if   self.mutation == 'speed+':
				pg.draw.circle(screen, M_SPEED, (self.rect.x+self.size[0]//2, self.rect.y+self.size[0]//2), self.size[0]//2)
			elif self.mutation == 'regen+':
				pg.draw.circle(screen, M_REGEN, (self.rect.x+self.size[0]//2, self.rect.y+self.size[0]//2), self.size[0]//2)
			elif self.mutation == 'regen rate+':
				pg.draw.circle(screen, M_HEALTH, (self.rect.x+self.size[0]//2, self.rect.y+self.size[0]//2), self.size[0]//2)
			elif self.mutation == 'health+':
				pg.draw.circle(screen, M_REGENRATE, (self.rect.x+self.size[0]//2, self.rect.y+self.size[0]//2), self.size[0]//2)
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
			game.last_mutation = game.lang.lang[self.mutation]
	
			if self.mutation == 'speed+':
				if game.player.speed < game.player.max_speed:
					game.player.speed += 1
				game.weights[0] = round(game.weights[0]-0.1,1)
			elif self.mutation == 'regen+':
				if game.player.regen < game.player.max_regen:
					game.player.regen += 1
				game.weights[1] = round(game.weights[1]-0.1,1)
			elif self.mutation == 'regen rate+':
				if game.player.regen_ticks > game.player.min_regen_ticks:
					game.player.regen_ticks -= 100
				game.weights[2] = round(game.weights[2]-0.1,1)
			elif self.mutation == 'health+':
				if game.player.max_health < game.player.max_max_health:
					game.player.max_health += 20
				game.player.heal(20)
				game.weights[3] = round(game.weights[3]-0.1,1)
			elif self.mutation == 'immunity+':
				if game.player.immunity_ticks < game.player.max_immunity_ticks:
					game.player.immunity_ticks += 100
				game.weights[4] = round(game.weights[4]-0.1,1)
			elif self.mutation == 'bullet speed-':
				if round(game.bullet_speed,2) > game.bullet_speed_min:
					game.bullet_speed -= 0.05
				game.weights[5] = round(game.weights[5]-0.1,1)
			elif self.mutation == 'defense+':
				if game.player.defense < game.player.max_defense:
					game.player.defense += 1
				game.weights[6] = round(game.weights[6]-0.1,1)





