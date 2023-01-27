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
#    [ ♥ ■■■■■ 1 ] [ ♠ ■■■■■ 100 ]
#    [ Kills 11 ]    [ Time 1:30 ]
#


import os
import re
import sys
import time
import random
import asyncio
import datetime
import keyboard
import traceback
from colorama import Fore, Style
from pympler.tracker import SummaryTracker

from entities import *
from rendering import *
from utils import *


# |  ▲▪▫░▒▓█▄▀▌▐•Ꞌꞌꞈ◌○◊ι۞۝֎֍˚˙ʷʬ◄►▲█•●│■   |

class SystemVariables:
	def __init__(self):
		self.start_time = time.time()
		self.start_loop = None

		self.loop = asyncio.get_event_loop()

		if width_in_characters <= 5 and height_in_characters <= 10:
			log("error", "The world is too small. Set width>5 and height>10 in config.", False)
			input()
			exit()

		self.array_map = map_loading(generate_new_map(width_in_characters, height_in_characters))

		self.player = Player(name="Cherry")

		self.infobar = InfoBar(self.player)
		
		self.entities = [self.player]
		self.bullets = []


sysvars = SystemVariables()

os.system(f'mode con:cols={width_in_characters*2} lines={height_in_characters+1}')

async def spawner():
	probability = random.randint(1, 150) if True in [isinstance(i, Bot) for i in sysvars.entities] else random.randint(1, 15)
	if ticks(10) and probability == 1:
		sysvars.entities.append(Bot())

	if ticks(10) and random.randint(1,700) == 1:
		sysvars.entities.append(Torturer())
		

async def bullet_processing():
	sysvars.bullets = [i for i in sysvars.bullets if (i.y > 0 and i.weapon.shooter.IS_FORWARD) or (i.y < height_in_characters-1 and not i.weapon.shooter.IS_FORWARD)]
	for bullet in sysvars.bullets:
		bullet.process()


async def entity_behavior():
	sysvars.entities = [i for i in sysvars.entities if i.health != 0]
	for entity in sysvars.entities:
		entity.move()

		shoot = entity.shoot()
		if shoot is not None:
			sysvars.bullets.append(shoot)

		entity.restore_energy(5)


async def find_collisions():
	for entity in sysvars.entities:
		for bullet in sysvars.bullets:
			if entity.x == bullet.x and entity.y == bullet.y and entity.IS_FRIENDLY != bullet.weapon.shooter.IS_FRIENDLY:
				entity.damage(bullet.weapon.damage)
				if entity.health == 0:
					log("info", f"{bullet.weapon.shooter.name} shot {entity.name}")
					if isinstance(bullet.weapon.shooter, entities.Player): sysvars.infobar.update_kills()
					break


def main():
	global sysvars
	while True:
		if sysvars.start_loop == None or time.time() - sysvars.start_loop >= 1 / ticks_per_second:
			sysvars.start_loop = time.time()
		else: continue
		
		if is_pressed(28) and sysvars.player.health == 0:
			sysvars = SystemVariables()
		if is_pressed(1):
			while True:
				keyboard.wait('esc')
				if is_pressed(1):
					time.sleep(0.3)
					break

		sysvars.infobar.second(sysvars.player)

		tasks = [spawner(), bullet_processing(), entity_behavior(), find_collisions()]
		sysvars.loop.run_until_complete(asyncio.gather(*tasks))

		if ticks(35): sysvars.array_map = map_loading(sysvars.array_map)

		sys.stdout.write(matrix_to_string(objects_loading(sysvars.array_map, sysvars.entities, sysvars.bullets)) + "\n" + sysvars.infobar.structuring(sysvars.player))
		sys.stdout.flush()


if __name__ == '__main__':
	try:
		log("info", "Starting this shit")
		main()
	except Exception:
		sys.stdout.write(traceback.format_exc())
		input("\nPress ENTER to exit.")