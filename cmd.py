import glob
import os
import platform
import subprocess
import base64

true = True
false = False

SYSTEM = platform.system()[0]

LINUX = SYSTEM == 'L'
WINDOWS = SYSTEM == 'W'


def get_screen_size():
	import pygame as pg
	pg.init()
	if LINUX:
		try:
			return eval(str(subprocess.check_output(['xprop', '-root', '_NET_WORKAREA'])).split(' = ')[1].split('\\n')[0])[2:4]
		except:
			return pg.display.Info().current_w, pg.display.Info().current_h
	elif WINDOWS:
		return pg.display.Info().current_w, pg.display.Info().current_h



def import_python_module(name: str):
	if LINUX:
		os.system('python3 -m pip install -U --user ' + name)
	elif WINDOWS:
		os.system('py -3 -m pip install -U --user ' + name)


def clear_screen():
	if LINUX:
		os.system('clear')
	elif WINDOWS:
		os.system('cls')


def list_directory(name: str, output_file: str = ""):
	try:
		if LINUX:
			res = os.listdir(name)
		elif WINDOWS:
			res = glob.glob(name.replace('/', '\\'))
	except FileNotFoundError:
		res = ""
	if output_file:
		with open(output_file, "w") as file:
			file.write(str(res))
	return res


def create_dir(name: str):
	if LINUX:
		os.system('mkdir -p "' + name + '">/dev/null')
	elif WINDOWS:
		os.system('mkdir "' + name.replace('/', '\\') + '">nul')

def delete_file(name: str):
	if LINUX:
		os.system('rm "' + name + '"')
	elif WINDOWS:
		os.system('del "' + name.replace('/', '\\') + '"')

def copy_file(name: str, target: str):
	if LINUX:
		os.system('cp "' + name + '" "' + target + '"')
	elif WINDOWS:
		os.system('copy "' + name.replace('/', '\\') + '" "' + target.replace('/', '\\') + '"')


def run_file(name: str):
	if LINUX:
		os.system('"./' + name + '"')
	elif WINDOWS:
		os.system('".\\' + name.replace("/", "\\") + '"')

def open_page(url: str):
	if LINUX:
		os.system('xdg-open "' + url + '"')
	elif WINDOWS:
		os.system('start "' + url + '"')


def base64_to_image(data: str, output_file: str):
	if ";base64," in data: data = data.split(",")[1]

	base64_bytes = data.encode("utf-8")

	image_bytes = base64.decodebytes(base64_bytes)

	with open(output_file, "wb") as file:
		file.write(image_bytes)

	return image_bytes

def image_to_base64(file: str):
	with open(file, 'rb') as file:
		binary_data = file.read()

	base64_bytes = base64.b64encode(binary_data)

	return "data:image/png;base64," + base64_bytes.decode('utf-8')


def recursive_json(json, depth = 1):
	space = "\n" + "  " * depth
	output = ""
	if type(json) == dict:
		first = True
		output += "{"
		for key, item in json.items():
			if first:
				output += space + '"' + key + '": ' + recursive_json(item, depth + 1)
				first = False
			else:
				output += ',' + space + '"' + key + '": ' + recursive_json(item, depth + 1)
		output += space[:-2] + "}"
	elif type(json) == list:
		first = True
		output += "["
		for element in json:
			if first:
				output += space + recursive_json(element, depth + 1)
				first = False
			else:
				output += ',' + space + recursive_json(element, depth + 1)
		output += space[:-2] + "]"
	elif type(json) == str:
		output += space + '"' + json + '"'
	elif type(json) == bool:
		output += space + str(json).lower()
	else:
		output += space + str(json)
	return output

def read_json(name: str):
	with open(name, "r") as file:
		return eval(file.read())

def write_json(json: dict, name: str):
	with open(name, "w") as file:
		file.write(recursive_json(json))
