from itertools import combinations

import math
import numpy as np
from shapely.geometry import Polygon
import smallestenclosingcircle

total = 0
presents = []
with open("year2023.txt") as f:
    for line in f:
        coordinates = line.rstrip().split("), ")
        min_size = 0
        present = []
        for coordinate in coordinates:
            x, y = map(int, coordinate.replace(")", "").replace("(", "").split(", "))
            present.append((x, y))

            min_size = max(min_size, math.sqrt(x*x + y*y))
        total += min_size
        presents.append(present)

print(f"Part 1: {int(total)}")


total = 0
for present in presents:
    center_x, center_y, radius = smallestenclosingcircle.make_circle(present)
    print(center_x, center_y, radius)

    total += radius

print(f"Part 2: {int(total)}")


