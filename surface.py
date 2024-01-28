import sys

import pygame as pg
from .logger import *
from .files import *

pg.init()

FONT = {}
FONT_LIST = {}

TOOLTIPS = True

WIDTH = 1900
HEIGHT = 1000
FRAME_X = 10
FRAME_Y = 40
FACTOR = 1

LAYERS = []
SCREEN_OBJECTS = []

messages = {}

window = False


def init__surface(total_size, size, total_layers, version, cursor: bool = True, flags = pg.NOFRAME, title: str = False, image: str = False, show_tooltips: bool = True):
	global WIDTH, HEIGHT, FRAME_X, FRAME_Y, FACTOR, LAYERS, window, screen

	show__tooltips(show_tooltips)

	WIDTH, HEIGHT = size

	title = title or "Naturemag " + str(version)
	image = image or '__RESOURCES__/ntmg.png'

	window = pg.display.set_mode(total_size, flags)
	pg.display.set_caption(title)
	pg.display.set_icon(pg.image.load(image))

	pg.mouse.set_visible(cursor)

	FACTOR = HEIGHT / 1000
	FRAME_X = (total_size[0] - size[0]) // 2
	FRAME_Y = (total_size[1] - size[1]) // 2

	LAYERS = []

	for i in range(total_layers):
		LAYERS.append(ScreenObject(Surface(size)).set((FRAME_X, FRAME_Y), -1))
		SCREEN_OBJECTS.append([])

	return WIDTH, HEIGHT, FRAME_X, FRAME_Y, FACTOR


def init__fonts(colors, msg = False, name = "ntmg", plugin = "naturemag"):
	global FONT, FONT_LIST, messages

	messages = msg

	with open(get__path(plugin + "/data/fonts/" + name + ".font"), 'r') as file:
		FONT_LIST = eval(file.read())

	color_width = 512 / len(colors) * FACTOR

	for n, color in enumerate(colors):
		r = color.r
		g = color.g
		b = color.b
		I_font = Image("fonts/" + name + ".png", plugin = plugin, useFactor = False)
		FONT[map_rgb(color.to_pg_color())] = {}
		for y in range(I_font.size[1]):
			for x in range(I_font.size[0]):
				I_font.surface.set_at((x, y), (r, g, b)
						if I_font.surface.get_at((x, y)) == pg.Color(0, 0, 0) else
					pg.Color(0, 0, 0, 0))

		for letter, value in FONT_LIST.items():
			surface = Surface((FONT_LIST["size"][0], FONT_LIST["size"][1]))
			surface.blit(I_font, (value[0] * -FONT_LIST["size"][0], value[1] * -FONT_LIST["size"][1]))
			surface.letter = letter
			FONT[map_rgb(color.to_pg_color())][letter] = surface

		if messages:
			draw__loading__bar__page(int(n * color_width), description="loading.font")


def map_rgb(color):
	color = eval(str(color))
	if type(color) == tuple:
		color = Color(color[0], color[1], color[2])
	return Surface((0, 0), Color(0, 0, 0, 0)).surface.map_rgb(color.to_pg_color())


def show__tooltips(show_tooltips: bool = True):
	global TOOLTIPS
	TOOLTIPS = show_tooltips



class Color:
	def __init__(self, r: int, g: int, b: int, a: int = 255):
		self.r = r
		self.g = g
		self.b = b
		self.a = a

	def __repr__(self):
		return "Color(" + str(self.r) + ", " + str(self.g) + ", " + str(self.b) + ", " + str(self.a) + ")"

	def __str__(self):
		return self.__repr__()
	
	def to_pg_color(self):
		return pg.Color(self.r, self.g, self.b, self.a)

	
class Position:
	def __init__(self, pos: tuple, size: tuple, center: tuple = (False, False)):
		self.set_pos_size(pos, size, center)

	def __repr__(self):
		return "Position(" + str(self.pos) + ", " + str(self.size) + ", " + str(self.center) + ")"

	def set_pos_size(self, pos: tuple, size: tuple, center: tuple = (False, False)):
		x, y = pos
		self.size = self.width, self.height = size
		self.center = center
		if self.center[0]:
			x = x - size[0] // 2
		if self.center[1]:
			y = y - size[1] // 2
		self.pos = self.x, self.y = x, y
		return self
	
	def set_size(self, size: tuple):
		return self.set_pos_size(self.pos, size, self.center)
	
	def set_pos(self, pos: tuple, center: tuple = (False, False)):
		return self.set_pos_size(pos, self.size, center)


class Surface:
	def __init__(self, size: tuple, color: Color = Color(0, 0, 0, 0), element_list: list = [None]):
		self.surface = pg.Surface(size).convert_alpha()
		self.size = size
		self.fill(color)
		self.set_at = self.surface.set_at
		self.get_at = self.surface.get_at
		self.element_list = []
		for i in element_list:
			if i:
				self.blit(i[0], i[1])

	def __repr__(self):
		return "Surface(" + str(self.size) + ", " + str(self.color) + ", " + str(self.element_list) + ")"

	def fill(self, color: Color):
		if type(color) == tuple:
			color = eval("Color" + str(color))
		self.surface.fill(pg.Color(color.r, color.g, color.b, color.a))
		self.color = color
		return self

	def blit(self, surface, pos: tuple, center: tuple = (False, False)):
		self.element_list.append([surface, self.blit_pg(surface.surface, pos, center)])
		return self

	def blit_pg(self, surface: pg.Surface, pos: tuple, center: tuple = (False, False)):
		if type(pos) != Position:
			pos = Position(pos, (surface.get_width(), surface.get_height()), center)
		self.surface.blit(surface, pos.pos)
		return pos

	def set_alpha(self, alpha: int):
		self.surface.set_alpha(alpha)
		return self

	def fill_alpha(self, color: Color):
		self.set_alpha(color.a)
		color.a = 255
		self.fill(color)
		return self


class ScreenObject(Surface):
	def __init__(self, surface: Surface):
		super().__init__(surface.size, surface.color)
		self.init_surface = surface
		self.position = Position((0, 0), self.size)
		self.finished = False
		try:
			self.screen = LAYERS[2]
			self.layer = 2
		except:
			self.screen = window
			self.layer = -1
		self.blit(surface, (0, 0))

	def __repr__(self):
		return "ScreenObject(" + str(self.init_surface) + ").set(" + str(self.position.pos) + ", " + str(self.layer) + ")"

	def set_pos(self, pos: tuple, center: tuple = (False, False)):
		self.position = Position(pos, self.size, center)
		return self

	def get_surface_pos(self):
		return self.get_pos()

	def get_pos(self):
		if isinstance(self.screen, ScreenObject):
			return Position((self.position.x + self.screen.get_surface_pos().x, self.position.y + self.screen.get_surface_pos().y), self.size)
		else:
			return Position((self.position.x, self.position.y), self.size)

	def get_mouse_collision(self):
		res = self.get_pos().x < pg.mouse.get_pos()[0] < self.get_pos().x + self.size[0] and self.get_pos().y < pg.mouse.get_pos()[1] < self.get_pos().y + self.size[1]
		if isinstance(self.screen, ScreenObject):
			res = res and self.screen.get_mouse_collision()
		return res

	def get_mouse_pos(self):
		return pg.mouse.get_pos()[0] - self.get_surface_pos().x, pg.mouse.get_pos()[1] - self.get_surface_pos().y

	def set_layer(self, layer: int):
		self.layer = layer
		if layer >= 0:
			self.screen = LAYERS[layer]
		else:
			self.screen = window
		return self

	def set(self, pos: tuple, layer: int = 2, center:  tuple = (False, False)):
		self.set_layer(layer)
		self.set_pos(pos, center)
		return self

	def set_pos_screen(self, pos: tuple, screen, center: tuple = (False, False)):
		self.set_layer(screen.layer)
		self.set_pos(pos, center)
		self.screen = screen
		return self


class Button(ScreenObject):
	def __init__(self, image: Surface, chosenImage: Surface = False, alt_text: str = ""):
		super().__init__(image)
		self.image = image
		self.chosenImage = chosenImage or image
		self.surface = self.image.surface
		self.active = False
		self.set_alt_text(alt_text)

	def __repr__(self):
		return "Button(" + str(self.image) + ", " + str(self.chosenImage) + ", '" + self.text_init + "').set(" + str(self.position.pos) + ", " + str(self.layer) + ")"

	def set_alt_text(self, alt_text: str):
		self.text_init = alt_text
		if type(alt_text) == str:
			self.alt_text = ScreenObject(Text(alt_text, color= (255, 255, 255, 255), bg_color=(0, 0, 25, 127)))
		elif isinstance(alt_text, Surface):
			self.alt_text = ScreenObject(alt_text)
		else:
			self.alt_text = False

	def activate(self):
		self.surface = self.chosenImage.surface
		self.active = True
		return self
	
	def deactivate(self):
		self.surface = self.image.surface
		self.active = False
		return self

	def blit_all(self, surface: Surface, pos: tuple, center: tuple = (False, False)):
		self.image.blit(surface, pos, center)
		self.chosenImage.blit(surface, pos, center)
		self.blit(surface, pos, center)
		return self


class ScrollableSurface(ScreenObject):
	def __init__(self, size: tuple, full_size: tuple, color: Color = Color(0, 0, 0, 0), surface_pos: list = [0, 0]):
		self.full_surface = pg.Surface(full_size).convert_alpha()
		self.full_surface.fill((0, 0, 0, 0))
		self.full_size = full_size
		self.surface_pos = surface_pos

		super().__init__(Surface(size))
		self.fill(color)
		self.update()

	def __repr__(self):
		return "ScrollableSurface(" + str(self.size) + ", " + str(self.full_size) + ", " + str(self.color) + ", " + str(self.surface_pos) + ")"

	def blit(self, surface, pos: tuple, center: tuple = (False, False)):
		self.blit_pg(surface.surface, pos, center)
		return self

	def blit_pg(self, surface: pg.Surface, pos: tuple, center: tuple = (False, False)):
		if type(pos) != Position:
			pos = Position(pos, (surface.get_width(), surface.get_height()), center)
		self.full_surface.blit(surface, pos.pos)
		self.update()
		return self

	def get_surface_pos(self):
		if isinstance(self.screen, ScreenObject):
			return Position((self.position.x + self.surface_pos[0] + self.screen.get_pos().x, self.position.y + self.surface_pos[1] + self.screen.get_pos().y), self.size)
		else:
			return Position((self.position.x + self.surface_pos[0] + FRAME_X, self.position.y + self.surface_pos[1] + FRAME_Y), self.size)

	def scroll(self, x: int, y: int):
		if x > 0:
			if -self.surface_pos[0] + x + self.size[0] <= self.full_size[0]:
				self.surface_pos[0] -= x
			else:
				self.surface_pos[0] = -(self.full_size[0] - self.size[0]) if -(self.full_size[0] - self.size[0]) < 0 else 0
		elif x < 0:
			if -self.surface_pos[0] >= -x:
				self.surface_pos[0] -= x
			else:
				self.surface_pos[0] = 0

		if y > 0:
			if -self.surface_pos[1] + y + self.size[1] <= self.full_size[1]:
				self.surface_pos[1] -= y
			else:
				self.surface_pos[1] = -(self.full_size[1] - self.size[1]) if -(self.full_size[1] - self.size[1]) < 0 else 0
		elif y < 0:
			if -self.surface_pos[1] >= -y:
				self.surface_pos[1] -= y
			else:
				self.surface_pos[1] = 0

		self.update()

	def update(self):
		self.surface.blit(self.full_surface, self.surface_pos)


class TextBox(ScrollableSurface):
	def __init__(self, size: tuple, font_size: int = 1, font_color: int = Color(0, 0, 0), bg_color: str = Color(50, 50, 50, 50), init_text: str = ""):
		self.full_size = (int(len(init_text) * FONT_LIST["size"][0] * FACTOR * font_size), int(FONT_LIST["size"][1] * FACTOR * font_size))
		self.size = size
		self.font_size = font_size
		self.font_color = font_color
		self.bg_color = bg_color
		self.text = self.init_text = init_text
		self.active = False
		super().__init__(self.size, self.full_size, self.bg_color)
		self.update_text()

	def input(self, event: pg.event.Event, shift: bool):
		if self.active:
			if event.type == pg.KEYDOWN:
				if event.unicode and event.unicode.isprintable():
					self.text += event.unicode if not shift else event.unicode.upper()
					self.update_text()

	def activate(self):
		self.active = True

	def deactivate(self):
		self.active = False

	def update_text(self):
		self.element_list = []
		self.surface.fill(self.bg_color.to_pg_color())
		s = Text(self.text, self.font_color, font_size = self.font_size)
		self.full_surface = s.surface
		self.full_size = s.size
		print(self.text, self.full_size, self.size)
		self.scroll(self.full_size[0], 0)


IMG_CACHE = {}.copy()

class Image(Surface):
	def __init__(self, path: str, size: tuple = False, plugin: str = "naturemag", alpha: int = 255, direct_path: bool = False, useFactor: bool = True):
		global IMG_CACHE
		self.image = path
		self.plugin = plugin
		self.alpha = alpha
		if not direct_path: path = get__path(plugin + '/images/' + path)
		if size:
			super().__init__(size)
			if (size, path) in IMG_CACHE:
				self.surface = IMG_CACHE[(size, path)]
				print__debug("Load image from cache:", path, size)
			else:
				self.surface = pg.transform.scale(pg.image.load(path), size)
				IMG_CACHE[(size, path)] = self.surface
		else:
			if path in IMG_CACHE:
				surface = IMG_CACHE[path]
				size = (surface.get_width(), surface.get_height())
				super().__init__(size)
				self.surface = IMG_CACHE[path]
				print__debug("Load image from cache: " + path)
			else:
				surface = pg.image.load(path)
				size = (int(FACTOR * surface.get_width()), int(FACTOR * surface.get_height())) if useFactor else (surface.get_width(), surface.get_height())
				super().__init__(size)
				self.surface = pg.transform.scale(surface, size)
				IMG_CACHE[path] = self.surface
		self.set_alpha(alpha)


	def __repr__(self):
		return "Image('" + str(self.image) + "', " + str(self.size) + ", '" + self.plugin + "', " + str(self.alpha) + ")"

'''
class GIFImage(Surface):
	def __init__(self, ):
'''

class Text(Surface):
	def __init__(self, text: str, color: pg.Color = pg.Color(0, 0, 0), bg_color = pg.Color(0, 0, 0, 0), font_size: int = 1):
		global FONT

		self.text = text
		self.element_list = []

		self.font_color = eval(str(color))

		if type(self.font_color) == tuple: self.font_color = Color(self.font_color[0], self.font_color[1], self.font_color[2])

		self.bg_color = bg_color

		self.font_size = font_size = font_size * FACTOR
		size = (int(len(self.text) * FONT_LIST["size"][0] * font_size), int(FONT_LIST["size"][1] * font_size))

		text_surface = Surface((len(self.text) * FONT_LIST["size"][0], FONT_LIST["size"][1]))

		if map_rgb(self.font_color.to_pg_color()) in FONT:
			for n, i in enumerate(self.text):
				text_surface.blit(FONT[map_rgb(self.font_color.to_pg_color())][i], (n * FONT_LIST["size"][0], 0)) \
						if i in FONT_LIST else \
					text_surface.blit(FONT[map_rgb(self.font_color.to_pg_color())]['default'], (n * FONT_LIST["size"][0], 0))
		else:
			for n, i in enumerate(self.text):
				text_surface.blit(FONT[map_rgb((0, 0, 0))][i], (n * FONT_LIST["size"][0], 0)) if i in FONT_LIST else self.blit(FONT[map_rgb((0, 0, 0))]['default'], (n * FONT_LIST["size"][0], 0))
			for y in range(FONT_LIST["size"][1]):
				for x in range(len(self.text) * FONT_LIST["size"][0]):
					text_surface.set_at((x, y), map_rgb(self.font_color.to_pg_color())
							if text_surface.get_at((x, y)) == pg.Color(0, 0, 0) else
						pg.Color(0, 0, 0, 0))

		super().__init__(size, bg_color, element_list = self.element_list)

		self.surface = pg.transform.scale(text_surface.surface, size)

	def __repr__(self):
		return "Text('" + self.text + "', " + str(self.font_color) + ", " + str(self.bg_color) + ", " + str(self.font_size) + ")"


class Enum:
	def __init__(self, **kwargs):
		self.content = {}
		self.set_with_dict(kwargs)

	def __getattr__(self, item):
		try: return self.content[item]
		except: return None

	def set(self, **kwargs):
		self.set_with_dict(kwargs)

	def set_with_dict(self, kwargs: dict):
		for key, item in kwargs.items():
			self.content[key] = item

	def get(self, key: str):
		if key in self.content:
			return self.content[key]
		else:
			print__error("Key " + key + " is not contained in Enum.")
			return None

	def get_all(self):
		return self.content


class Colors(Enum):
	def __init__(self):
		super().__init__()
		self.set(black = Color(0, 0, 0))
		self.set(red = Color(158, 35, 43))
		self.set(green = Color(0, 119, 40))
		self.set(yellow = Color(230, 150, 0))
		self.set(gold = Color(255, 127, 0))
		self.set(purple = Color(100, 0, 200))
		self.set(magenta = Color(200, 0, 200))
		self.set(aqua = Color(0, 200, 200))
		self.set(light_blue = Color(150, 255, 255))
		self.set(light_green = Color(150, 255, 150))
		self.set(gray = Color(127, 127, 127))
		self.set(brown = Color(100, 50, 0))
		self.set(light_brown = Color(150, 100, 50))


COLORS = Colors()


def get__color_tuple(color):
	return (color.r, color.g, color.b, color.a)


def get__screen_objects():
	global SCREEN_OBJECTS
	return SCREEN_OBJECTS


def draw(surface: ScreenObject):
	global SCREEN_OBJECTS
	if isinstance(surface, Button):
		if surface.get_mouse_collision():
			surface.activate()
			SCREEN_OBJECTS[surface.layer].append(surface)
			if surface.alt_text and TOOLTIPS:
				x = pg.mouse.get_pos()[0] - FRAME_X + 10
				y = pg.mouse.get_pos()[1] - FRAME_Y + 10
				if x + surface.alt_text.size[0] > WIDTH:
					x -= surface.alt_text.size[0]
				if y + surface.alt_text.size[1] > HEIGHT:
					y -= surface.alt_text.size[1]
				draw(surface.alt_text.set((x, y), 7))
		else:
			surface.deactivate()
			SCREEN_OBJECTS[surface.layer].append(surface)
	else:
		SCREEN_OBJECTS[surface.layer].append(surface)
	return surface


def fill__screen(color):
	LAYERS[0].fill(color)


def draw__clean(color: Color = Color(0, 0, 0)):
	global LAYERS, SCREEN_OBJECTS
	for screen in LAYERS:
		screen.fill((0, 0, 0, 0))
	SCREEN_OBJECTS = [[], [], [], [], [], [], [], []]
	LAYERS[0].fill(color)


def draw__clean__screen(screen: int = 3):
	global SCREEN_OBJECTS, LAYERS

	SCREEN_OBJECTS[screen].clear()
	if screen != 1: LAYERS[screen].fill(Color(0, 0, 0, 0))


def draw__window():
	global SCREEN_OBJECTS, LAYERS

	for n, i in enumerate(SCREEN_OBJECTS):
		for j in i:
			j.screen.blit(j, j.position.pos)

	for i in LAYERS:
		window.blit(i.surface, (FRAME_X, FRAME_Y))

	pg.display.flip()


def draw__sign(title, description: str = ""):
	T_sign = Surface((int(FACTOR * 600), int(FACTOR * 300)), COLORS.light_brown)
	T_sign.blit(Text(messages[title], font_size=2), (int(300 * FACTOR), int(140 * FACTOR)), (True, True))
	if description: T_sign.blit(Text(messages[description]), (int(300 * FACTOR), int(220 * FACTOR)), (True, True))
	return draw(ScreenObject(T_sign).set((int(WIDTH // 2 - 300 * FACTOR), int(HEIGHT // 2 - 150 * FACTOR)), 2))


def draw__sign__page(title, description: str = ""):
	draw__clean()
	draw__sign(title, description)
	draw__window()


def draw__loading__sign(description: str = ""):
	return draw__sign('loading', description)


def draw__loading__sign__page(description: str = ""):
	draw__clean()
	draw__loading__sign(description)
	draw__window()


def draw__loading__bar(current_width: int, total_width: int = False, height: int = False,
					   pos: tuple = False, center: tuple = (True, False)):
	pos = pos or (WIDTH // 2, int(600 * FACTOR))
	total_width = total_width or int(512 * FACTOR)
	height = height or int(100 * FACTOR)
	x, y = pos
	if center[0]:
		x = x - total_width // 2
	if center[1]:
		y = y - height // 2
	bar = Surface((total_width, height), pg.Color(0, 150, 50))
	progress = Surface((current_width, height), pg.Color(150, 255, 150))
	bar.blit(progress, (0, 0))
	return draw(ScreenObject(bar).set((x, y), 3))


def draw__loading__bar__page(current_width: int, total_width: int = False, height: int = False,
							 pos: tuple = False, center: tuple = (True, False),
							 description: str = ""):
	draw__clean()
	draw__loading__sign(description)
	draw__loading__bar(current_width, total_width, height, pos, center)
	draw__window()


def screenshot(version: str):
	global window
	dateTime = datetime.datetime.now()
	nowTime = dateTime.strftime("%H_%M_%S")
	nowDate = time.strftime('%Y_%m_%d_')
	front = nowDate + str(nowTime)
	cmd.create_dir('__SCREENSHOTS__/' + version)
	pg.image.save(window, '__SCREENSHOTS__/' + version + '/' + front + '.png')
