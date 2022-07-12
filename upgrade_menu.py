import pygame as pg
from button import Button
from colors import *
from math import floor
import os

class UpgradeMenu:
	def __init__(self, screen, game):
		self.font = pg.font.Font(os.path.join('assets', 'font', '8bit.ttf'), 24)
		self.font30 = pg.font.Font(os.path.join('assets', 'font', '8bit.ttf'), 30)
		self.font18 = pg.font.Font(os.path.join('assets', 'font', '8bit.ttf'), 18)
		self.buttons = [
		Button(self.font, 'Speed',  (-150,50), vcenter=True, hcenter=True, screen_size=screen.get_size(), command=game.upgrade_speed),
		Button(self.font, 'Luck',   (0,50), vcenter=True, hcenter=True, screen_size=screen.get_size(), command=game.upgrade_luck),
		Button(self.font, 'Magnet', (150,50), vcenter=True, hcenter=True, screen_size=screen.get_size(), command=game.upgrade_magnet),
		Button(self.font, 'Go Back',(0,250), vcenter=True, hcenter=True, screen_size=screen.get_size(), command=game.btn_back_main_menu)
		]



		self.lbl_desc = self.font18.render('', True, WHITE)


	def draw(self, screen, cfg):
		screen.fill(BLACK)
		flag = False


		lbl_speed_p  = self.font.render(f'{cfg.upgrades["speed"]}/{cfg.upgrades_max["speed"]}'  , True, WHITE)
		lbl_luck_p   = self.font.render(f'{cfg.upgrades["luck"]}/{cfg.upgrades_max["luck"]}'  , True, WHITE)
		lbl_magnet_p = self.font.render(f'{cfg.upgrades["magnet"]}/{cfg.upgrades_max["magnet"]}', True, WHITE)

		screen.blit(lbl_speed_p, (screen.get_size()[0]//2-150  - lbl_speed_p.get_width()//2,  370))
		screen.blit(lbl_luck_p, (screen.get_size()[0]//2   - lbl_speed_p.get_width()//2,      370))
		screen.blit(lbl_magnet_p, (screen.get_size()[0]//2+150 - lbl_speed_p.get_width()//2,  370))

		# cost
		lbl_speed_c  = self.font.render(f'{cfg.upgrade_cost["speed"]}'  , True, POINTS)
		lbl_luck_c   = self.font.render(f'{cfg.upgrade_cost["luck"]}'  , True,  POINTS)
		lbl_magnet_c = self.font.render(f'{cfg.upgrade_cost["magnet"]}', True,  POINTS)

		if not cfg.is_maxxed['speed']:
			screen.blit(lbl_speed_c, (screen.get_size()[0]//2-150  - lbl_speed_c.get_width()//2,  300))
		if not cfg.is_maxxed['luck']:
			screen.blit(lbl_luck_c, (screen.get_size()[0]//2   - lbl_luck_c.get_width()//2,      300))
		if not cfg.is_maxxed['magnet']:
			screen.blit(lbl_magnet_c, (screen.get_size()[0]//2+150 - lbl_magnet_c.get_width()//2,  300))

		for button in self.buttons:
			button.draw(screen)
			if button.hover:
				if button is self.buttons[0]:
					self.lbl_desc = self.font18.render('Permanently increase your speed', True, WHITE)
					flag = True
				elif button is self.buttons[1]:
					self.lbl_desc = self.font18.render('Increase the chance of getting the orbs you need', True, WHITE)
					flag = True
				elif button is self.buttons[2]:
					self.lbl_desc = self.font18.render('Orbs will get attracted to you when you get close to them', True, WHITE)
					flag = True


		lbl_mp0 = self.font18.render('Mutation Points', True, WHITE)
		lbl_mp1 = self.font30.render(str(cfg.mutation_points), True, POINTS)
		screen.blit(lbl_mp0, (screen.get_size()[0]//2-lbl_mp0.get_width()//2, 180))
		screen.blit(lbl_mp1, (screen.get_size()[0]//2-lbl_mp1.get_width()//2, 140))
		if flag:
			pg.draw.rect(screen, WHITE, (screen.get_size()[0]//2-self.lbl_desc.get_width()//2-7, screen.get_size()[1]//2+125-7, self.lbl_desc.get_width()+10, self.lbl_desc.get_height()+8), 2 )
			screen.blit(self.lbl_desc, (screen.get_size()[0]//2-self.lbl_desc.get_width()//2, screen.get_size()[1]//2+125))
		pg.display.flip()

	def button_click(self):
		for button in self.buttons:
			if button.hover:
				button.click()
