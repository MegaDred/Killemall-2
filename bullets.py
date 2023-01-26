from utils import ticks
from basis import *

class Bullet:
    def __init__(self, weapon):
        self.weapon = weapon

        self.skin = f"│"
        self.x = self.weapon.shooter.x
        self.y = self.weapon.shooter.y

        if self.weapon.shooter.IS_FORWARD:
            self.y_offset = -1
        else: self.y_offset = +1

    def process(self):
        if ticks(self.weapon.speed):
            self.y += self.y_offset