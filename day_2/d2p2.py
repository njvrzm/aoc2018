import sys
words = map(str.strip, open(sys.argv[1]))

for i, wx in enumerate(words):
    for wy in words[i:]:
        try:
            [where] = [n for n, (cx, cy) in enumerate(zip(wx, wy)) if cx != cy]
        except ValueError:
            continue
        else:
            print wx[:where] + wy[where + 1:]
            sys.exit()
