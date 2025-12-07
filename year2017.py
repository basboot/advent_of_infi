from copy import copy

import numpy as np
import matplotlib.pyplot as plt

with open("year2017.txt") as f:
    start_positions, moves = f.readline().rstrip().split("](")

start_positions = start_positions.replace("[", "").split("]")
moves = moves.replace(")", "").split("(")

robots = []
for start_position in start_positions:
    i, j = start_position.split(",")
    robots.append((int(i), int(j)))

collisions = 0

tracks = [[position] for position in robots]
collision_tracks = []

for robot, move in enumerate(moves):
    di, dj = list(map(int, move.split(",")))

    ci, cj = robots[robot % len(robots)]
    robots[robot % len(robots)] = (ci + di, cj + dj)

    tracks[robot % len(robots)].append(robots[robot % len(robots)])

    # print(robots)

    if robot % len(robots) == len(robots) - 1: # epoch
        # print("CHECK")
        positions = set()
        if len(robots) > len(set(robots)):
            collisions += 1
            collision_tracks.append(robots[robot % len(robots)] )



print(f"Collisions {collisions}")

tracks = np.array(tracks)

print("TT", tracks.shape)


# Plot the collision tracks
collision_tracks = np.array(collision_tracks)
plt.figure(figsize=(12, 8))
plt.scatter(collision_tracks[:, 0], -collision_tracks[:, 1], label='Collisions', alpha=0.7, s=20, color='red')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.title('Collision Points')
plt.grid(True, alpha=0.3)
plt.show()



