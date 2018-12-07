def sweep(string):
    last = string[0]
    skip = False
    for char in string[1:]:
        if skip:
            skip = False
        else:
            if char.lower() != last.lower() or char == last:
                yield last
            else:
                skip = True

        last = char
    if not skip:
        yield last

def react(string):
    new = ''
    while len(new) < len(string):
        if new:
            string = new
        new = list(sweep(string))
    return ''.join(new)

