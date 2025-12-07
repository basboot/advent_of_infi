def bag_content(n):
    content = 0
    material = n * 2 # top + bottom
    width = n
    # bottom
    for i in range(n):
        content += (n + i * 2)
        material += 4 # bottom + top
    # top
    content *= 2

    # middle
    content += n * (n + n * 2)
    material += n * 2

    return content, material

def minimal_bag_size(n):
    size = 1
    while True:
        if bag_content(size)[0] >= n:
            return size
        size += 1


continents = [4541396896, 1340812277, 747701769, 430855650, 368995941, 42712683]

print(f"Part 1: {minimal_bag_size(17474944)}")

materials = 0

for continent in continents:
    print("Contintent:", continent)
    minimal_size = minimal_bag_size(continent)
    _, material = bag_content(minimal_size)
    materials += material

print(f"Part 2: {materials}")