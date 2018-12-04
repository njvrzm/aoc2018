import re

record_shape = '#{} @ {},{}: {}x{}'
record_names = ('index', 'x', 'y', 'w', 'h')
named_number = '(?P<{}>[0-9]+)'
rx_parts = [named_number.format(name) for name in record_names]

match = re.compile(record_shape.format(*rx_parts)).match
parse = lambda line:{k:int(v) for k, v in match(line).groupdict().items()}

occupied = set()
doubly_occupied = set()

for entry in map(parse, open('input.txt')):
    for x in range(entry['x'], entry['x'] + entry['w']):
        for y in range(entry['y'], entry['y'] + entry['h']):
            if (x, y) in occupied:
                doubly_occupied.add((x,y))
            occupied.add((x,y))

print(len(doubly_occupied))



