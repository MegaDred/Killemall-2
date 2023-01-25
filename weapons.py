from utils import ticks
import bullets

class MiniGun():
    def __init__(self, shooter):
        self.name = "MiniGun"
        self.damage = 1
        self.cost = 1
        self.speed = 50
        self.frequency = 5
        
        self.shooter = shooter

        self.bullet = bullets.Bullet

    def new_bullet(self) -> bullets.Bullet:
        return self.bullet(self)
    

class MachineGun():
    def __init__(self, shooter):
        self.name = "MachineGun"
        self.damage = 3
        self.cost = 1
        self.speed = 60
        self.frequency = 15

        self.shooter = shooter

        self.bullet = bullets.Bullet

    def new_bullet(self) -> bullets.Bullet:
        return self.bullet(self)
    
class UltraGun():
    def __init__(self, shooter):
        self.name = "UltraGun"
        self.damage = 2
        self.cost = 5
        self.speed = 200
        self.frequency = 100

        self.shooter = shooter

        self.bullet = bullets.Bullet

    def new_bullet(self) -> bullets.Bullet:
        return self.bullet(self)