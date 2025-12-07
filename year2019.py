import json
from heapq import heappop, heappush

flats = {}

with open('year2019.json', 'r') as f:
    data = json.load(f)

    for x, y in data["flats"]: # index by x for easy lookup
        flats[x] = y

    jumps = data["sprongen"]
    roofs = data["flats"]

    santa = data["flats"][0] # start at first

n_jumps = 0
for dx, dy in jumps:
    # print(f"Santa at {santa} jumps {dx}, {dy}")
    n_jumps += 1
    x, y = santa
    nx, ny = x + 1 + dx, y + dy # always 1 forward

    # print(f"Santa jumps to {nx}, {ny}")

    # on top or above flat?
    if nx in flats and ny >= flats[nx]:
        santa = (nx, flats[nx]) # always land on top
    else:
        print(f"Santa falls after {n_jumps}")
        break


# max 4 power, x=1 is minimaal en gratis

def get_next_roofs(i):
    next_roofs = []
    x, y = roofs[i]
    next_i = i + 1
    # there must still be a roof, and it must be closer than max jump
    while next_i < len(roofs) and roofs[next_i][0] - roofs[i][0] < 6:
        nx, ny = roofs[next_i]
        power_x = nx - x - 1 # one free in x direction
        power_y = max(0, (ny - y)) # only need to jump up, falling is free
        power = power_x + power_y
        if power < 5:
            next_roofs.append((next_i, power, power_x, power_y))
        next_i += 1
    return next_roofs

def find_least_power():
    to_explore = [(0, 0, [])]
    visited = set() # Don't add starting position here

    while len(to_explore) > 0:
        power, negative_position, roof_jumps = heappop(to_explore)
        position = -negative_position

        if position in visited: # do not explore again
            continue

        print(position)

        visited.add(position) # invalidate after exploring

        if position == len(roofs) - 1:
            return power, roof_jumps

        for next_position, next_power, x, y in get_next_roofs(position):
            if next_position in visited:
                continue # not needed, but speed things up a bit

            heappush(to_explore, (power + next_power, -next_position, roof_jumps + [[x, y]]))
    return None

print(f"Part 2: {find_least_power()}")

# print(get_next_roofs(0))


