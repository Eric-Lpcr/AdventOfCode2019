

class Objects(dict):
    def __getitem__(self, object_code):
        if object_code in self:
            return dict.__getitem__(self, object_code)
        else:
            o = Object(object_code)
            self[object_code] = o
            return o


class Object:
    def __init__(self, object_code):
        self.code = object_code
        self.center = None
        self.orbit = None

    def compute_orbit(self, objects):
        if self.orbit is None:
            self.orbit = self.center.compute_orbit(objects) + 1
        return self.orbit

    def __str__(self):
        return self.code


def compute_orbit_path(obj):
    orbit_path = []
    center = obj.center
    while center is not None:
        orbit_path.append(center)
        center = center.center
    return orbit_path



def main():
    with open('input.txt') as f:
        orbits = f.readlines()

    objects = Objects()
    objects['COM'].orbit = 0

    for orbit in orbits:
        center_code, object_code = orbit.strip().split(')')
        objects[object_code].center = objects[center_code]

    res = sum([obj.compute_orbit(objects) for obj in objects.values()])
    print(f"Got {res} orbits")

    my_path = compute_orbit_path(objects['YOU'])
    santa_path = compute_orbit_path(objects['SAN'])
    common_objects = [obj for obj in my_path if obj in santa_path]
    first_common_object = common_objects[0]
    nb_transfers = objects['YOU'].orbit + objects['SAN'].orbit - 2 * first_common_object.orbit - 2
    print(f"Need {nb_transfers} orbit transfers to get close to Santa")


if __name__ == '__main__':
    main()
