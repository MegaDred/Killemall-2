import weapons
import random
import keyboard
from colorama import Fore, Style

from utils import ticks, width_in_characters, height_in_characters
import bullets

class SimpleEntity:
    def __init__(self, name:str, health:int, energy:int, speed:int, skin:str):
        self.name = name
        self.health = health
        self.energy = energy
        self.speed = speed
        self.skin = skin

        self.weapon = None

    def shoot(self) -> bullets.Bullet:
        if self.weapon is not None and ticks(self.weapon(self).frequency):
            return self.weapon(self).new_bullet()
        else: return None

    def damage(self, amount:int):
        if self.health > amount:
            self.health -= amount
        else:
            self.health = 0

    def move(self):
        pass

class Player(SimpleEntity):

    def __init__(self, *, name:str, health:int, energy:int, speed:int, skin:str):
        super().__init__(name, health, energy, speed, skin)

        self.MAX_HEALTH = health
        self.MAX_ENERGY = energy
        self.IS_FORWARD = True
        self.IS_FRIENDLY = True

        self.keys = keyboard._pressed_events

        self.area_top_border = int(height_in_characters/3)*2
        self.area_bottom_border = height_in_characters-1
        self.area_right_border = width_in_characters-1
        self.area_left_border = 1

        self.x = int(width_in_characters/2)
        self.y = int((self.area_top_border + self.area_bottom_border)/2)

        self.weapon = weapons.MiniGun

    def shoot(self) -> bullets.Bullet:
        if self.weapon is not None and ticks(self.weapon(self).frequency) and 57 in self.keys.keys():
            return self.weapon(self).new_bullet()
        else: return None

    def expend_energy(self, amount:int):
        if self.energy > amount:
            self.energy -= amount
        else: self.energy = 0

    def restore_energy(self, amount:int):
        if self.energy < self.MAX_ENERGY and amount > 0:
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
            if 72 in self.keys.keys():  # up
                if not self.y-1 < self.area_top_border:
                    self.y -= 1
            if 80 in self.keys.keys():  # down
                if not self.y+1 > self.area_bottom_border:
                    self.y += 1
            if 77 in self.keys.keys():  # right
                if not self.x+1 > self.area_right_border:
                    self.x += 1
            if 75 in self.keys.keys():  # left
                if not self.x-1 < self.area_left_border:
                    self.x -= 1

class Bot(SimpleEntity):
    
    def __init__(self, *, name:str, health:int, energy:int, speed:int, skin:str):
        super().__init__(name, health, energy, speed, skin)

        self.MAX_HEALTH = health
        self.MAX_ENERGY = energy
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
                    if random.randint(1, 100) == 1 and self.y-1 >= self.area_top_border: self.y -= 1
                    elif random.randint(1, 100) == 1 and self.y+1 <= self.area_bottom_border: self.y += 1

                    if self.goal > self.x and self.x+1 <= self.area_right_border: self.x += 1
                    elif self.goal < self.x and self.x-1 >= self.area_left_border: self.x -= 1
                else:
                    self.goal = random.randint(self.area_left_border, self.area_right_border)

class Torturer(SimpleEntity):
    
    def __init__(self, *, name:str, health:int, energy:int, speed:int, skin:str):
        super().__init__(name, health, energy, speed, skin)

        self.MAX_HEALTH = health
        self.MAX_ENERGY = energy
        self.IS_FORWARD = False
        self.IS_FRIENDLY = False

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
                    if random.randint(1, 100) == 1 and self.y-1 >= self.area_top_border: self.y -= 1
                    elif random.randint(1, 100) == 1 and self.y+1 <= self.area_bottom_border: self.y += 1

                    if self.goal > self.x and self.x+1 <= self.area_right_border: self.x += 1
                    elif self.goal < self.x and self.x-1 >= self.area_left_border: self.x -= 1
                else:
                    if random.randint(1, 20) == 1: self.goal = random.randint(self.area_left_border, self.area_right_border)