import pygame as pg
from colors import *
from player import *
from bullet import *
from orb import *
import sys
import random
import os
import math

class Game:
	def __init__(self):
		pg.init()
		self.SCREEN = pg.display.set_mode((800,600))
		self.FPS = 60
		self.CLOCK = pg.time.Clock()
		self.font = pg.font.Font(os.path.join('assets', 'font', '8bit.ttf'), 32)
		self.font20 = pg.font.Font(os.path.join('assets', 'font', '8bit.ttf'), 20)
		self.font12 = pg.font.Font(os.path.join('assets', 'font', '8bit.ttf'), 12)

		self.damagetext_cp = 0
		self.last_damage = 0
		self.last_player_pos = None

		self.points = 0

		self.bullet_increase_interval = 5000
		self.bullet_increase_cp = 0
		self.bullet_interval = 300
		self.bullet_speed = 3

		self.bullet_time = 0
		self.current_time = 0
		self.bullets = []
		self.ui_height = 56

		self.orbs = []
		self.orb_ticks = 6000
		self.orb_cp = 0


		self.mutations = ['speed+',
						  'regen+',
						  'regen rate+',
						  'health+',
						  'immunity+',
						  'defense+',
						  'bullet speed-']
		self.mutation_cp = 0
		self.last_mutation = None

		self.played, self.played_cp = 0,0 # time user has been playing

		# game states
		self.running = True
		self.in_menu = False

		self.player = Player(self.SCREEN)




	def draw(self, screen):
		screen.fill(BLACK)

		if self.current_time > self.bullet_time:
			self.spawn_bullet(random.randint(0,3))
			self.bullet_time = self.current_time + self.bullet_interval

		to_remove = []
		for bullet in self.bullets:
			bullet.move()
			if bullet.rect.colliderect(self.player.rect) and not self.player.is_immune:
				self.last_damage = self.player.gethit(30)
				self.last_player_pos = (self.player.rect.x, self.player.rect.y-12)
				self.damagetext_cp = self.current_time
				to_remove.append(bullet)
			bullet.draw(screen)
		# revove bullets that has hit the player
		for i in to_remove:
			self.bullets.remove(i)

		to_remove = []
		for orb in self.orbs:
			if orb.rect.colliderect(self.player.rect):
				orb.mutate(self)
				to_remove.append(orb)
			orb.draw(screen)

		for i in to_remove:
			self.orbs.remove(i)

		self.player.draw(screen)
		self.draw_damage(screen, self.last_damage)
		self.draw_ui(screen)

		pg.display.flip()

	def handle_event(self, event):
		if event.type == pg.QUIT:
			sys.exit()
			pg.quit()
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_ESCAPE:
				if self.in_menu:
					self.in_menu = False
				else:
					self.in_menu = True


	def draw_ui(self, screen):
		pg.draw.rect(screen, GREY45, ((0,0), (screen.get_size()[0], self.ui_height ))) # background of hud

		pg.draw.rect(screen, GREY35, ( (10,10), (300, 36) ))
		pg.draw.rect(screen, PLAYER_HEALTH, ( (10,10), ((self.player.health * 300 )//self.player.max_health, 36) ))

		phealth = self.font.render(f"{self.player.health}/{self.player.max_health}", True, WHITE)
		screen.blit(phealth, (10+(300//2)-phealth.get_width()//2,10))


		played = self.font.render(f"{str(self.played//60).rjust(2, '0')}:{str(self.played%60).rjust(2, '0')}", True, WHITE)
		screen.blit(played, (screen.get_size()[0]//2 - played.get_width()//2,10))


		points = self.font.render(f'{str(self.points).rjust(5)}', True, POINTS)
		screen.blit(points, (screen.get_size()[0]-points.get_width()-10, (10)))

		
		mutation = self.font20.render(f'{self.last_mutation}', True, FADE0)

		if self.current_time - self.mutation_cp > 2650:
			mutation = self.font20.render('', True, FADE4)
		elif self.current_time - self.mutation_cp > 2400:
			mutation = self.font20.render(f'{self.last_mutation}', True, FADE3)
		elif self.current_time - self.mutation_cp > 2150:
			mutation = self.font20.render(f'{self.last_mutation}', True, FADE2)
		elif self.current_time - self.mutation_cp > 1900:
			mutation = self.font20.render(f'{self.last_mutation}', True, FADE1)
		if self.last_mutation != None:
			screen.blit(mutation, (5, screen.get_size()[1]-mutation.get_height()))

	def draw_damage(self, screen, damage):

		damage_txt = self.font12.render(f'{damage*-1}', True, DAMAGE0)

		if self.current_time - self.damagetext_cp > 1300:
			damage_txt = self.font12.render('', True, DAMAGE4)
		elif self.current_time - self.damagetext_cp > 1100:
			damage_txt = self.font12.render(f'{damage*-1}', True, DAMAGE3)
		elif self.current_time - self.damagetext_cp > 900:
			damage_txt = self.font12.render(f'{damage*-1}', True, DAMAGE2)
		elif self.current_time - self.damagetext_cp > 700:
			damage_txt = self.font12.render(f'{damage*-1}', True, DAMAGE1)

		if self.last_player_pos != None:
			screen.blit(damage_txt, self.last_player_pos)

	def spawn_bullet(self, side):
		bullet = None
		if side == 0:
			bullet = Bullet((-16, random.randint(8, self.SCREEN.get_size()[1]) - 8), (16, 8), [side], self.bullet_speed)
		elif side == 1:
			bullet = Bullet((random.randint(8, self.SCREEN.get_size()[0]) - 8, -16), (8, 16), [side], self.bullet_speed)
		elif side == 2:
			bullet = Bullet((self.SCREEN.get_size()[0] + 16, random.randint(8, self.SCREEN.get_size()[1]) - 8), (16, 8), [side], self.bullet_speed)
		elif side == 3:
			bullet = Bullet((random.randint(8, self.SCREEN.get_size()[0]) - 8, self.SCREEN.get_size()[1] + 16), (8, 16), [side], self.bullet_speed)

		self.bullets.append(bullet)

	def spawn_orb(self):
		if len(self.orbs) > 2:
			self.orbs.pop(0)
		orb = Orb( (random.randint(24, self.SCREEN.get_size()[0]-24), random.randint(self.ui_height + 24, self.SCREEN.get_size()[1] - 24)) )
		self.orbs.append(orb)


	def draw_menu(self, screen):
		pg.draw.rect(screen, WHITE, (screen.get_size()[0]//2, screen.get_size()[1]//2, 100,100))

		pg.display.flip()


	def start(self):
		while self.running:
			self.current_time = pg.time.get_ticks()
			self.CLOCK.tick(self.FPS)
			for event in pg.event.get():
				self.handle_event(event)
			if self.in_menu:
				self.draw_menu(self.SCREEN)
			else:
				self.draw(self.SCREEN)
				keys_pressed = pg.key.get_pressed()
				self.player.move(keys_pressed, self.SCREEN)
	
				if self.current_time - self.played_cp > self.played:
					self.played += 1
					self.played_cp = self.current_time + 1000
					self.points += 2
	
				if self.current_time - self.bullet_increase_cp > self.bullet_increase_interval:
					self.bullet_increase_cp = self.current_time
					self.bullet_interval -= 5
	
				if self.current_time - self.orb_cp > self.orb_ticks:
 					self.orb_cp = self.current_time
 					self.spawn_orb()

if __name__ == '__main__':
	g = Game()
	g.start()