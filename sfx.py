import pygame as pg
import os

pg.mixer.init()

player_hit = pg.mixer.Sound(os.path.join('assets', 'sfx', 'hit.wav'))
player_death = pg.mixer.Sound(os.path.join('assets', 'sfx', 'death.wav'))
player_teleport = pg.mixer.Sound(os.path.join('assets', 'sfx', 'player_teleport.wav'))
player_evolve = pg.mixer.Sound(os.path.join('assets', 'sfx', 'player_evolve.wav'))
orb_pick = pg.mixer.Sound(os.path.join('assets', 'sfx', 'orb_pick.wav'))
orb_spawn = pg.mixer.Sound(os.path.join('assets', 'sfx', 'orb_spawn.wav'))
shoot = pg.mixer.Sound(os.path.join('assets', 'sfx', 'shoot.wav'))