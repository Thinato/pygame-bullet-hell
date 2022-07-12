import pygame as pg
from colors import *


class Button:
	def __init__(self, font, text, pos, hcenter=False, vcenter=False, screen_size=None, command=None):
		self.color = BUTTON_COLOR
		self.color_hover = BUTTON_HOVER
		self.font = font
		self.text = text
		temp = font.render(self.text, True, self.color)
		a, b = pos[0], pos[1]
		if hcenter:
			a += screen_size[0]//2 - temp.get_width()//2
		if vcenter:
			b += screen_size[1]//2 - temp.get_height()//2

		self.pos = (a,b)
		self.size = (temp.get_width(), temp.get_height())

		self.rect = pg.Rect(self.pos, self.size)
		self.hover = False

		self.command = command

	def draw(self, screen):
		if self.rect.collidepoint(pg.mouse.get_pos()):
			self.hover = True
			screen.blit(self.font.render(self.text, True, self.color_hover), self.pos)
		else:
			self.hover = False
			screen.blit(self.font.render(self.text, True, self.color), self.pos)

	def click(self):
		if self.command is None:
			print('command is none')
			return
		self.command()


