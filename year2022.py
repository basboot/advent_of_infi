import numpy as np
import matplotlib.pyplot as plt

instructions = []

with open("year2022.txt") as f:
    for line in f:
        instruction, value = line.rstrip().split(" ")
        instructions.append((instruction, int(value)))

N, E, S, W = -1, 1j, 1, -1j

directions = [[N],[N, E], [E], [S, E], [S], [S, W], [W], [N, W]]

print(instructions)

santa_direction = 0
santa_position = 0

tracks = [[(0, 0)]]

for instruction, value in instructions:
    match instruction:
        case "loop":
            for direction in directions[santa_direction]:
                santa_position += value * direction
        case "spring":
            tracks.append([])
            for direction in directions[santa_direction]:
                santa_position += value * direction
        case "draai":
            santa_direction = (santa_direction + value // 45) % len(directions)
    tracks[-1].append((santa_position.imag, santa_position.real))

print(f"Part 1: {abs(santa_position.real) + abs(santa_position.imag)}")

# Plot the collision tracks
plt.figure(figsize=(12, 8))
for i, track in enumerate(tracks):
    if not track:
        continue
    track_np = np.array(track)
    plt.plot(track_np[:, 0], -track_np[:, 1], alpha=0.7, marker='o', label=f'Track {i+1}')

plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.title('Santa Tracks')
plt.grid(True, alpha=0.3)
plt.show()
