from ursina import *
from timeit import default_timer
from player import Player

class Score(Text):
	def __init__(self, text = 'Score: 0'):
		super().__init__(
			text = text,
			position = (-.86,.47),
			scale = 1
			)
	score_number = 0

class Missed(Text):
	def __init__(self, text = 'Missed: 0'):
		super().__init__(
			text = text,
			position = (-.86,.43),
			scale = 1
			)

	missed_number = 0

class Timer(Text):
	def __init__(self, text = 'Time: 0'):
		super().__init__(
			text = text,
			position = (-.86,.39),
			scale = 1
			)
	time = 0
	start_timer = False
	start = 0.0
	timer_started = False