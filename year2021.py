from copy import copy

import numpy as np
import matplotlib.pyplot as plt
import pulp as pl

with open("year2021.txt") as f:
    lines = [line.rstrip() for line in f]

parts = {}
recipes = {}
toys = {}
toy_parts = set()

missing_parts = int(lines[0].split(" ")[0])
for line in lines[1:]:
    toy = line.split(": ")[0]
    parts[toy] = None

    recipe = []
    for part in line.split(": ")[1].split(", "):
        amount, toy_part = part.split(" ")
        recipe.append((int(amount), toy_part))
        toy_parts.add(toy_part)
    recipes[toy] = recipe

# Model
model = pl.LpProblem("MILP toy problem", pl.LpMinimize)

for toy in recipes:
    if toy not in toy_parts:
        toys[toy] = pl.LpVariable(toy, lowBound=0, cat="Integer")


def get_parts(toy):
    if toy not in parts:
        parts[toy] = 1

    if parts[toy] is None:
        parts[toy] = calculate_parts(toy)

    return parts[toy]

def calculate_parts(toy):
    assert parts[toy] is None, "Parts already calculated"
    n_parts = 0
    for amount, toy_part in recipes[toy]:
        n_parts += amount * get_parts(toy_part)
    return n_parts


max_parts = 0
for toy in recipes:
    n_parts = get_parts(toy)
    print(toy, n_parts)
    max_parts = max(max_parts, n_parts)

print(f"Part 1: {max_parts}")

print(f"Missing parts #{missing_parts}")
print(f"Toys: {toys}")

total_produced_parts = pl.lpSum(get_parts(toy) * toys[toy] for toy in toys)
total_produced_toys = pl.lpSum(toys[toy] for toy in toys)

# minimize number of used parts
model += total_produced_parts

# used parts must be minimal the real used parts
model += total_produced_parts >= missing_parts

# there must be 20 toys
model += total_produced_toys >= 20
model += total_produced_toys <= 20

print(model)

model.solve()

print("Status:", pl.LpStatus[model.status])
solution = []
total_parts = 0
for toy in toys:
    print(f"{toy} =", toys[toy].value())
    if toys[toy].value() > 0:
        solution += toy[0] * int(toys[toy].value())
        total_parts += int(toys[toy].value()) * get_parts(toy)

solution.sort()
print(f"Part 2: {total_parts} - {"".join(solution)}")

