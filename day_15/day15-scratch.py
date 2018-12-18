# Space

## map of (y, x) -> None or Elf or Goblin or Rock


from itertools import count
import sys
from util import living, init, show, locus, grave
from habitors import Habitor



def turn():
    actors = living()
    for actor in actors:
        if len(set(actor.kind for actor in living())) == 1:
            return False
        if not actor.alive:
            continue
        actor.move()
        actor.fight()
    return True


if __name__ == '__main__':
    for power in count(3):
        init(fn = sys.argv[1])
        Habitor.Elf.power = power
        rounds = 0 
        while True:
            if not turn():
                break
            rounds += 1
        health = sum(being.health for being in locus if being.alive)
        score = rounds * health
        dead_elves = [being for being in grave if being.kind is Habitor.Elf]
        print(power,rounds, health, score, len(dead_elves), sep = '\t')
        if not dead_elves:
            break


    # for place in sorted(space):
    #     if space[place] is Habitor.Elf:
    #         way = find(place)
    #         show(overlay={place: 'e', way: '*'})
    #         input()
