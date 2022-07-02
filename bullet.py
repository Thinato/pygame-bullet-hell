import pygame as pg
from colors import *

class Bullet:
	def __init__(self, pos, size, directions, speed):
		self.color = RED
		self.rect = pg.Rect(pos, size)
		self.directions = directions
		self.speed = speed

	def draw(self, screen):
		pg.draw.rect(screen, self.color, self.rect)

	def move(self):
		for d in self.directions:
			if d == 0:
				self.rect.x += self.speed
			elif d == 1:
				self.rect.y += self.speed
			elif d == 2:
				self.rect.x -= self.speed
			elif d == 3:
				self.rect.y -= self.speed
