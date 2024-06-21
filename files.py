#!/bin/python3

import os
import subprocess
from . import cmd

PACKS = ["__RESOURCES__/"]

def init__resource_packs(plugins: list):
	global PACKS
	PACKS = ["__RESOURCES__/"]
	for i in plugins:
		PACKS.append("__PLUGINS__/" + i.name + "/resources/")
	return PACKS

def get__path(name: str):
	for i in PACKS:
		if os.path.exists(i + name):
			return i + name

def get__path__resource(resource):
	return get__path(resource.plugin + '/images/' + resource.type + '/' + resource.name + '.png')

def list__all(path: str, file: str = "/dev/null"):
	result = []
	for i in PACKS:
		try:
			res = cmd.list_directory(i + path, file)
			result.append(res)
		except:
			pass

	res = []
	for i in result:
		for j in i:
			res.append(j)

	with open(file, "w") as file:
		file.write(str(res))
	return res
