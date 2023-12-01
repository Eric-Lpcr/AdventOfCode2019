from collections import namedtuple


WireStep = namedtuple('WireStep', ['wire_num', 'step'])


class WireWasHere(dict):
    """ A special dict whose key is a wire number and value is a list of number of steps """
    def __setitem__(self, wire_num, step):
        if wire_num not in self:
            dict.__setitem__(self, wire_num, list())
        self[wire_num].append(step)

    def __getitem__(self, wire_num):
        if wire_num not in self:
            return list()
        else:
            return dict.__getitem__(self, wire_num)

    def put(self, wire_step):
        self[wire_step.wire_num] = wire_step.step  # use __setitem__

    def get_shortest_combined_path(self):
        return sum([min(number_of_steps) for number_of_steps in self.values()])


class WireMap(dict):
    """ A special dict whose key is a point and value is a WireWasHere
        Mimics a sparse matrix
    """
    def __setitem__(self, point, wire_step):
        if point not in self:
            dict.__setitem__(self, point, WireWasHere())
        self[point].put(wire_step)

    def __getitem__(self, point):
        if point not in self:
            return WireWasHere()
        else:
            return dict.__getitem__(self, point)


Point = namedtuple('Point', ['x', 'y'])


def manhattan_distance(point):
    return abs(point.x) + abs(point.y)


def main():
    with open('input.txt') as f:
        wires = f.readlines()

    # wires = [
    #     "R8,U5,L5,D3",
    #     "U7,R6,D4,L4"
    # ]
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
        x = y = step = 0
        for path in wire.split(','):
            direction = path[0]
            distance = int(path[1:])
            if direction == 'R':
                for _ in range(distance):
                    x += 1
                    step += 1
                    wire_map[Point(x, y)] = WireStep(wire_num, step)
            elif direction == 'L':
                for _ in range(distance):
                    x -= 1
                    step += 1
                    wire_map[Point(x, y)] = WireStep(wire_num, step)
            elif direction == 'U':
                for _ in range(distance):
                    y += 1
                    step += 1
                    wire_map[Point(x, y)] = WireStep(wire_num, step)
            elif direction == 'D':
                for _ in range(distance):
                    y -= 1
                    step += 1
                    wire_map[Point(x, y)] = WireStep(wire_num, step)
            else:
                raise ValueError(f"Unknown direction {direction}")

    intersections = {p: wire_was_here for p, wire_was_here in wire_map.items() if len(wire_was_here) > 1}

    distances = [manhattan_distance(p) for p in intersections]
    nearest = min(distances)
    print(f"Nearest crossing between two wires is at {nearest}")

    shortest_steps = [wire_was_here.get_shortest_combined_path() for wire_was_here in intersections.values()]
    shortest_step = min(shortest_steps)
    print(f"Shortest combined path to a crossing is {shortest_step}")


if __name__ == '__main__':
    main()
