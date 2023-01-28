from utils import ticks
import bullets

class MiniGun():
    def __init__(self, shooter):
        self.name = "MiniGun"
        self.damage = 1
        self.cost = 3
        self.speed = 55
        self.frequency = 6
        
        self.shooter = shooter

        self.bullet = bullets.Bullet

    def new_bullet(self) -> bullets.Bullet:
        if self.shooter.energy >= self.cost:
            self.shooter.expend_energy(self.cost)
            return self.bullet(self)
    

class MachineGun():
    def __init__(self, shooter):
        self.name = "MachineGun"
        self.damage = 3
        self.cost = 5
        self.speed = 60
        self.frequency = 15

        self.shooter = shooter

        self.bullet = bullets.Bullet

    def new_bullet(self) -> bullets.Bullet:
        if self.shooter.energy >= self.cost:
            self.shooter.expend_energy(self.cost)
            return self.bullet(self)
    
class UltraGun():
    def __init__(self, shooter):
        self.name = "UltraGun"
        self.damage = 5
        self.cost = 4
        self.speed = 100
        self.frequency = 100

        self.shooter = shooter

        self.bullet = bullets.Bullet

    def new_bullet(self) -> bullets.Bullet:
        if self.shooter.energy >= self.cost:
            self.shooter.expend_energy(self.cost)
            return self.bullet(self)