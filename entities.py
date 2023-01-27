import weapons
import random
import keyboard
from colorama import Fore, Style
from basis import *

from utils import ticks, width_in_characters, height_in_characters, is_pressed
import bullets

class SimpleEntity:
    def __init__(self, name:str, health:int, energy:int, speed:int, skin:str):
        self.name = name
        self.health = health
        self.energy = energy
        self.speed = speed
        self.skin = skin

        self.weapon = None

        self.MAX_HEALTH = health
        self.MAX_ENERGY = energy

        self.energy_restore_speed = 15

        self.shooting = True

    def shoot(self) -> bullets.Bullet:
        if self.weapon is not None and ticks(self.weapon(self).frequency) and self.shooting == True:
            return self.weapon(self).new_bullet()
        else: return None

    def expend_energy(self, amount:int):
        if self.energy > amount:
            self.energy -= amount
        else: self.energy = 0

    def restore_energy(self, amount:int):
        if self.energy < self.MAX_ENERGY and amount > 0 and ticks(self.energy_restore_speed):
            if self.shooting == True and self.energy < self.weapon(self).cost: self.shooting = False
            elif self.shooting == False and self.energy == self.MAX_ENERGY: self.shooting = True

            if self.shooting == False:
                if self.MAX_ENERGY - self.energy > amount:
                    self.energy += amount
                else: self.energy = self.MAX_ENERGY
                if self.energy == self.MAX_ENERGY:
                    self.shooting = True
        

    def damage(self, amount:int):
        if self.health > amount:
            self.health -= amount
        else:
            self.health = 0

    def move(self):
        pass


class Player(SimpleEntity, Navigate):

    def __init__(self, *, name:str="Player", health:int=1, energy:int=100, speed:int=40, skin:str="▲"):
        super().__init__(name, health, energy, speed, skin)

        self.IS_FORWARD = True
        self.IS_FRIENDLY = True

        self.area_top_border = int(height_in_characters/3)*2
        self.area_bottom_border = height_in_characters-1
        self.area_right_border = width_in_characters-1
        self.area_left_border = 1

        self.x = int(width_in_characters/2)
        self.y = int((self.area_top_border + self.area_bottom_border)/2)

        self.weapon = weapons.MiniGun

    def shoot(self) -> bullets.Bullet:
        if self.weapon is not None and ticks(self.weapon(self).frequency) and is_pressed(57):
            return self.weapon(self).new_bullet()
        else: return None

    def restore_energy(self, amount:int):
        if self.energy < self.MAX_ENERGY and amount > 0 and ticks(self.energy_restore_speed) and is_pressed(57):
            if self.MAX_ENERGY - self.energy > amount:
                self.energy += amount
            else: self.energy = self.MAX_ENERGY

    def heal(self, amount:int):
        if self.health < self.MAX_HEALTH and amount > 0 and self.health > 0:
            if self.MAX_HEALTH - self.health > amount:
                self.health += amount
            else: self.health = self.MAX_HEALTH

    def move(self):
        if ticks(self.speed):
            if is_pressed(72):  # up
                self.up()
            if is_pressed(80):  # down
                self.down()
            if is_pressed(77):  # right
                self.right()
            if is_pressed(75):  # left
                self.left()


class Bot(SimpleEntity, Navigate):
    
    def __init__(self, *, name:str="Bot", health:int=1, energy:int=50, speed:int=20, skin:str="◊"):
        super().__init__(name, health, energy, speed, skin)

        self.IS_FORWARD = False
        self.IS_FRIENDLY = False

        self.area_top_border = 4
        self.area_bottom_border = int(height_in_characters/3)
        self.area_right_border = width_in_characters-1
        self.area_left_border = 1

        self.x = random.randint(self.area_left_border, self.area_right_border)
        self.y = 0
        self.goal = None

        self.weapon = weapons.MiniGun

    def move(self):
        if ticks(self.speed):
            if self.y < self.area_top_border:
                self.y += 1
            elif self.y > self.area_bottom_border:
                self.y -= 1
            else:
                if self.goal != self.x and self.goal is not None:
                    if random.randint(1, 100) == 1: self.up()
                    elif random.randint(1, 100) == 1: self.down()

                    if self.goal > self.x: self.right()
                    elif self.goal < self.x: self.left()
                else:
                    self.goal = random.randint(self.area_left_border, self.area_right_border)


class Torturer(SimpleEntity, Navigate):
    
    def __init__(self, *, name:str="Torturer", health:int=1, energy:int=1000, speed:int=20, skin:str="█"):
        super().__init__(name, health, energy, speed, skin)

        self.IS_FORWARD = False
        self.IS_FRIENDLY = False

        self.energy_restore_speed = 100

        self.area_top_border = 4
        self.area_bottom_border = int(height_in_characters/3)
        self.area_right_border = width_in_characters-2
        self.area_left_border = 2

        self.x = random.randint(self.area_left_border+1, self.area_right_border-1)
        self.y = 0
        self.goal = None

        self.weapon = random.choice((weapons.MachineGun, weapons.UltraGun)) 

    def move(self):
        if ticks(self.speed):
            if self.y < self.area_top_border:
                self.y += 1
            elif self.y > self.area_bottom_border:
                self.y -= 1
            else:
                if self.goal != self.x and self.goal is not None:
                    if random.randint(1, 100) == 1: self.up()
                    elif random.randint(1, 100) == 1: self.down()

                    if self.goal > self.x: self.right()
                    elif self.goal < self.x: self.left()
                else:
                    if random.randint(1, 20) == 1: self.goal = random.randint(self.area_left_border, self.area_right_border)