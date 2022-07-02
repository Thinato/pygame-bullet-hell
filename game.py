import pygame as pg
from colors import *
from player import *
from bullet import *
from orb import *
from button import *
import sys
import random
import os
import math


class Game:
	def __init__(self):
		pg.init()

		# constants
		self.SCREEN = pg.display.set_mode((800,600))
		self.FPS = 60
		self.CLOCK = pg.time.Clock()
		self.font = pg.font.Font(os.path.join('assets', 'font', '8bit.ttf'), 32)
		self.font20 = pg.font.Font(os.path.join('assets', 'font', '8bit.ttf'), 22)
		self.font22 = pg.font.Font(os.path.join('assets', 'font', '8bit.ttf'), 22)
		self.font12 = pg.font.Font(os.path.join('assets', 'font', '8bit.ttf'), 12)


		# variables that end with 'cp' mean CheckPoint, theyre used to check the timer
		# they store the last tick a command was executed
		self.damagetext_cp = 0
		self.last_damage = 0
		self.last_player_pos = None

		self.points = 0

		self.bullet_increase_interval = 5000
		self.bullet_increase_cp = 0
		self.bullet_interval = 300
		self.bullet_speed = 3
		self.bullet_speed_min = 2.8

		self.bullet_time = 0
		self.current_time = 0
		self.bullets = []
		self.ui_height = 56

		self.orbs = []
		self.orb_ticks = 6000
		self.orb_cp = 0

		self.mutation_cp = 0
		self.last_mutation = None

		self.played, self.played_cp = 0,0 # time user has been playing

		# game states
		self.running = True
		self.in_menu = False
		self.in_game_over = False

		temp = self.font.render('CONTINUE', True, WHITE)
		self.continue_button = Button(self.font, 'CONTINUE', (self.SCREEN.get_size()[0]//2-temp.get_width()//2, self.SCREEN.get_size()[1]//2+140))

		self.player = Player(self.SCREEN)

		# just for testing/debugging
		# self.player.max(self) 




	# this function will draw pretty much everything in the game, except by the pause menu
	def draw(self, screen):
		screen.fill(BLACK)

		if self.current_time > self.bullet_time:
			self.spawn_bullet(random.randint(0,3))
			self.bullet_time = self.current_time + self.bullet_interval

		to_remove = []
		for bullet in self.bullets:
			bullet.move()
			if bullet.rect.colliderect(self.player.rect) and not self.player.is_immune:
				self.last_damage = self.player.gethit(30, self)
				self.last_player_pos = (self.player.rect.x, self.player.rect.y-12)
				self.damagetext_cp = self.current_time
				to_remove.append(bullet)
			bullet.draw(screen)

		# revove bullets that has hit the player
		for i in to_remove:
			self.bullets.remove(i)
		# 'why this to_remove var?': well its never a good idea to remove an item during the identation
		# so its better to just set a list for items that you want to remove after


		to_remove = []
		for orb in self.orbs:
			if orb.rect.colliderect(self.player.rect):
				orb.mutate(self)
				to_remove.append(orb)
				self.player.is_maxxed(self)
			orb.draw(screen, self)

		# remove the orb the player got
		for i in to_remove:
			self.orbs.remove(i)

		self.player.draw(screen)
		self.draw_damage(screen, self.last_damage)
		self.draw_ui(screen)

		pg.display.flip()



	# Handle pygame events
	def handle_event(self, event):
		if event.type == pg.QUIT: # event executed when you click on the window close button (x)
			sys.exit()
			pg.quit()

		elif event.type == pg.KEYDOWN: # when any key is pressed
			if event.key == pg.K_ESCAPE:
				# open and closes the pause menu
				if self.in_menu:
					self.in_menu = False
				else:
					self.in_menu = True

		elif event.type == pg.MOUSEBUTTONUP: # when mouse button is up (it must go down first, of course)
			if self.in_menu:
				pass
			elif self.in_game_over:
				if self.continue_button.hover:
					print('go to main menu')
			else:
				if self.player.maxxed:
					self.player.teleport(pg.mouse.get_pos(), self)



	# draws the entire game hud, 'why is it named draw_ui not draw_hud?': laziness
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

		

		# draws the mutation text and with a improvised 'fade out effect'
		mutation = self.font20.render(f'{self.last_mutation}', True, FADE0)

		# fade out effect
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

	# draws the damage numbers on top of the player
	def draw_damage(self, screen, damage):

		damage_txt = self.font12.render(f'{damage*-1}', True, DAMAGE0)
		# face out effect
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

	# spawns a bullet on a random side of the screen with a random position
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

		# spawn an orb at a random location of the screen and make sure theres always a maximum of 3 orbs on screen 
	def spawn_orb(self):
		if len(self.orbs) > 2:
			self.orbs.pop(0)
		orb = Orb( (random.randint(24, self.SCREEN.get_size()[0]-24), random.randint(self.ui_height + 24, self.SCREEN.get_size()[1] - 24)) )
		self.orbs.append(orb)



	# draws the pause menu
	def draw_menu(self, screen):
		# BACKGROUND
		pg.draw.rect(screen, GREY45, (screen.get_size()[0]//2-200, screen.get_size()[1]//2-200, 400,400))

		# TITLE
		pause = self.font.render("PAUSE", True, WHITE)
		screen.blit(pause, (screen.get_size()[0]//2 - pause.get_width()//2,screen.get_size()[1]//2-190))

		self.draw_stats(screen)

		pg.display.flip()

	def draw_stats(self, screen):
				# STATS
		screen.blit(self.font20.render('SPEED:', True, WHITE), (screen.get_size()[0]//2-190,screen.get_size()[1]//2-100))
		if self.player.speed / self.player.max_speed == 1:
			speed = self.font20.render(f"{self.player.speed}/{self.player.max_speed}", True, MAXXED)
		else:
			speed = self.font20.render(f"{self.player.speed}/{self.player.max_speed}", True, WHITE)
		screen.blit(speed, (screen.get_size()[0]//2+190-speed.get_width(),screen.get_size()[1]//2-100))


		screen.blit(self.font20.render('REGEN:', True, WHITE), (screen.get_size()[0]//2-190,screen.get_size()[1]//2-75))
		if self.player.regen / self.player.max_regen == 1:
			regen = self.font20.render(f"{self.player.regen}/{self.player.max_regen}", True, MAXXED)
		else:
			regen = self.font20.render(f"{self.player.regen}/{self.player.max_regen}", True, WHITE)
		screen.blit(regen, (screen.get_size()[0]//2+190-regen.get_width(),screen.get_size()[1]//2-75))


		screen.blit(self.font20.render('REGEN RATE:', True, WHITE), (screen.get_size()[0]//2-190,screen.get_size()[1]//2-50))
		if self.player.regen_ticks / self.player.min_regen_ticks == 1:
			regenrate = self.font20.render(f"{self.player.regen_ticks/1000}/{self.player.min_regen_ticks/1000}", True, MAXXED)
		else:
			regenrate = self.font20.render(f"{self.player.regen_ticks/1000}/{self.player.min_regen_ticks/1000}", True, WHITE)
		screen.blit(regenrate, (screen.get_size()[0]//2+190-regenrate.get_width(),screen.get_size()[1]//2-50))


		screen.blit(self.font20.render('HEALTH:', True, WHITE), (screen.get_size()[0]//2-190,screen.get_size()[1]//2-25))
		if self.player.max_health / self.player.max_max_health == 1:
			health = self.font20.render(f"{self.player.max_health}/{self.player.max_max_health}", True, MAXXED)
		else:
			health = self.font20.render(f"{self.player.max_health}/{self.player.max_max_health}", True, WHITE)
		screen.blit(health, (screen.get_size()[0]//2+190-health.get_width(),screen.get_size()[1]//2-25))


		screen.blit(self.font20.render('IMMUNITY:', True, WHITE), (screen.get_size()[0]//2-190,screen.get_size()[1]//2))
		if self.player.immunity_ticks / self.player.max_immunity_ticks == 1:
			immunity = self.font20.render(f"{self.player.immunity_ticks/1000}/{self.player.max_immunity_ticks/1000}", True, MAXXED)
		else:
			immunity = self.font20.render(f"{self.player.immunity_ticks/1000}/{self.player.max_immunity_ticks/1000}", True, WHITE)
		screen.blit(immunity, (screen.get_size()[0]//2+190-immunity.get_width(),screen.get_size()[1]//2))
		

		screen.blit(self.font20.render('DEFENSE:', True, WHITE), (screen.get_size()[0]//2-190,screen.get_size()[1]//2+25))
		if self.player.defense / self.player.max_defense == 1:
			defense = self.font20.render(f"{self.player.defense}/{self.player.max_defense}", True, MAXXED)
		else:
			defense = self.font20.render(f"{self.player.defense}/{self.player.max_defense}", True, WHITE)
		screen.blit(defense, (screen.get_size()[0]//2+190-defense.get_width(),screen.get_size()[1]//2+25))


		screen.blit(self.font20.render('BULLET SPEED:', True, WHITE), (screen.get_size()[0]//2-190,screen.get_size()[1]//2+50))
		if round(self.bullet_speed, 2) / self.bullet_speed_min == 1:
			bulletspeed = self.font20.render(f"{round(self.bullet_speed,2)}/{self.bullet_speed_min}", True, MAXXED)
		else:
			bulletspeed = self.font20.render(f"{round(self.bullet_speed, 2)}/{self.bullet_speed_min}", True, WHITE)
		screen.blit(bulletspeed, (screen.get_size()[0]//2+190-bulletspeed.get_width(),screen.get_size()[1]//2+50))

	def game_over(self, screen):
		# BACKGROUND
		pg.draw.rect(screen, GREY45, (screen.get_size()[0]//2-200, screen.get_size()[1]//2-200, 400,400))

		# TITLE
		pause = self.font.render("GAME OVER!", True, WHITE)
		screen.blit(pause, (screen.get_size()[0]//2 - pause.get_width()//2,screen.get_size()[1]//2-190))

		# POINTS
		score = self.font20.render(f"SCORE: {self.points}", True, WHITE)
		screen.blit(score, (screen.get_size()[0]//2-score.get_width()//2,screen.get_size()[1]//2-125))

		self.draw_stats(screen)
		self.continue_button.draw(screen)

		pg.display.flip()


	def start(self):
		while self.running:
			self.current_time = pg.time.get_ticks()
			self.CLOCK.tick(self.FPS)
			for event in pg.event.get():
				self.handle_event(event)
			if self.in_menu:
				self.draw_menu(self.SCREEN)
			elif self.in_game_over:
				self.game_over(self.SCREEN)
			else:
				self.draw(self.SCREEN)
				keys_pressed = pg.key.get_pressed()
				self.player.move(keys_pressed, self.SCREEN)
	
				# game time
				if self.current_time - self.played_cp > self.played:
					self.played += 1
					self.played_cp = self.current_time + 1000
					if self.player.maxxed:
						self.points += 8 
					self.points += 2

				# increase bullet speed time
				if self.current_time - self.bullet_increase_cp > self.bullet_increase_interval:
					self.bullet_increase_cp = self.current_time
					self.bullet_interval -= 5

				# orb spawn time
				if self.current_time - self.orb_cp > self.orb_ticks:
 					self.orb_cp = self.current_time
 					self.spawn_orb()

if __name__ == '__main__':
	g = Game()
	g.start()