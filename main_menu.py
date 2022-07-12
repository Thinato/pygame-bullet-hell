import pygame as pg
from button import Button
from colors import *
import os
import sys


class MainMenu:
	def __init__(self, screen, game):
		self.lang = game.lang
		self.font = pg.font.Font(os.path.join('assets', 'font', '8bit.ttf'), 24)
		self.buttons = [ Button(self.font, self.lang.lang['start game'], (0,0), vcenter=True, hcenter=True, screen_size=screen.get_size(), command=game.btn_startgame ),
						 Button(self.font, self.lang.lang['upgrades'], (0, 36), vcenter=True,hcenter=True, screen_size=screen.get_size(), command=game.btn_upgrade ),
						 Button(self.font, self.lang.lang['options'], (0, 72), vcenter=True,hcenter=True, screen_size=screen.get_size() ),
						 Button(self.font, self.lang.lang['exit'], (0, 108), vcenter=True,hcenter=True, screen_size=screen.get_size(), command=self.btn_exit ) ]
		self.lbl_version = self.font.render(game.version, True, WHITE)
		
	
	def draw(self, screen):
		screen.fill(BLACK)
		for button in self.buttons:
			button.draw(screen)

		screen.blit(self.lbl_version, (screen.get_size()[0]-self.lbl_version.get_width()-5, screen.get_size()[1]-self.lbl_version.get_height()))

		pg.display.flip()

	def btn_exit(self):
		sys.exit()
		pg.quit()


	def button_click(self):
		for button in self.buttons:
			if button.hover:
				button.click()




