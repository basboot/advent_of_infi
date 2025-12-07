
total = 0
instructions = []
with open("year2024.txt") as f:
    for line in f:
        instructions.append(line.rstrip().split(" "))

# print(instructions)


def cloud_machine(program, x, y, z):
    pc = 0
    program_stack = []

    while True:
        instruction = program[pc]
        if len(instruction) == 2:
            match instruction[1]:
                case "x":
                    value = x
                case "y":
                    value = y
                case "z":
                    value = z
                case _:
                    value = int(instruction[1])
        else:
            value = None

        match instruction[0]:
            case "push":
                program_stack.append(value)
            case "add":
                a = program_stack.pop()
                b = program_stack.pop()
                program_stack.append(a + b)
            case "jmpos":
                j = program_stack.pop()
                if j >= 0:
                    pc += value
            case "ret":
                return program_stack.pop()
        pc += 1

clouds = set()
total = 0
for x in range(30):
    for y in range(30):
        for z in range(30):
            value = cloud_machine(instructions, x, y, z)
            total += value
            if value > 0:
                clouds.add((x, y, z))

print(f"Part 1: {total}")

def find_cloud(cloud, x, y, z):
    cloud.add((x, y, z))
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            for dz in [-1, 0, 1]:
                nx, ny, nz = x + dx, y + dy, z + dz
                if (nx, ny, nz) in cloud:
                    continue
                elif (nx, ny, nz) in clouds:
                    cloud = find_cloud(cloud, nx, ny, nz)
    return cloud


# find clouds
n_clouds = 0
while len(clouds) > 0:
    cloud_part = list(clouds)[0]
    cloud = find_cloud(set(), *cloud_part)
    clouds -= cloud
    n_clouds += 1

print(f"Part 2: {n_clouds}")