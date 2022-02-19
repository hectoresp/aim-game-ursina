try:
    from ursina import *
    from point import Point
    from score import *
    from menu import MenuButton
    from player import Player
    from timeit import default_timer
    import pickle
except ModuleNotFoundError:
    print("Installing required modules...")
    from os import system
    system("python -m pip install -r requirements.txt")

player = Player()


def start():
	for i in main_menu.buttons:
		i.enabled = False
	player.start = True

def resume():
	p.enabled = True
	for i in pause_menu.buttons:
		i.enabled = False

def set_velocity():
	p.velocity = velocity_slider.value

def set_size():
	p.scale = size_slider.value
	p.scaled = p.scale

def quit():
	data_file = open('game_data.txt', 'wb')
	data = [str(velocity_slider.value), str(size_slider.value)]
	pickle.dump(data, data_file)
	data_file.close()

	application.quit()


def update():	

	if player.start:

		p.enabled = True
		setattr(Timer, 'start_timer', True)
		player.start = False
	if getattr(Timer, 'start_timer'):
		setattr(Timer, 'start', default_timer())
		setattr(Timer, 'start_timer', False)
		setattr(Timer, 'timer_started', True)
	if getattr(Timer, 'timer_started'):
		value = default_timer() - getattr(Timer, 'start')
		value = str(value).replace('.', ' ')
		value = value.split()
		setattr(Timer, 'time', value[0]) 

	time = str(getattr(Timer, 'time'))
	score.text = f'Score: ' + str(getattr(Score, 'score_number'))
	missed.text = f'Missed: ' + str(getattr(Missed, 'missed_number'))
	timer.text = f'Time: ' + str(getattr(Timer, 'time'))

def input(key):
	if key == 'escape':
		for i in pause_menu.buttons:
			i.enabled = True
		p.enabled = False

app = Ursina(title = 'Aim Trainer', borderless = False)

try:
	data_file = open('game_data.txt', 'rb')
	velocity_value, size_value = pickle.load(data_file)
	data_file.close()
except FileNotFoundError as e:
	print('game_data.txt - ' + str(e))
	velocity_value = .04
	size_value = .1


score = Score('')
missed = Missed('')
timer = Timer('')

button_spacing = .075 * 1.25
menu_parent = Entity(parent = camera.ui, y = .15)
main_menu = Entity(parent = menu_parent)
settings_menu = Entity(parent = menu_parent)
pause_menu = Entity(parent = menu_parent)

state_handler = Animator({
    'main_menu' : main_menu,
    'settings_menu' : settings_menu,
    'pause_menu' : pause_menu
    }
)

main_menu.buttons = [
    MenuButton('Play', on_click = start),
    MenuButton('Settings', on_click = Func(setattr, state_handler, 'state', 'settings_menu')),
    MenuButton('Quit', on_click = Sequence(Wait(.01), Func(quit))),
]

for i, e in enumerate(main_menu.buttons):
    e.parent = main_menu
    e.eternal = True
    e.y = -i * button_spacing

pause_menu.buttons = [
	MenuButton('Resume', on_click = resume),
    MenuButton('Settings', on_click = Func(setattr, state_handler, 'state', 'settings_menu')),
    MenuButton('Quit', on_click = Sequence(Wait(.01), Func(quit)))
]

for i, e in enumerate(pause_menu.buttons):
    e.parent = main_menu
    e.eternal = True
    e.y = -i * button_spacing
    e.enabled = False


settings_menu.back = MenuButton('Back', parent = settings_menu, y = -.25, on_click = Func(setattr, state_handler, 'state', 'main_menu'))
size_slider = Slider(text = 'Circle Spawn Size', min = .1, max = 2, dynamic = True, value = float(size_value), on_value_changed = set_size, parent = settings_menu, x = -.22, y = -.1)
velocity_slider = Slider(text = 'Velocity', min = 0.001, max = 5, parent = settings_menu, x = -.22, dynamic = True, value = float(velocity_value), on_value_changed = set_velocity, ignore_paused = True)

p = Point(size_slider.value)
p.enabled = False

app.run()
