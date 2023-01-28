from entities import *

class EntityControl:

    def __init__(self):
        self.player = Player(name="Cherry")
        self.entities = [self.player]

    async def process(self, sv):
        self.entities = [i for i in self.entities if i.health != 0]
        for entity in EnumEntities:
            if entity.value.spawn_roulete(sv, self):
                self.entities.append(entity.value())
        for entity in self.entities:
            entity.behavior(sv)