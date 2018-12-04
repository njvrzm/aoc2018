import re

record_shape = '#{} @ {},{}: {}x{}'
record_names = ('index', 'x', 'y', 'w', 'h')
named_number = '(?P<{}>[0-9]+)'
number_parts = [named_number.format(name) for name in record_names]
record_match = re.compile(record_shape.format(*number_parts)).match

def parse(line):
    claim = {k:int(v) for k, v in record_match(line).groupdict().items()}
    claim['xr'] = claim['x'] + claim['w']
    claim['yd'] = claim['y'] + claim['h']
    claim['good'] = True
    return claim

claims = list(map(parse, open('input.txt')))

def overlap(one, two):
    # There is not overlap if one's right edge is lefter than two's left edge,
    # or two's right edge is lefter than one's left edge, etc.
    return not (one['xr'] < two['x'] or two['xr'] < one['x']
            or one['yd'] < two['y'] or two['yd'] < one['y'])

for one in claims:
    for two in claims:
        if one is two:
            continue
        if overlap(one, two):
            one['good'] = False
            break
    if one['good']:
        print('{index} is the one'.format(**one))
        break

