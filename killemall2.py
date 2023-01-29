# KILLEMALL
#
# There is a console game about a space wanderer
# that goes through the armada of enemies and 
# thousands of light years.
#
# Coordinates:
#
#         -y
#          ↑
#     -x ←   → +x
#          ↓
#         +y
#
# Information bar
#
#    [ ♥ ■■■■■ 1 ] [ ♠ ■■■■■ 100 ] [Kills: 11] [Time: 30s]
#    
# Symbols
#
#     ▲▪▫░▒▓█▄▀▌▐•Ꞌꞌꞈ◌○◊ι۞۝֎֍˚˙ʷʬ◄►•●│■
#


import os
import sys
import time
import asyncio
import keyboard
import traceback

from entities import Player
from rendering import *
from utils import *
from logic import *


class SystemVariables:
	start_time = time.time()
	start_loop = None
	loop = asyncio.get_event_loop()
	array_map = map_loading(generate_new_map(width_in_characters, height_in_characters))
	projectiles = []


class InfoPanel():
		
	def __init__(self, sv, ec):
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
			return self.result.format(self.tps, max_tps, len(sv.projectiles), len(ec.entities), ec.player.x, ec.player.y, ec.player.weapon.name).replace("\n", "\n    ")
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
			os.system(f'mode con:cols={width_in_characters*2} lines={height_in_characters+1+infopanel.height}')


ec = EntityControl()
sv = SystemVariables()
infopanel = InfoPanel(sv, ec)

window_height_control(infopanel)
infopanel_visible = infopanel.visible

keyboard.on_press_key(46, lambda e: infopanel.toggle_visibility())


async def bullet_processing():
	sv.projectiles = [i for i in sv.projectiles if (i.y > 0 and i.weapon.shooter.IS_FORWARD) or (i.y < height_in_characters-1 and not i.weapon.shooter.IS_FORWARD)]
	for bullet in sv.projectiles:
		bullet.process()


async def find_collisions():
	for entity in ec.entities:
		for projectile in sv.projectiles:
			if entity.x == projectile.x and entity.y == projectile.y and entity.IS_FRIENDLY != projectile.weapon.shooter.IS_FRIENDLY:
				entity.damage(projectile.weapon.damage)
				if entity.health == 0:
					log("info", f"{projectile.weapon.shooter.name} shot {entity.name}")
					if isinstance(projectile.weapon.shooter, Player): ec.player.increment_kills()
					break


def main():
	global sv, ec, infopanel_visible
	while True:
		if sv.start_loop == None or time.time() - sv.start_loop >= 1 / max_tps:
			sv.start_loop = time.time()
			infopanel.note_tick_time()
		else: continue
		
		if keyboard.is_pressed(28) and ec.player.health == 0:
			sv = SystemVariables()
			ec = EntityControl()
		if keyboard.is_pressed(1):
			keyboard.wait('esc')
			if keyboard.is_pressed(1):
				time.sleep(0.3)

		ec.player.increment_seconds()

		tasks = [ec.process(sv), bullet_processing(), find_collisions()]
		sv.loop.run_until_complete(asyncio.gather(*tasks))

		if infopanel_visible != infopanel.visible:
			window_height_control(infopanel)
			infopanel_visible = infopanel.visible

		if ticks(35): sv.array_map = map_loading(sv.array_map)

		sys.stdout.write(matrix_to_string(objects_loading(sv.array_map, ec.entities, sv.projectiles)) + ec.player.infobar_structure() + infopanel.structure())
		sys.stdout.flush()


if __name__ == '__main__':
	try:
		log("info", "Starting this shit")
		main()
	except Exception:
		sys.stdout.write(traceback.format_exc())
		input("\nPress ENTER to exit.")