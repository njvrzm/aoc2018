from itertools import count
import sys
from util import quick, begin, locus, grave
from habitors import Habitor

def turn():
    for actor in quick():
        if not actor.alive:
            # Killed this round
            continue
        if all(being.kind is actor.kind for being in quick()):
            # This check must be _before_ fight, not after, because
            # the round end condition is that an actor discovers they
            # have no-one left to fight. If the last actor kills the last
            # foe, and this check happens after, the round will incorrectly
            # be counted as incomplete.
            return False
        actor.move()
        actor.fight()
    return True


if __name__ == '__main__':
    for power in count(3):
        begin(fn = sys.argv[1])
        Habitor.Elf.power = power
        rounds = 0 
        while True:
            if not turn():
                break
            rounds += 1
        points = sum(being.points for being in locus if being.alive)
        score = rounds * points
        slain = sum(1  for being in grave if being.kind is Habitor.Elf)
        print(power, rounds, points, score, slain, sep = '\t')
        if not slain:
            break
