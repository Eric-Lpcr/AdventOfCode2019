from collections import namedtuple


class WireMap(dict):
    def __setitem__(self, key, value):
        if key not in self:
            dict.__setitem__(self, key, set())
        self[key].add(value)

    def __getitem__(self, item):
        if item not in self:
            return set()
        else:
            return dict.__getitem__(self, item)


Point = namedtuple('Point', ['x', 'y'])


def manhattan_distance(point):
    return abs(point.x) + abs(point.y)


def main():
    with open('input.txt') as f:
        wires = f.readlines()

    # wires = [
    #     "R75,D30,R83,U83,L12,D49,R71,U7,L72",
    #     "U62,R66,U55,R34,D71,R55,D58,R83"
    # ]
    # wires = [
    #     "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
    #     "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"
    # ]

    wire_map = WireMap()
    for wire_num, wire in enumerate(wires):
        x = y = 0
        for path in wire.split(','):
            direction = path[0]
            distance = int(path[1:])
            if direction == 'R':
                for _ in range(distance):
                    x += 1
                    wire_map[Point(x, y)] = wire_num
            elif direction == 'L':
                for _ in range(distance):
                    x -= 1
                    wire_map[Point(x, y)] = wire_num
            elif direction == 'U':
                for _ in range(distance):
                    y += 1
                    wire_map[Point(x, y)] = wire_num
            elif direction == 'D':
                for _ in range(distance):
                    y -= 1
                    wire_map[Point(x, y)] = wire_num
            else:
                raise ValueError(f"Unknown direction {direction}")

    intersections = [p for p, wires in wire_map.items() if len(wires) > 1]
    distances = [manhattan_distance(p) for p in intersections]
    nearest = min(distances)

    print(f"Nearest crossing between two wires is at {nearest}")


if __name__ == '__main__':
    main()
