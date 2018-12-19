import re
import sys

rx = '(?P<varone>[xy])=(?P<valone>[0-9]+), (?P<vartwo>[xy])=(?P<vallo>[0-9]+)\.\.(?P<valhi>[0-9]+)'

space = dict()

for intrusion in map(re.open(sys.argv[1])):
    interp = re.match(rx, line).groupdict()
    w = int(interp['valone'])
    onevar = interp['varone']
    loval = int(interp['vallo'])
    hival = int(interp['valhi'])
    for z in range(loval, hival + 1):
        point = (w, z) if onevar == 'x' else (z, w)
        space[point] = '#'

