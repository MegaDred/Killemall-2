import random
from enum import Enum

import weapons
import keyboard
import projectiles

from basis import *
from utils import ticks, width_in_characters, height_in_characters, randbool


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

    def shoot(self) -> projectiles.Lazer:
        if self.weapon is not None and ticks(self.weapon.frequency) and self.shooting == True:
            return self.weapon(self).new_projectile ()
        else: return None

    def expend_energy(self, amount:int) -> None:
        if self.energy > amount:
            self.energy -= amount
        else: self.energy = 0

    def restore_energy(self, amount:int) -> None:
        if self.energy < self.MAX_ENERGY and amount > 0 and ticks(self.energy_restore_speed):
            if self.shooting == True and self.energy < self.weapon.cost: self.shooting = False
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

    def behavior(self, sv) -> None:
        self.move()

        shoot = self.shoot()
        if shoot is not None:
            sv.projectiles.append(shoot)

        self.restore_energy(5)

    @classmethod
    def spawn_roulete(self, sv, ec) -> bool:
        return False
    
    @classmethod
    def spawn_forcibly(self) -> bool:
        return False


class Player(SimpleEntity, Navigate):

    top_border = int(height_in_characters/3)*2
    bottom_border = height_in_characters-1
    right_border = width_in_characters-1
    left_border = 1

    def __init__(self, *, name:str="Player", health:int=1, energy:int=100, speed:int=40, skin:str="▲"):
        super().__init__(name, health, energy, speed, skin)

        self.IS_FORWARD = True
        self.IS_FRIENDLY = True
        
        self.x = int(width_in_characters/2)
        self.y = int((self.top_border + self.bottom_border)/2) if None not in (self.top_border, self.bottom_border) else int(height_in_characters/2)

        self.weapon = weapons.SG_228

        self.kills = 0
        self.lifetime = 0

    def shoot(self) -> projectiles.Lazer:
        if self.weapon is not None and ticks(self.weapon.frequency) and keyboard.is_pressed(57):
            return self.weapon(self).new_projectile()
        else: return None

    def restore_energy(self, amount:int):
        if self.energy < self.MAX_ENERGY and amount > 0 and ticks(self.energy_restore_speed) and not keyboard.is_pressed(57):
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
            if keyboard.is_pressed(72):  # up
                self.up()
            if keyboard.is_pressed(80):  # down
                self.down()
            if keyboard.is_pressed(77):  # right
                self.right()
            if keyboard.is_pressed(75):  # left
                self.left()

    def infobar_structure(self):    
        hit_points = '■'*round(self.health/(self.MAX_HEALTH/5))
        enrg_points = '■'*round(self.energy/(self.MAX_ENERGY/5))
        health = f"[ ♥ {hit_points}{' '*(5-len(hit_points))} {self.health} ]"
        energy = f"[ ♠ {enrg_points}{' '*(5-len(enrg_points))} {self.energy} ]"
        kills = f"[Kills: {self.kills}]"
        return f"\n{health} {energy} {kills} [Time: {self.lifetime}s]"

    def increment_kills(self):
        self.kills += 1

    def increment_seconds(self):
        if self.health != 0 and ticks(1): 
            self.lifetime += 1


class Bot(SimpleEntity, Navigate):

    top_border = 4
    bottom_border = int(height_in_characters/3)
    right_border = width_in_characters-1
    left_border = 1

    def __init__(self, *, name:str="Bot", health:int=1, energy:int=50, speed:int=20, skin:str="◊"):
        super().__init__(name, health, energy, speed, skin)

        self.IS_FORWARD = False
        self.IS_FRIENDLY = False

        self.x = random.randint(self.left_border, self.right_border)
        self.y = 0
        self.goal = None

        self.weapon = weapons.SG_228

        self.energy_restore_speed = 10

    def move(self):
        if ticks(self.speed):
            if self.y < self.top_border:
                self.y += 1
            elif self.y > self.bottom_border:
                self.y -= 1
            else:
                if self.goal != self.x and self.goal is not None:
                    if random.randint(1, 100) == 1: self.up()
                    elif random.randint(1, 100) == 1: self.down()

                    if self.goal > self.x: self.right()
                    elif self.goal < self.x: self.left()
                else:
                    self.goal = random.randint(self.left_border, self.right_border)

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
    
    @classmethod
    def spawn_forcibly(self) -> bool:
        if keyboard.is_pressed(2):
            return True
        else:
            return False


class Divider(SimpleEntity, Navigate):

    top_border = 4
    bottom_border = int(height_in_characters/3)
    right_border = width_in_characters-2
    left_border = 2

    def __init__(self, *, name:str="Divider", health:int=1, energy:int=1000, speed:int=20, skin:str="█"):
        super().__init__(name, health, energy, speed, skin)

        self.IS_FORWARD = False
        self.IS_FRIENDLY = False

        self.energy_restore_speed = 100

        self.x = random.randint(self.left_border+1, self.right_border-1)
        self.y = 0
        self.goal = None

        self.weapon = random.choice((weapons.MFK_337, weapons.UDG_95)) 

    def move(self):
        if ticks(self.speed):
            if self.y < self.top_border:
                self.y += 1
            elif self.y > self.bottom_border:
                self.y -= 1
            else:
                if self.goal != self.x and self.goal is not None:
                    if random.randint(1, 100) == 1: self.up()
                    elif random.randint(1, 100) == 1: self.down()

                    if self.goal > self.x: self.right()
                    elif self.goal < self.x: self.left()
                else:
                    if random.randint(1, 20) == 1: self.goal = random.randint(self.left_border, self.right_border) 

    @classmethod
    def spawn_roulete(self, sv, ec) -> bool:
        if ticks(1) and ec.player.kills >= 5 and ec.player.kills <= 45:
                probability = round(((20-abs(25-ec.player.kills))*((0.05-0.0001)/20))+0.0001, 6)
                return randbool(probability)
        
    @classmethod
    def spawn_forcibly(self) -> bool:
        if keyboard.is_pressed(3):
            return True
        else:
            return False


class EnumEntities(Enum):
    PLAYER = Player
    BOT = Bot
    DIVIDER = Divider