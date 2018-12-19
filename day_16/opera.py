import re
from collections import defaultdict
from cpu import CPU

def scan(fn):
    op = None
    before = None

    for line in open(fn):
        numbers = [int(n) for n in re.findall('[0-9]+', line)]
        if not numbers:
            continue
        if 'After' in line:
            yield (before, op, numbers)
        elif 'Before' in line:
            before = numbers
        else:
            op = numbers


def part_one():
    core = CPU()
    multis = 0
    for i, (before, opcode, after) in enumerate(scan('codes.txt')):
        _num, a, b, c = opcode
        matching = 0
        for name in core.names:
            core.load(before)
            core.apply(name, a, b, c)
            if core.reg == after:
                print(i, before, name, a, b, c, after, sep = '\t')
                matching += 1
        if matching > 2:
            multis += 1
    print(multis)

def part_two():
    core = CPU()
    possible = defaultdict(lambda:set(core.names))
    definite = dict()
    for i, (before, opcode, after) in enumerate(scan('codes.txt')):
        num, a, b, c = opcode
        for name in set(possible[num]):
            core.load(before)
            core.apply(name, a, b, c)
            if core.reg != after:
                possible[num].remove(name)

    possible = dict(possible)
    while possible:
        available = defaultdict(list)
        for num, names in possible.items():
            for name in names:
                available[name].append(num)
        for name, nums in available.items():
            if len(nums) == 1:
                [num] = nums
                definite[num] = name
                possible.pop(num)
                for names in possible.values():
                    names.discard(name)
    for num, name in sorted(definite.items()):
        print(num, name, sep='\t')


    core.load()
    extract = re.compile('[0-9]+').findall
    print(core.reg)
    for numbers in map(extract, open('program.txt')):
        op, a, b, c = map(int, numbers)
        core.apply(definite[op], a, b, c)
        print((definite[op], a, b, c), core.reg, sep='\t')



if __name__ == '__main__':
    part_two()

