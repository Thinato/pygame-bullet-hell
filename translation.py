import pickle
import os

class Translation:
	def __init__(self, lang=None):
		self.lang = {
		'lang_name'		: '',
		'start game'	: 'start game',
		'upgrades'		: 'upgrades',
		'options'		: 'options',
		'exit'			: 'exit',
		'continue'		: 'continue',
		'game over'		: 'game over',
		'speed+'		: 'speed+',
		'regen+'		: 'regen+',
		'regen rate+'	: 'regen rate+',
		'health+'		: 'health+',
		'immunity+'		: 'immunity+',
		'defense+'		: 'defense+',
		'bullet speed-'	: 'bullet speed-',
		'score'			: 'score',
		'pause'			: 'pause',
		'speed'			: 'speed',
		'luck'			: 'luck',
		'magnet'		: 'magnet'}
		if lang is not None:
			self.load(lang)

	def load(self, lang_name):
		file = open(os.path.join('languages', lang_name), 'rb')
		self.lang = pickle.load(file)
		file.close()

	def __str__(self):
		return f'''
		{self.lang}'''

	def save(self, lang_name):
		self.lang['lang_name'] = lang_name
		file = open(os.path.join('languages', lang_name), 'wb')
		pickle.dump(self.lang, file)
		file.close()
'''
english = Translation()
english.save('en-US')

portuguese = Translation()
portuguese.lang['lang_name'		] = 'pt-BR'
portuguese.lang['start_game'	] = 'iniciar jogo'
portuguese.lang['upgrades'		] = 'melhorias'
portuguese.lang['options'		] = 'opcoes'
portuguese.lang['exit'			] = 'sair'
portuguese.lang['continue'		] = 'continuar'
portuguese.lang['game over'		] = 'fim de jogo'
portuguese.lang['speed+'		] = 'velocidade+'
portuguese.lang['regen+'		] = 'regen+'
portuguese.lang['regen rate+'	] = 'taxa de regen+'
portuguese.lang['health+'		] = 'saude+'
portuguese.lang['immunity+'		] = 'imunidade+'
portuguese.lang['defense+'		] = 'defesa+'
portuguese.lang['bullet speed-' ] = 'velocidade do tiro-'
portuguese.lang['score' 		] = 'pontuacao'
portuguese.lang['pause' 		] = 'pausa'
portuguese.save('pt-BR')
print(portuguese)'''