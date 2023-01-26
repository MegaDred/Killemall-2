import time

from enum import Enum
from utils import width_in_characters, height_in_characters, ticks

class InfoBar:
    def __init__(self, player):
        self.kills = 0
        self.seconds = 0

    def structuring(self, player):
    
        hit_points = '■'*round(player.health/(player.MAX_HEALTH/5))
        enrg_points = '■'*round(player.energy/(player.MAX_ENERGY/5))

        health = f"[ ♥ {hit_points}{' '*(5-len(hit_points))} {player.health} ]"
        energy = f"[ ♠ {enrg_points}{' '*(5-len(enrg_points))} {player.energy} ]"
        kills = f"[Kills: {self.kills}]"

        return f"{health} {energy} {kills} [Time: {self.seconds}s]"


    def update_kills(self):
        self.kills += 1

    def second(self, player):
        if player.health != 0 and ticks(1): 
            self.seconds += 1


class Navigate:
    def __init__(self):

        self.area_top_border = 0
        self.area_bottom_border = height_in_characters
        self.area_right_border = width_in_characters
        self.area_left_border = 0

        self.x = 0
        self.y = 0

    def up(self):
        if self.y - 1 >= self.area_top_border:
            self.y -= 1

    def down(self):
        if self.y + 1 <= self.area_bottom_border:
            self.y += 1 

    def right(self):
        if self.x + 1 <= self.area_right_border:
            self.x += 1 

    def left(self):
        if self.x - 1 >= self.area_left_border:
            self.x -= 1

    def tp(self, x, y):
        if x in range(self.area_left_border, self.area_right_border) and y in range(self.area_top_border, self.area_bottom_border):
            self.x = x
            self.y = y