#!/bin/python3

import colorama
import time
import datetime
from . import cmd

colorama.init()


def init__logger(log_file):
	global TIME_STAMP, LATEST_LOG, LOG_FILE
	TIME_STAMP = '"[" + time.strftime("%Y-%m-%d, ") + str(datetime.datetime.time(datetime.datetime.now())) + "]"'
	LATEST_LOG = '__LOGS__/latest.log'
	LOG_FILE = log_file
	cmd.create_dir('__LOGS__')
	m = eval(TIME_STAMP) + ": Initialized logger"
	print(m)
	with open(LOG_FILE, "w") as file: file.write(m)
	with open(LATEST_LOG, "w") as file: file.write(m)


def print__info(*output: str):
	m = ''
	for i in output:
		m += str(i) + ' '
	print__basic(eval(TIME_STAMP) + ' [INFO]: ' + m, colorama.Fore.BLUE)


def print__warning(*output: str):
	m = ''
	for i in output:
		m += str(i) + ' '
	print__basic(eval(TIME_STAMP) + ' [WARN]: ' + m, colorama.Fore.YELLOW)


def print__debug(*output: str):
	m = ''
	for i in output:
		m += str(i) + ' '
	print__basic(eval(TIME_STAMP) + ' [DEBUG]: ' + m, colorama.Fore.CYAN)


def print__error(*output: str):
	m = ''
	for i in output:
		m += str(i) + ' '
	print__basic(eval(TIME_STAMP) + ' [ERROR]: ' + m, colorama.Fore.RED)


def print__system(*output: str):
	m = ''
	for i in output:
		m += str(i) + ' '
	print__basic(eval(TIME_STAMP) + m, colorama.Fore.CYAN)


def print__basic(output: str, color: colorama.Fore):
	global LATEST_LOG, LOG_FILE
	output = str(output)
	print(color + output + colorama.Fore.RESET)
	with open(LATEST_LOG, 'r') as file:
		log = file.read()
		log += output + '\n'
	with open(LATEST_LOG, 'w') as file:
		file.write(log)
	with open(LOG_FILE, 'w') as file:
		file.write(log)
