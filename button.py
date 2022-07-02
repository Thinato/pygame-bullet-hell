import pygame as pg
from colors import *


class Button:
	def __init__(self, font, text, pos):
		self.color = BUTTON_COLOR
		self.color_hover = BUTTON_HOVER
		self.font = font
		self.pos = pos
		self.text = text
		temp = font.render(self.text, True, self.color)
		self.size = (temp.get_width(), temp.get_height())
		self.rect = pg.Rect(pos, self.size)
		self.hover = False

	def draw(self, screen):
		if self.rect.collidepoint(pg.mouse.get_pos()):
			self.hover = True
			screen.blit(self.font.render(self.text, True, self.color_hover), self.pos)
		else:
			self.hover = False
			screen.blit(self.font.render(self.text, True, self.color), self.pos)


