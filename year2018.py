from collections import defaultdict, deque
import time

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

EXIT = {
    UP : set(list("║╠╚╝╬╩╣")),
    DOWN : set(list("║╔╗╠╦╬╣")),
    LEFT : set(list("╗╦╝╬╩═╣")),
    RIGHT : set(list("╔╠╦╚╬╩═")),
}

REVERSE = {
    UP: DOWN,
    DOWN: UP,
    LEFT: RIGHT,
    RIGHT: LEFT
}

maze = defaultdict(str)

width = 0
height = 0
with open("year2018.txt") as f:
    for i, line in enumerate(f):
        height = max(i, height)
        for j, cell in enumerate(list(line.rstrip())):
            maze[(i, j)] = cell
            width = max(j, width)

print(maze)

start = (0, 0)
goal = (height, width) # note that h + w are the coordinates of the bottom right cell

# update height and width to reflect outer dimensions instead of the bottom right cell
height, width = height + 1, width + 1

def get_exits(maze, cell):
    exits = []
    i, j = cell
    for direction in DIRECTIONS:
        di, dj = direction
        next_cell = i + di, j + dj
        if next_cell not in maze:
            continue # never step outside
        if maze[cell] in EXIT[direction] and maze[next_cell] in EXIT[REVERSE[direction]]:
            exits.append(next_cell)
    return exits

def find_shortest_route():
    to_explore = deque([(start, 0)])
    visited = {start} # bfs, so visit when queing

    while len(to_explore) > 0:
        position, steps = to_explore.popleft()

        if position == goal:
            return steps

        for next_position in get_exits(maze, position):
            if next_position in visited:
                continue # never visit twice
            visited.add(next_position)
            to_explore.append((next_position, steps + 1))
    return None

def move_maze(maze, position, steps):
    moved_maze = {}
    moved_santa = False

    for cell, value in maze.items():
        i, j = cell
        if steps % 2 == 1: # odd = row
            row_index = (steps - 1) % height # TODO: check width/height
            if i == row_index:
                j = (j + 1) % width
        else:  # even = column
            col_index = (steps - 1) % width
            if j == col_index:
                i = (i + 1) % height
        moved_maze[(i, j)] = value
        if cell == position and not moved_santa: # TODO: avoid updating position twice!
            position = (i, j)
            moved_santa = True
    return moved_maze, position



def find_shortest_route_moving():
    to_explore = deque([(start, 0, maze)])
    visited = {(start, frozenset(maze.items()))} # bfs, so visit when queing

    while len(to_explore) > 0:
        position, steps, moving_maze = to_explore.popleft()

        if position == goal:
            return steps

        for next_position in get_exits(moving_maze, position):
            # TODO: check early for goal, before moving maze
            if next_position == goal:
                print("finish early before moving maze")
                return steps + 1

            next_maze, next_position = move_maze(moving_maze, next_position, steps + 1)
            maze_id = frozenset(next_maze.items())

            if (next_position, maze_id) in visited:
                continue # never visit twice
            visited.add((next_position, maze_id))
            to_explore.append((next_position, steps + 1, next_maze))
    return None

start_time = time.time()
print(f"Part 1: {find_shortest_route()}")
end_time = time.time()
print(f"{end_time - start_time} seconds") 

start_time = time.time()
print(f"Part 2: {find_shortest_route_moving()}")
end_time = time.time()
print(f"{end_time - start_time} seconds")
