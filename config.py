import pickle
from math import floor

class Config:
	def __init__(self):
		self.upgrades = {'speed':1, 'luck':0, 'magnet':0}
		self.upgrades_max = {'speed':3, 'luck':3, 'magnet':3}
		self.is_maxxed = {'speed':False, 'luck':False, 'magnet':False}
		self.upgrade_cost = {'speed':0, 'luck':0, 'magnet':0}

		self.lang = 'en-US'

		self.show_info = False

		self.mutation_points = 0
		self.mute_sfx = False
		self.mute_music = False
		self.update_cost()


	def update_cost(self):
		self.upgrade_cost['speed'] = self.get_cost(self.upgrades['speed'])
		self.upgrade_cost['luck'] = self.get_cost(self.upgrades['luck'])
		self.upgrade_cost['magnet'] = self.get_cost(self.upgrades['magnet'])

	def get_cost(self, upgrade):
		return int(floor(90*(1.6**(upgrade)))*10)

	def check_max(self):
		if self.upgrades['speed'] / self.upgrades_max['speed'] == 1:
			self.is_maxxed['speed'] = True
		if self.upgrades['luck'] / self.upgrades_max['luck'] == 1:
			self.is_maxxed['luck'] = True
		if self.upgrades['magnet'] / self.upgrades_max['magnet'] == 1:
			self.is_maxxed['magnet'] = True


if __name__ == '__main__':
	cfg = Config()
	file = open('cfg', 'wb')
	pickle.dump(cfg, file)
	file.close()