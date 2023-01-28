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
#     ▲▪▫░▒▓█▄▀▌▐•Ꞌꞌꞈ◌○◊ι۞۝֎֍˚˙ʷʬ◄►▲█•●│■
#


import os
import sys
import time
import asyncio
import traceback

from entities import *
from rendering import *
from utils import *
from logic import *


class SystemVariables:
	start_time = time.time()
	start_loop = None
	loop = asyncio.get_event_loop()
	array_map = map_loading(generate_new_map(width_in_characters, height_in_characters))
	bullets = []


os.system(f'mode con:cols={width_in_characters*2} lines={height_in_characters+1}')

ec = EntityControl()
sv = SystemVariables()
		

async def bullet_processing():
	sv.bullets = [i for i in sv.bullets if (i.y > 0 and i.weapon.shooter.IS_FORWARD) or (i.y < height_in_characters-1 and not i.weapon.shooter.IS_FORWARD)]
	for bullet in sv.bullets:
		bullet.process()


async def find_collisions():
	for entity in ec.entities:
		for bullet in sv.bullets:
			if entity.x == bullet.x and entity.y == bullet.y and entity.IS_FRIENDLY != bullet.weapon.shooter.IS_FRIENDLY:
				entity.damage(bullet.weapon.damage)
				if entity.health == 0:
					log("info", f"{bullet.weapon.shooter.name} shot {entity.name}")
					if isinstance(bullet.weapon.shooter, Player): ec.player.increment_kills()
					break


def main():
	global sv, ec
	while True:
		if sv.start_loop == None or time.time() - sv.start_loop >= 1 / ticks_per_second:
			sv.start_loop = time.time()
		else: continue
		
		if is_pressed(28) and ec.player.health == 0:
			sv = SystemVariables()
			ec = EntityControl()
		if is_pressed(1):
			keyboard.wait('esc')
			if is_pressed(1):
				time.sleep(0.3)

		ec.player.increment_seconds()

		tasks = [ec.process(sv), bullet_processing(), find_collisions()]
		sv.loop.run_until_complete(asyncio.gather(*tasks))

		if ticks(35): sv.array_map = map_loading(sv.array_map)

		sys.stdout.write(matrix_to_string(objects_loading(sv.array_map, ec.entities, sv.bullets)) + "\n" + ec.player.infobar_structure())
		sys.stdout.flush()


if __name__ == '__main__':
	try:
		log("info", "Starting this shit")
		main()
	except Exception:
		sys.stdout.write(traceback.format_exc())
		input("\nPress ENTER to exit.")