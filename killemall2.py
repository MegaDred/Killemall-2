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

from entities import *
from rendering import *
from utils import *


# |  ▲▪▫░▒▓█▄▀▌▐•Ꞌꞌꞈ◌○◊ι۞۝֎֍˚˙ʷʬ◄►▲█•●   |


class SystemVariables:
	def __init__(self):
		self.start_time = time.time()
		self.start_loop = None

		if width_in_characters <= 5 and height_in_characters <= 10:
			log("error", "The world is too small. Set width>5 and height>10 in config.", False)
			input()
			exit()

		self.array_map = map_loading(generate_new_map(width_in_characters, height_in_characters))

		self.player = Player(
		    name="Cherry", 
			health=1, 
			energy=100, 
			speed=40,
	      	skin=f"▲",
		)
		
		self.entities = [self.player]
		self.bullets = []


SV = SystemVariables()

os.system(f'mode con:cols={width_in_characters*2} lines={height_in_characters}')

async def spawner():
	probability = random.randint(1, 150) if True in [isinstance(i, Bot) for i in SV.entities] else random.randint(1, 15)
	if ticks(10) and probability == 1:
		SV.entities.append(Bot(
			name=f"Bot{random.randint(100,999)}",
			health=1,
			energy=100,
			speed=20,
			skin=f"◊"
		))

	if ticks(10) and random.randint(1,700) == 1:
		SV.entities.append(Torturer(
			name=f"Torturer{random.randint(100,999)}",
			health=1,
			energy=100,
			speed=20,
			skin=f"█"
		))


async def bullet_processing():
	SV.bullets = [i for i in SV.bullets if (i.y > 0 and i.weapon.shooter.IS_FORWARD) or (i.y < height_in_characters-1 and not i.weapon.shooter.IS_FORWARD)]
	for bullet in SV.bullets:
		bullet.process()


async def entity_behavior():
	SV.entities = [i for i in SV.entities if i.health != 0]
	for entity in SV.entities:
		entity.move()

		shoot = entity.shoot()
		if shoot is not None:
			SV.bullets.append(shoot)


async def find_collisions():
	for entity in SV.entities:
		for bullet in SV.bullets:
			if entity.x == bullet.x and entity.y == bullet.y and entity.IS_FRIENDLY != bullet.weapon.shooter.IS_FRIENDLY:
				entity.damage(bullet.weapon.damage)
				if entity.health == 0:
					log("info", f"{bullet.weapon.shooter.name} shot {entity.name}")
					break


async def key_check():
	global SV
	keyboard.hook(lambda e: None)
	if 28 in keyboard._pressed_events.keys() and SV.player.health == 0:
		SV = SystemVariables()


def main():
	
	while True:
		if SV.start_loop == None or time.time() - SV.start_loop >= 1 / ticks_per_second:
			SV.start_loop = time.time()
		else: continue
		
		loop = asyncio.get_event_loop()
		tasks = [spawner(), bullet_processing(), entity_behavior(), find_collisions(), key_check()]
		loop.run_until_complete(asyncio.gather(*tasks))

		if ticks(35): SV.array_map = map_loading(SV.array_map)

		sys.stdout.write(matrix_to_string(objects_loading(SV.array_map, SV.entities, SV.bullets)))
		sys.stdout.flush()


if __name__ == '__main__':
	try:
		log("info", "Starting this shit")
		main()
	except Exception:
		sys.stdout.write(traceback.format_exc())
		input("\nPress ENTER to exit.")