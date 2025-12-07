forrest = {}
width = 0
height = 0

with open("year2025.txt") as f:
    for i, line in enumerate(f):
        for j, cell in enumerate(list(line.strip())):
            width = max((j - 1) // 3, width)
            height = max(i - 1, height)
            if cell.isnumeric():
                forrest[(i - 1, (j - 1) // 3)] = int(cell)

# (on)even rij/kolom = (on)even plekken

# map rows and cols, and store full grid
rows = []
cols = []
grid = set()

for i in range(height):
    row = []
    for j in range(width + 1):
        if (i % 2) == (j % 2):
            row.append((i, j))
            grid.add((i, j))
    rows.append(row)

for j in range(width + 1):
    col = []
    for i in range(height):
        if (i % 2) == (j % 2):
            col.append((i, j))
    cols.append(col)


def find_fluorescent_places(cell, dir):
    bounce_directions = {
        "N": [(1, -1), (1, 1)],
        "S": [(-1, -1), (-1, 1)],
        "E": [(-1, -1), (1, -1)],
        "W": [(-1, 1), (1, 1)],
    }

    lit = set()
    height = forrest[cell]

    for di, dj in bounce_directions[dir]:
        max_height = 0
        position = cell
        while height > max_height:
            i, j = position
            ni, nj = i + di, j + dj
            position = (ni, nj)
            if position not in grid:
                break # stop outside grid

            if max_height == 0: # when at ground level everything is reachable
                lit.add(position)
            if position in forrest and forrest[position] > max_height: # when a tree is hit level rises
                lit.add(position)
                max_height = forrest[position]
                
    return lit



def find_lit_places(dir):
    if dir in {"N", "S"}:
        tree_map = cols
    else:
        tree_map = rows

    if dir in {"N", "W"}:
        direction = 1
        offset = 0
    else:
        direction = -1
        offset = -1

    lit = set()

    for tree_line in tree_map:
        max_height = 0
        for i in range(len(tree_line)):
            cell = tree_line[i * direction + offset]
            if max_height == 0: # when at ground level everything is reachable
                lit.add(cell)
            if cell in forrest and forrest[cell] > max_height: # when a tree is hit level rises
                lit.add(cell)
                max_height = forrest[cell]

                # add fluorescent hit trees
                lit = lit.union(find_fluorescent_places(cell, dir))
    return lit

def has_2_neighbours_size_2(cell):
    i, j = cell
    count = 0
    for neighbour in {
        (i - 2, j),
        (i + 2, j),
        (i - 1, j - 1),
        (i + 1, j - 1),
        (i - 1, j + 1),
        (i + 1, j + 1),
    }:
        if neighbour in forrest and forrest[neighbour] >= 2:
            count += 1
    return count >= 2

light_directions = ["N", "E", "S", "W"]
trees_cut = 0

for days in range(256):

    lit = find_lit_places(light_directions[days % len(light_directions)])
    next_forrest = {}
    for cell in forrest:
        # grow or remove
        if cell in lit:
            if forrest[cell] == 4:
                trees_cut += 1 # remove
            else:
                next_forrest[cell] = forrest[cell] + 1
        else: # no grow
            next_forrest[cell] = forrest[cell]

    # plant
    for cell in lit:
        if cell not in forrest and has_2_neighbours_size_2(cell):
            next_forrest[cell] = 0

    forrest = next_forrest


print(f"Part 2: {trees_cut}")