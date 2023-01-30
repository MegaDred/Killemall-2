import os
import re
import json
import pytz
import time
import random
import datetime
import traceback


player = None
entities = None
projectiles = None

max_tps = 60
width_in_characters = 30
height_in_characters = 45


def randbool(probability:float=0.5):
    if probability >= 0 and probability <= 1:
        return random.random() <= probability
    else:
        raise ValueError("Probability must be float from 0 to 1")


def msk(format:str="%Y-%m-%d %H:%M:%S", timestamp:int=None) -> str:
    if timestamp is None: return datetime.datetime.now().astimezone(pytz.timezone('Europe/Moscow')).strftime(format)
    else: return datetime.datetime.fromtimestamp(timestamp).astimezone(pytz.timezone('Europe/Moscow')).strftime(format)


def log(level:str, text: str) -> None:  # levels: info, warn, error
    now_log = msk('%Y-%m-%d %H:%M:%S')
    if len(os.listdir(os.getcwd())) != 0:
        latest_log = os.listdir(os.getcwd())[-1]
    else: latest_log = None
    number = int(latest_log.split('_')[1][:-4]) + 1 if latest_log is not None and len(latest_log) >= 16 and re.search(msk('%Y-%m-%d') + r"_[0-9]+\.log", latest_log) else 1
    now_filename = msk('%Y-%m-%d_' + str(number))
    if not os.path.exists(f"logs"):
        os.mkdir("logs")
    if not os.path.exists(f"logs/{now_filename}.log"):
        with open(f"logs/{now_filename}.log", "w", encoding="utf8") as new: pass
    with open(f"logs/{now_filename}.log", "a", encoding="utf8") as logs:
        logs.write(str(f"[{now_log}] [{level.upper()}] {text}\n"))


def get_config(path: str) -> dict:
    try:
        with open(path, "r") as file:
            return json.loads(file.read())
    except FileNotFoundError:
        log("error", f'"{path}" not found')
        return None
    except json.JSONDecodeError:
        log("error", f'JSONDecoderError in "{path}"')
        return None
    except Exception:
        log("error", "get_config: " + traceback.format_exc())
        return None
        

def get_config_value(config:dict, path:list, default):
    try:
        for i in path:
            config = config[i]
        return config
    except: return default

    
def is_matrix(object:list[list]):
    row_length = None
    for i in object:
        if row_length != None:
            if row_length != len(i):
                raise ValueError("value must be a matrix")
        else:
            row_length = len(i)
    return row_length


config = get_config("./config.json")

sandbox_mode = get_config_value(config, ["sandbox_mode"], False)


def ticks(amount_of_ticks:int):
    if amount_of_ticks > max_tps: amount_of_ticks = max_tps
    second = time.time()
    if int(((second - int(second)) + (1/max_tps)) / (1/max_tps)) % ((max_tps+1)/amount_of_ticks) <= 1:
        return True
    else: return False

def window_height_control(infopanel):
    if infopanel.visible: os.system(f'mode con:cols={width_in_characters*2} lines={height_in_characters+1+infopanel.height}')		
    else: os.system(f'mode con:cols={width_in_characters*2} lines={height_in_characters+1}')


class InfoPanel():
		
	def __init__(self):
		self.visible = False
		self.second = time.time()
		self.ticks = 0
		self.ticks_per_split_second = []
		self.tps = 0

		self.result = "\n\nTPS & FPS: {0}/{1}\n\nX: {4}, Y: {5}\nWeapon: {6}\n\nProjectiles: {2}\nEntities: {3}\n"
		self.height = self.result.count("\n")
		
	def structure(self):
		if self.visible:
			if ticks(10):
				self.tps = 0
				for i in self.ticks_per_split_second:
					self.tps += i
			return self.result.format(self.tps, max_tps, len(projectiles), len(entities), player.x, player.y, player.weapon.name).replace("\n", "\n    ")
		else:
			return ""
	
	def note_tick_time(self):
		if self.visible:
			if time.time() > self.second+0.5:
				if len(self.ticks_per_split_second) >= 2:
					self.ticks_per_split_second.pop(0)
				self.ticks_per_split_second.append(self.ticks)
				self.ticks = 0
				self.second = time.time()
			self.ticks += 1

	def toggle_visibility(self):
		if self.visible:
			self.visible = False
			os.system(f'mode con:cols={width_in_characters*2} lines={height_in_characters+1}')		
		else:
			self.visible = True
			os.system(f'mode con:cols={width_in_characters*2} lines={height_in_characters+1+self.height}')


class Navigate:

    top_border = 0
    bottom_border = height_in_characters
    right_border = width_in_characters
    left_border = 0 

    def __init__(self):
        self.x = 0
        self.y = 0

    def up(self):
        if not self.is_in_permitted_area() or (self.top_border is None or self.y - 1 >= self.top_border):
            self.y -= 1

    def down(self):
        if not self.is_in_permitted_area() or (self.bottom_border is None or self.y + 1 <= self.bottom_border):
            self.y += 1

    def right(self):
        if not self.is_in_permitted_area() or (self.right_border is None or self.x + 1 <= self.right_border):
            self.x += 1

    def left(self):
        if not self.is_in_permitted_area() or (self.left_border is None or self.x - 1 >= self.left_border):
            self.x -= 1

    def tp(self, x, y):
        if x in range(self.left_border, self.right_border) and y in range(self.top_border, self.bottom_border):
            self.x = x
            self.y = y

    def is_in_permitted_area(self):
        if not (self.top_border is None or self.y >= self.top_border): return False
        if not (self.bottom_border is None or self.y <= self.bottom_border): return False
        if not (self.right_border is None or self.x <= self.right_border): return False
        if not (self.left_border is None or self.x >= self.left_border): return False
        return True