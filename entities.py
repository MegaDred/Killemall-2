import random
from enum import Enum

import weapons
import bullets

from basis import *
from utils import ticks, width_in_characters, height_in_characters, is_pressed, randbool


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

    def expend_energy(self, amount:int) -> None:
        if self.energy > amount:
            self.energy -= amount
        else: self.energy = 0

    def restore_energy(self, amount:int) -> None:
        if self.energy < self.MAX_ENERGY and amount > 0 and ticks(self.energy_restore_speed):
            if self.shooting == True and self.energy < self.weapon(self).cost: self.shooting = False
            elif self.shooting == False and self.energy == self.MAX_ENERGY: self.shooting = True

            if self.shooting == False:
                if self.MAX_ENERGY - self.energy > amount:
                    self.energy += amount
                else: self.energy = self.MAX_ENERGY
                if self.energy == self.MAX_ENERGY:
                    self.shooting = True
        
    def damage(self, amount:int) -> None:
        if self.health > amount:
            self.health -= amount
        else:
            self.health = 0

    def move(self):
        pass

    def behavior(self, sysvars) -> None:
        self.move()

        shoot = self.shoot()
        if shoot is not None:
            sysvars.bullets.append(shoot)

        self.restore_energy(5)

    @classmethod
    def spawn_roulete(self, sv, ec) -> bool:
        return False


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

        self.kills = 0
        self.lifetime = 0

    def shoot(self) -> bullets.Bullet:
        if self.weapon is not None and ticks(self.weapon(self).frequency) and is_pressed(57):
            return self.weapon(self).new_bullet()
        else: return None

    def restore_energy(self, amount:int):
        if self.energy < self.MAX_ENERGY and amount > 0 and ticks(self.energy_restore_speed) and not is_pressed(57):
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

    def infobar_structure(self):    
        hit_points = '■'*round(self.health/(self.MAX_HEALTH/5))
        enrg_points = '■'*round(self.energy/(self.MAX_ENERGY/5))
        health = f"[ ♥ {hit_points}{' '*(5-len(hit_points))} {self.health} ]"
        energy = f"[ ♠ {enrg_points}{' '*(5-len(enrg_points))} {self.energy} ]"
        kills = f"[Kills: {self.kills}]"
        return f"{health} {energy} {kills} [Time: {self.lifetime}s]"

    def increment_kills(self):
        self.kills += 1

    def increment_seconds(self):
        if self.health != 0 and ticks(1): 
            self.lifetime += 1


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

        self.energy_restore_speed = 10

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

    @classmethod
    def spawn_roulete(self, sv, ec) -> bool:
        if ticks(1):
            probability = 0.5
            bots = 0
            divider = False
            for i in ec.entities:
                if isinstance(i, Bot):
                    bots += 1
                if isinstance(i, Divider):
                    divider = True

            if bots == 1: probability = 0.05
            elif bots == 2: probability = 0.01
            elif bots >= 3: probability = 0.001
            
            if divider: probability /= 200

            return randbool(probability)


class Divider(SimpleEntity, Navigate):
    
    def __init__(self, *, name:str="Divider", health:int=1, energy:int=1000, speed:int=20, skin:str="█"):
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

    @classmethod
    def spawn_roulete(self, sv, ec) -> bool:
        if ticks(1) and ec.player.kills >= 5 and ec.player.kills <= 45:
                probability = round(((20-abs(25-ec.player.kills))*((0.05-0.0001)/20))+0.0001, 6)
                return randbool(probability)


class EnumEntities(Enum):
    PLAYER = Player
    BOT = Bot
    DIVIDER = Divider