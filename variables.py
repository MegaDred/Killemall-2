import sys
import time
import traceback

from utils import get_config, get_config_value, log
from entities import Player


start_time = time.time()
start_loop = None

main_config = get_config("./configs/main.json")
mobs_config = get_config("./configs/mobs.json")
player_config = get_config("./configs/player.json")

ticks_per_second = get_config_value(main_config, ["ticks_per_second"], 100)
width_in_characters = get_config_value(main_config, ["width_in_characters"], 30)
height_in_characters = get_config_value(main_config, ["height_in_characters"], 70)

if not (width_in_characters >= 5 and height_in_characters >= 10):
    log("error", "The world is too small.")
    input()
    exit()

player_zone_x = (1, width_in_characters-1)
player_zone_y = (int(height_in_characters/3)*2, height_in_characters-1)

array_map = []

player = Player("Cherry", 1, 100, 40, int(width_in_characters/2), int((player_zone_y[0]+player_zone_y[1])/2), "▲")
entities = [player]
bullets = []