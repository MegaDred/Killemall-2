# !/usr/bin/python
# -*- coding: utf-8 -*-

#
# KILLEMALL 2
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

from entities import *
from rendering import *


start_time = 0
start_loop = None

utils.player = Player(name="Cherry")
utils.entities = [utils.player]
utils.projectiles = []

infopanel = utils.InfoPanel()


utils.window_height_control(infopanel)
infopanel_visible = infopanel.visible

keyboard.on_release_key(46, lambda e: infopanel.toggle_visibility())


async def bullet_processing():
	utils.projectiles = [i for i in utils.projectiles if (i.y > 0 and i.weapon.shooter.IS_FORWARD) or (i.y < utils.height_in_characters-1 and not i.weapon.shooter.IS_FORWARD)]
	for bullet in utils.projectiles:
		bullet.process()


async def find_collisions():
	for entity in utils.entities:
		for projectile in utils.projectiles:
			if entity.x == projectile.x and entity.y == projectile.y and entity.IS_FRIENDLY != projectile.weapon.shooter.IS_FRIENDLY:
				entity.damage(projectile.weapon.damage)
				if entity.health == 0:
					utils.log("info", f"{projectile.weapon.shooter.name} shot {entity.name}")
					if isinstance(projectile.weapon.shooter, Player): utils.player.increment_kills()
					break

async def entity_control():
	utils.player.increment_seconds()

	utils.entities = [i for i in utils.entities if i.health != 0]

	if not utils.sandbox_mode:
		for entity in EnumEntities:
			if entity.value.spawn_roulete():
				utils.entities.append(entity.value())
	else:
		if ticks(4):
			for entity in EnumEntities:
				if entity.value.spawn_forcibly():
					utils.entities.append(entity.value())

	for entity in utils.entities:
		entity.behavior()


def main():
	global infopanel_visible, loop, array_map, start_loop, start_time
	while True:
		if start_loop == None or time.time() - start_loop >= 1 / utils.max_tps:
			start_loop = time.time()
			infopanel.note_tick_time()
		else: continue
		
		if (keyboard.is_pressed(28) and utils.player.health == 0) or start_time == 0:
			start_time = time.time()
			start_loop = None
			loop = asyncio.get_event_loop()
			array_map = Rendering.generate_new_map(utils.width_in_characters, utils.height_in_characters)
			utils.player = Player(name="Cherry")
			utils.entities = [utils.player]
			utils.projectiles = []
		if keyboard.is_pressed(1):
			keyboard.wait('esc')
			if keyboard.is_pressed(1):
				time.sleep(0.3)

		tasks = (
			entity_control(), 
		  	bullet_processing(), 
		    find_collisions()
		)
		
		loop.run_until_complete(asyncio.gather(*tasks))

		if infopanel_visible != infopanel.visible:
			utils.window_height_control(infopanel)
			infopanel_visible = infopanel.visible

		sys.stdout.write(Rendering.new_frame() + utils.player.infobar_structure() + infopanel.structure())
		sys.stdout.flush()


if __name__ == '__main__':
	try:
		utils.log("info", "--- Starting this shit ---")
		main()
	except Exception:
		sys.stdout.write(traceback.format_exc())
		input("\nPress ENTER to exit.")