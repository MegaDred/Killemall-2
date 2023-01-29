from utils import ticks
import projectiles


class Weapon():
    name = "Unnamed"
    damage = 1
    cost = 0
    speed = 50
    frequency = 6
    projectile = projectiles.Lazer

    def __init__(self, shooter):
        self.shooter = shooter

    def new_projectile(self) -> projectile:
        if self.shooter.energy >= self.cost:
            self.shooter.expend_energy(self.cost)
            return self.projectile(self)


class SG_228(Weapon):
    name = "SG-228"
    damage = 1
    cost = 3
    speed = 55
    frequency = 6
    projectile = projectiles.Lazer

    def __init__(self, shooter):
        super().__init__(shooter)
    

class MFK_337(Weapon):
    name = "MFK-337"
    damage = 3
    cost = 5
    speed = 60
    frequency = 15
    projectile = projectiles.Lazer

    def __init__(self, shooter):
        super().__init__(shooter)
    

class UDG_95(Weapon):
    name = "UDG-95"
    damage = 5
    cost = 4
    speed = 100
    frequency = 100
    projectile = projectiles.Lazer

    def __init__(self, shooter):
        super().__init__(shooter)