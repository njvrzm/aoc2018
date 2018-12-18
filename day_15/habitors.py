from enum import Enum

class Habitor(Enum):
    Rock = '#'
    Goblin = 'G'
    Elf = 'E'
    Space = '.'

    @property
    def foe(self):
        if self in (Habitor.Goblin, Habitor.Elf):
            return Habitor.Elf if self is Habitor.Goblin else Habitor.Goblin
        else: # Why not?
            return Habitor.Rock if self is Habitor.Space else Habitor.Space

Habitor.Elf.power = 3
Habitor.Goblin.power = 3
Habitor.Rock.power = 0
Habitor.Space.power = 0
